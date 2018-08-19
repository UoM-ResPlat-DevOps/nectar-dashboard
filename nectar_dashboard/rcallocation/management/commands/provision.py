import logging
import datetime
from dateutil.relativedelta import relativedelta

from nectarallocationclient import client
from nectarallocationclient.exceptions import AllocationDoesNotExist, \
    Forbidden

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from nectar_dashboard.rcallocation.models import AllocationRequest
from nectar_dashboard.rcallocation import utils

LOG = logging.getLogger('rcallocation.commands.provision')


class Command(BaseCommand):
    help = 'Provisions resources for allocations which have been approved.'

    # Create dict so we can convert from letters to full status names
    statuses = dict(AllocationRequest.REQUEST_STATUS_CHOICES)

    def add_arguments(self, parser):
        parser.add_argument('--noinput',
            action='store_true',
            dest='no_prompts',
            default=False,
            help='Do NOT prompt the user for input of any kind.')
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Run the command without invoking any API calls.')
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Do NOT skip when operations fail.')
        parser.add_argument('-p', '--project-name',
            nargs='+',
            dest='project_name',
            default=False,
            help='Limit provisioning to specific allocation requests by '
                'specifying their project_name(s).')

    def handle(self, *args, **options):
        LOG.debug("Executing command '{0}' with options: {1}".format(
            __name__.split('.')[-1], str(options)))

        self.options = options
        self.dry_run = options['dry_run']
        self.force = options['force']

        try:
            self.nectar = utils.get_nectar_client()
        except Exception as e:
            LOG.critical(e.message)
            raise CommandError(str(e))

        # Generate a project_name filter and sanitise project_name input(s)
        project_filter = Q()
        if options['project_name']:
            for project_name in options['project_name']:
                # Raise error if project_name does not exist
                search = AllocationRequest.objects.filter(
                    project_name=project_name)
                if not search:
                    raise CommandError('There are no allocation requests with '
                        'the project_name {0}.'.format(project_name))
                # Raise error if latest AR object is not in Approved state
                search = search.filter(parent_request=None)
                status = search[0].status
                if status != 'A':
                    raise CommandError('The status of allocation request with '
                        'project_name {0} is "{1}" and needs to be "{2}".'
                        ''.format(project_name, self.statuses[status],
                        self.statuses['A']))
                # Add project_name to filter
                project_filter = project_filter | Q(project_name=project_name)

        # Find approved allocation requests on local database which have not
        # been provisioned yet
        allocs = AllocationRequest.objects.filter(parent_request=None).filter(
            project_filter & Q(status='A') & Q(provisioned=False)).order_by(
            '-modified_time')
        allocs_locked = allocs.filter(locked=True)
        allocs_unlocked = allocs.filter(locked=False)

        # Summary for console
        self.stdout.write(self.style.MIGRATE_HEADING("Operations to perform:"))
        if allocs_unlocked:
            self.stdout.write(self.style.MIGRATE_LABEL("  Register new "
                "approvals with NeCTAR: "), ending='')
            for i, alloc in enumerate(allocs_unlocked):
                ending=', '
                if i == len(allocs_unlocked) - 1:
                    ending='\n'
                self.stdout.write(alloc.project_name, ending=ending)
        if allocs_locked:
            self.stdout.write(self.style.MIGRATE_LABEL("  Check if pending "
                "approvals have been provisioned by NeCTAR, and process: "),
                ending='')
            for i, alloc in enumerate(allocs_locked):
                ending=', '
                if i == len(allocs_locked) - 1:
                    ending='\n'
                self.stdout.write(alloc.project_name, ending=ending)

        # For each new allocation approval that needs to be registered on the
        # NeCTAR database
        for alloc_local in allocs_unlocked:
            self.register_new_approval(alloc_local)

        # For each allocation approval that has been registered on the NeCTAR
        # database and are awaiting provisioning
        for alloc_local in allocs_locked:
            self.process_pending_approval(alloc_local)

    def register_new_approval(self, alloc_local):
        project_name = alloc_local.project_name
        self.stdout.write(self.style.MIGRATE_HEADING("\nRegistering allocation"
            " approval with project_name {0}:".format(project_name)))

        project_is_new = self.project_is_new(alloc_local)

        # Retrieve the allocation in the NeCTAR allocations database. Match
        # on project_name
        if project_is_new:
            self.stdout.write("  Checking if project_name is available in "
            "NeCTAR allocations database... ", ending='')
        else:
            self.stdout.write("  Retrieving allocation from NeCTAR database..."
                " ", ending='')
        try:
            alloc_nectar = self.nectar.allocations.get_current(
                project_name=project_name
            )
            if project_is_new:
                self.write_failed("Allocation is new but project_name {0} "
                    "already exists in NeCTAR database.".format(project_name))
                if not self.force:
                    return
            else:
                # TODO: Verify this is the right allocation by confirming that
                # the contact_email field is the same
                self.write_ok()
        except AllocationDoesNotExist:
            if project_is_new:
                self.write_ok()
                pass
            else:
                self.write_failed("Attempted to retrieve allocation with "
                    "project_name {0} from NeCTAR database, but failed."
                    "".format(project_name))
                if not self.force:
                    return
        except Exception as e:
            self.write_failed("Unexpected exception raised: " + str(e))
            if not self.force:
                return

        # These fields will be defaulted to these values for both
        # create and update
        default_fields = {
            'notifications': False
        }

        # Create the allocation object if new
        if project_is_new:
            alloc_create_data = {
                'project_name': alloc_local.project_name,
                'project_description': alloc_local.project_description,
                'start_date': alloc_local.start_date,
                'convert_trial_project': alloc_local.convert_trial_project,
                'allocation_home': alloc_local.allocation_home,
                'use_case': alloc_local.use_case,
            }
            alloc_create_data.update(default_fields)
            if not self.dry_run:
                self.stdout.write("  Creating new allocation on the NeCTAR "
                    "database... ", ending='')
                try:
                    alloc_nectar = self.nectar.allocations.create(
                        **alloc_create_data)
                    self.write_ok()
                except Exception as e:
                    self.write_failed("Exception raised when attempting to "
                        "create allocation {0} in NeCTAR database: {1}".format(
                        project_name, str(e)))
                    if not self.force:
                        return
            else:
                self.stdout.write("  An allocation would have been created on "
                    "the NeCTAR database with data={0}.".format(str(
                    alloc_create_data)))
                alloc_nectar = None

        # Generate a new start_date
        # TODO: Find out whether the start_date is ever changed by NeCTAR on
        # their database during the provisioning process
        start_date = datetime.date.today()
        duration_relativedelta = relativedelta(
            months=alloc_local.estimated_project_duration)
        end_date = start_date + duration_relativedelta
        if not self.dry_run:
            self.stdout.write("  Updating start date ({0}) and end date "
                "({1})... ".format(str(start_date), str(end_date)), ending='')
            try:
                alloc_local.start_date = start_date
                alloc_local.end_date = end_date
                alloc_local.save(provisioning=True)
                self.write_ok()
            except Exception as e:
                self.write_failure("Exception raised trying to update "
                    "start_date and end_date for {0}: {1}".format(project_name,
                    str(e)))
                if not self.force:
                    return
        else:
            self.stdout.write("  Would have updated start date ({0}) and end "
                "date ({1}).".format(str(start_date), str(end_date)))

        ## Update the allocation object
        alloc_update_data = {}
        alloc_update_fields = ['approver_email', 'estimated_number_users',
            'estimated_project_duration', 'field_of_research_1',
            'field_of_research_2', 'funding_national_percent', 'funding_node',
            'ncris_support', 'nectar_support', 'usage_patterns', 'use_case',
            'start_date', 'end_date']
        for field in alloc_update_fields:
            alloc_update_data[field] = getattr(alloc_local, field)
        alloc_update_data.update(default_fields)
        # Include FOR percentages for NeCTAR reporting requirements
        if alloc_update_data['field_of_research_2']:
            alloc_update_data['for_percentage_1'] = 50
            alloc_update_data['for_percentage_2'] = 50
        else:
            alloc_update_data['for_percentage_1'] = 100
            alloc_update_data['for_percentage_2'] = 0
        if not self.dry_run:
            self.stdout.write("  Updating allocation fields on the NeCTAR "
                "database... ", ending='')
            try:
                alloc_nectar.update(**alloc_update_data)
                self.write_ok()
            except Exception as e:
                self.write_failed("Exception raised when attempting to update "
                    "allocation {0} in NeCTAR database: {1}".format(
                    project_name, str(e)))
                if not self.force:
                    return
        else:
            self.stdout.write("  The allocation would have been updated on the"
                " NeCTAR database with data={0}.".format(str(
                alloc_update_data)))

        # NOTE: Need to be able to find id/pk of each resource type based on
        # its quota_name, but list() does not seem to filter when passed a
        # quota_name kwarg, so they're mapped here
        # WARNING: This specifically excludes the `share` service_type because
        # both it and `volume` have a resource type called `gigabytes`
        nectar_resources = {}
        for resource in self.nectar.resources.list():
            service_type = getattr(resource, 'service_type')
            if service_type != 'share':
                quota_name = getattr(resource, 'quota_name')
                id = getattr(resource, 'id')
                nectar_resources[quota_name] = id

        # Generate a list of data dicts to pass to quotas.create()
        quotas_local = []
        for quota_group_local in alloc_local.quotas.all():
            for quota in quota_group_local.quota_set.all():
                quotas_local.append({
                    'allocation': alloc_nectar,
                    'resource': nectar_resources[quota.resource.quota_name],
                    'zone': quota_group_local.zone_id,
                    'quota': quota.quota,
                    'requested_quota': quota.requested_quota,
                })

        # NOTE: There is no update method for quotas, so delete and add

        # Delete old quotas in NeCTAR database
        if not project_is_new:
            for quota_nectar in alloc_nectar.quotas:
                id = getattr(quota_nectar, 'id')
                if not self.dry_run:
                    self.stdout.write("  Deleting old quota {0}... ".format(
                        str(quota_nectar)), ending='')
                    try:
                        self.nectar.quotas.delete(id)
                        self.write_ok()
                    except Exception as e:
                        self.write_failed("Exception raised when attempting to"
                            " delete quota {0} in NeCTAR database: {1}".format(
                            str(quota_nectar), str(e)))
                        if not self.force:
                            return
                else:
                    self.stdout.write("  Quota would have been deleted from "
                        "NeCTAR database: {0}.".format(str(quota_nectar)))

        # Create new quotas in NeCTAR database
        for quota_local in quotas_local:
            if not self.dry_run:
                self.stdout.write("  Creating quota with resource id="
                    "{resource} in zone='{zone}' (quota={quota}, requested="
                    "{requested_quota})... ".format(**quota_local), ending='')
                try:
                    self.nectar.quotas.create(**quota_local)
                    self.write_ok()
                except Exception as e:
                    self.write_failed("Exception raised when attempting to "
                        "create quota {0} in NeCTAR database: {1}".format(
                        str(quota_local), str(e)))
                    if not self.force:
                        return
            else:
                self.stdout.write("  Quota would have been created in NeCTAR "
                    "database with resource id={resource} in zone='{zone}' "
                    "(quota={quota}, requested={requested_quota}).".format(
                    **quota_local))

        # Set the NeCTAR allocation to approved
        if not self.dry_run:
            self.stdout.write("  Setting the NeCTAR allocation to approved... "
                "", ending='')
            try:
                alloc_nectar.approve()
                self.write_ok()
            except Exception as e:
                self.write_failed("Exception raised when attempting to approve"
                    " NeCTAR allocation {0}: {1}".format(project_name, str(e)))
                if not self.force:
                    return
        else:
            self.stdout.write("  NeCTAR allocation object would have been set "
                "to approved.")

        # The allocation is now being acted on by a different system, so lock
        # the local allocation object until provisioning is complete
        if not self.dry_run:
            self.stdout.write("  Locking local allocation object while NeCTAR "
                "provisions the project... ", ending='')
            try:
                alloc_local.lock()
                self.write_ok()
            except Exception as e:
                self.stdout.write(self.style.MIGRATE_FAILURE("FAILED"))
                LOG.error("Exception raised when attempting to lock allocation"
                    " {0}: {1}".format(project_name, str(e)))
        else:
            self.stdout.write("  Local allocation object would have been "
                "locked.")
        return

    def process_pending_approval(self, alloc_local):
        project_name = alloc_local.project_name
        self.stdout.write(self.style.MIGRATE_HEADING("\nChecking pending "
            "allocation approval with project_name {0}:".format(project_name)))

        project_is_new = self.project_is_new(alloc_local)

        # Retrieve the allocation in the NeCTAR allocations database. Match
        # on project_name
        self.stdout.write("  Retrieving allocation from NeCTAR database..."
            " ", ending='')
        try:
            alloc_nectar = self.nectar.allocations.get_current(
                project_name=project_name
            )
            # TODO: Verify this is the right allocation by confirming that
            # the contact_email field is the same
            self.write_ok()
        except AllocationDoesNotExist:
            self.write_failed("Attempted to retrieve allocation with "
                "project_name {0} from NeCTAR database, but failed."
                "".format(project_name))
            if not self.force:
                return
        except Exception as e:
            self.write_failed("Unexpected exception raised: " + str(e))
            if not self.force:
                return

        # Store latest NeCTAR allocation values locally
        provisioned = alloc_nectar.provisioned
        project_id = alloc_nectar.project_id
        # NOTE: For testing, uncomment the following
        # provisioned = True
        # project_id = 'myprojectid'

        # Check if allocation has been provisioned
        self.stdout.write("  Checking if allocation has been provisioned..."
            " ", ending='')
        if provisioned is True and project_id is not None:
            self.stdout.write(self.style.MIGRATE_SUCCESS("YES"))
        else:
            self.stdout.write(self.style.MIGRATE_FAILURE("NO"))
            self.stdout.write("  Skipping...")
            return

        # Update local allocation with new values
        # TODO: Is there a situation where the quota values will have changed
        # in the NeCTAR database, and we need to update our local allocation?
        if not self.dry_run:
            self.stdout.write("  Updating allocation in local database with "
                "provisioned status and project_id={0}... ".format(project_id),
                ending='')
            try:
                alloc_local.provisioned = provisioned
                alloc_local.project_id = project_id
                alloc_local.save(provisioning=True)
                self.write_ok()
            except Exception as e:
                self.write_failed("Exception raised when trying to update {0} "
                    "in local database with provisioned status and project_id:"
                    " {1}".format(project_name, str(e)))
                if not self.force:
                    return
        else:
            self.stdout.write("  Allocation in local database would have been "
                "updated with provisioned status and project_id={0}... "
                "".format(project_id))

        # Set template for email
        if project_is_new:
            template = 'rcallocation/email_provision_create.txt'
        else:
            template = 'rcallocation/email_provision_update.txt'

        # Send email
        if not self.dry_run:
            self.stdout.write("  Sending email notification to user... ",
                ending='')
            try:
                alloc_local.send_email_notification(template)
                self.write_ok()
            except Exception as e:
                self.write_failed("Exception raised when trying to send email "
                    "notification for {0}: {1}".format(project_name, str(e)))
                if not self.force:
                    return
        else:
            self.stdout.write("  Would have sent email notification to user.")

        # Unlock the local allocation object
        if not self.dry_run:
            self.stdout.write("  Unlocking the local allocation object... ",
                ending='')
            try:
                alloc_local.unlock()
                self.write_ok()
            except Exception as e:
                self.stdout.write(self.style.MIGRATE_FAILURE("FAILED"))
                LOG.error("Exception raised when attempting to unlock "
                    "allocation {0}: {1}".format(project_name, str(e)))
        else:
            self.stdout.write("  Local allocation object would have been "
                "unlocked.")
        return

    def project_is_new(self, alloc_local):
        # Based on the local allocation database, is this allocation
        # request new or an extension?
        provisioned_before = AllocationRequest.objects.filter(
            project_name=alloc_local.project_name, provisioned=True)
        if alloc_local.project_id is None and not provisioned_before:
            project_is_new = True
            self.stdout.write("  Allocation is new and has not been "
                "provisioned before...")
        else:
            project_is_new = False
            self.stdout.write("  Allocation is an existing one and has "
                "been provisioned before...")
        return project_is_new

    def write_ok(self, log_message=None):
        self.stdout.write(self.style.MIGRATE_SUCCESS("OK"))
        if log_message is not None:
            LOG.info(log_message)
        return

    def write_failed(self, log_message=None):
        self.stdout.write(self.style.MIGRATE_FAILURE("FAILED"))
        if not self.force:
            self.stdout.write("  Skipping...")
        if log_message is not None:
            LOG.error(log_message)
        return
