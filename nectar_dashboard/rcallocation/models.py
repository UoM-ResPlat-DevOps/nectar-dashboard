# Models for the ResearchCloud Allocations portal
# Original: Tom Fifield <fifieldt@unimelb.edu.au> - 2011-10
# Modified by Martin Paulo
import datetime
from dateutil.relativedelta import relativedelta
import logging

from django.core.mail import EmailMessage
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from choices import ALLOC_HOME_CHOICE, DURATION_CHOICE, GRANT_TYPES, \
    REQUESTER_ROLE_CHOICE, USE_CATEGORY_CHOICE
from choices_dept import DEPT_CHOICE
from choices_for import FOR_CHOICES


LOG = logging.getLogger('rcallocation')


#############################################################################
#
# Requests are created by Users who wish to receive Allocations
#
#############################################################################


def _six_months_from_now():
    return datetime.date.today() + datetime.timedelta(
        days=30 * 6),


class AllocationRequest(models.Model):
    NEW = 'N'
    SUBMITTED = 'E'
    APPROVED = 'A'
    DECLINED = 'R'
    UPDATE_PENDING = 'X'
    UPDATE_DECLINED = 'J'
    LEGACY = 'L'
    LEGACY_APPROVED = 'M'
    LEGACY_REJECTED = 'O'
    DELETED = 'D'

    REQUEST_STATUS_CHOICES = (
        # Request created but nothing else
        # User can: Submit
        (NEW, 'New'),

        # Request has been emailed
        # Admin can: Approve, Reject, Edit
        # User can: Edit
        (SUBMITTED, 'Submitted'),

        # Admin has approved the request
        # Admin can: Provision, Edit
        # User can: Amend, Extend
        (APPROVED, 'Approved'),

        # Admin has rejected the request
        # User can: Edit, Submit
        (DECLINED, 'Declined'),

        # User has requested an extension
        # Admin can: Approve, Reject, Edit
        # User can: Edit
        (UPDATE_PENDING, 'Update requested'),

        # Admin has rejected an extension
        # User can: Edit, Extend
        (UPDATE_DECLINED, 'Update declined'),

        # Requests in above status can be viewed by both user
        # and admin at all times.

        # Not visible to users
        (LEGACY, 'Legacy submission'),

        # Allocation has been deleted
        (DELETED, 'Deleted'),

        # Avoid sending emails for legacy approvals/rejections.
        # Set to A/R during model save.
        (LEGACY_APPROVED, 'Legacy approved'),
        (LEGACY_REJECTED, 'Legacy rejected'),
    )
    parent_request = models.ForeignKey('AllocationRequest', null=True,
                                       blank=True)

    status = models.CharField(max_length=1, blank=False,
                              choices=REQUEST_STATUS_CHOICES,
                              default=NEW)

    status_explanation = models.TextField(
        null=True, blank=True,
        verbose_name="Reason",
        help_text="A brief explanation of the reason the request has been "
                  "sent back to the user for changes")

    created_by = models.CharField(null=False, blank=False, max_length=100)

    submit_date = models.DateField('Submission Date',
                                   default=datetime.date.today)
    modified_time = models.DateTimeField('Modified Date',
                                         default=datetime.datetime.utcnow)

    # The following fields (all before project_name) are no longer used,
    # but are kept for consistency

    convert_trial_project = models.BooleanField(
        'Convert trial project?',
        default=False,
        help_text='If selected, your existing trial project pt- will be '
                  'renamed so any resources inside it will become part of '
                  'this new allocation. A new trial project will be created '
                  'in its place.')

    allocation_home = models.CharField(
        "Allocation home location",
        choices=ALLOC_HOME_CHOICE,
        blank=False,
        null=False,
        default='uom',
        max_length=128,
        help_text="""You can provide a primary location where you expect to
                use most resources, effectively the main Nectar site for your
                allocation. Use of other locations is still possible.
                This can also indicate a specific arrangement with a
                Nectar site, for example where you obtain support, or if
                your institution is a supporting member of that site.
                Select unassigned if you have no preference.
                """
    )

    PERCENTAGE_CHOICES = (
        (0, '0%'),
        (10, '10%'),
        (20, '20%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (80, '80%'),
        (90, '90%'),
        (100, '100%'),
    )

    for_percentage_1 = models.IntegerField(
        choices=PERCENTAGE_CHOICES, default=100, blank=True,
        help_text="""The percentage""")

    for_percentage_2 = models.IntegerField(
        choices=PERCENTAGE_CHOICES, default=0, blank=True,
        help_text="""The percentage""")

    field_of_research_3 = models.CharField(
        "Third Field Of Research",
        choices=FOR_CHOICES,
        blank=True,
        null=True,
        max_length=6
    )

    for_percentage_3 = models.IntegerField(
        choices=PERCENTAGE_CHOICES, default=0, blank=True)

    funding_national_percent = models.IntegerField(
        'Nationally Funded Percentage [0..100]',
        default='0',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        error_messages={'min_value': 'The minimum percent is 0',
                        'max_value': 'The maximum percent is 100'},
        help_text="""Percentage funded under the National
                    Allocation Scheme.""")

    funding_node = models.CharField(
        "Node Funding Remainder (if applicable)",
        choices=ALLOC_HOME_CHOICE[1:],
        default='uom',
        blank=True,
        null=True,
        max_length=128,
        help_text="""You can choose the node that complements
                    the National Funding."""
    )

    # The ordering of the following fields are important, as it
    # governs the order they appear on the forms
    project_name = models.CharField(
        'Project identifier',
        max_length=64,
        blank=True,
        null=True,
        help_text='A short name used to identify your project.<br>'
                  'Must contain only letters and numbers.<br>'
                  '16 characters max.')

    project_description = models.CharField(
        'Project allocation title',
        max_length=200,
        help_text='A human-friendly descriptive name for your project.')

    start_date = models.DateField(
        'Start date',
        default=datetime.date.today,
        help_text="""The day on which you want your project allocation
            to go live. Format: YYYY-MM-DD.<br><br>Note that if the
            project is provisioned at a later date than your desired
            start date, the start date will be updated to the day of
            provisioning."""
    )

    end_date = models.DateField(
        'Estimated end date',
        editable=False,
        default=_six_months_from_now,
        help_text='The day on which your project will end.')

    estimated_project_duration = models.IntegerField(
        'Estimated project duration',
        choices=DURATION_CHOICE,
        blank=False,
        null=False,
        default=1,
        help_text="""Resources are approved for 12 months at most,
                    but projects can be extended once they have been
                    approved.""")

    requester_title = models.CharField(
        'Title',
        max_length=60,
        blank=False,
        null=True,
        help_text='Your title.'
    )

    requester_given_name = models.CharField(
        'Given name',
        max_length=255,
        blank=False,
        null=True,
        help_text='Your given name.'
    )

    requester_surname = models.CharField(
        'Surname',
        max_length=255,
        blank=False,
        null=True,
        help_text='Your surname.'
    )

    contact_email = models.EmailField(
        'Contact e-mail', blank=True,
        help_text="""Please verify that this e-mail address is current and
            accessible. It will be used to communicate with you about this
            allocation request.<br><br><strong>Note:</strong> <i>If this is not
            a valid email address you will not receive communications on any
            allocation request you make</i>. If invalid please submit a support
            ticket in ServiceNow (link provided in top navigation bar)."""
    )

    requester_phone = models.CharField(
        'Contact phone number',
        max_length=255,
        blank=False,
        null=True,
        help_text='Your preferred contact phone number.'
    )

    requester_role = models.CharField(
        'Your role',
        max_length=255,
        choices=REQUESTER_ROLE_CHOICE,
        blank=False,
        null=True,
        help_text="""Select the category that best fits your role in
            this project."""
    )

    requester_is_ci = models.CharField(
        'Are you the Chief Investigator?',
        max_length=255,
        help_text="""Please select 'Yes' if you are the Chief
            Investigator.<ul><li>For research projects this is the first
            investigator.</li><li>For higher degree research projects this is
            the primary supervisor.</li><li>For other activities this is the
            academic sponsor or head of the managing organisation unit.</li>
            </ul>""",
        choices=(
            ('yes', 'Yes'),
            ('no', 'No'),
        ),
        blank=False,
        null=True,
    )

    approver_email = models.EmailField('Approver email', blank=True)

    use_category = models.CharField(
        'Category of work',
        max_length=255,
        choices=USE_CATEGORY_CHOICE,
        blank=False,
        null=True,
        help_text='Select the category that this project is primarily for.')

    use_case = models.TextField(
        "Use case",
        max_length=4096,
        help_text="""Provide a very brief overview of your project, and how
                     you will use the cloud to support it.""")

    usage_patterns = models.TextField(
        "Instance, Object Storage and Volumes Storage Usage Patterns",
        max_length=1024, blank=True,
        help_text="""Will your project have many users and small data sets?
                     Or will it have large data sets with a small number of
                     users? Will your instances be long running or created
                     and deleted as needed? <br>
                     Your answers here will help validate the Instances,
                     Object Storage and Volume Storages is right for the
                     project.""")

    # TODO: Rename field
    geographic_requirements = models.TextField(
        max_length=1024,
        blank=True,
        verbose_name="Special requirements",
        help_text="""Describe any special requirements you need for your
                     project. For example geographical location,
                     high-memory nodes, or GPU enable nodes.""")

    project_id = models.CharField(max_length=36, blank=True, null=True)

    estimated_number_users = models.IntegerField(
        'Estimated number of users',
        default='1',
        validators=[MinValueValidator(1), ],
        error_messages={
            'min_value': 'The estimated number of users must be great than 0'},
        help_text="""Estimated number of users, researchers and collaborators
        to be supported by the project.""")

    use_other = models.TextField(
        'List other capabilities you use/intend to use with this project',
        max_length=1024,
        blank=True,
        help_text="""e.g. AWS, Google compute, Nectar, other NCRIS platforms,
            ..."""
    )

    field_of_research_1 = models.CharField(
        "First Field of Research",
        choices=FOR_CHOICES,
        blank=False,
        null=True,
        max_length=6,
        help_text="""Pick the primary Field of Research for this project."""
    )

    field_of_research_2 = models.CharField(
        "Second Field of Research",
        choices=FOR_CHOICES,
        blank=True,
        null=True,
        max_length=6,
        help_text="""Optional: Pick an additional Field of Research for this
            project."""
    )

    nectar_support = models.CharField(
        """List any ARDC (formerly ANDS, Nectar and RDS) funded projects
        supporting this request.""",
        help_text="""List the names of any ARDC funded projects.<br><br><strong>
            Note:</strong> On 1 July 2018 ANDS, Nectar and RDS combined to form
            the Australian Research Data Commons (ARDC).""",
        blank=True,
        max_length=255
    )

    ncris_support = models.CharField(
        'List any NCRIS capabilities supporting this request.',
        blank=True,
        max_length=255,
        help_text="""List the names of any NCRIS capabilities supporting this
            request."""
    )

    accepted_terms = models.CharField(
        """I have read and accepted the <a href="/terms" target="_blank">
            University of Melbourne - Terms and Conditions</a>""",
        help_text="""Users of The University of Melbourne Research Cloud must
                     read and accept the Terms and Conditions.""",
        max_length=255,
        choices=(
            ('yes', 'Yes'),
            ('no', 'No'),
        ),
        blank=False,
        null=True,
        validators=[RegexValidator(
            regex=r'^yes$',
            message="You must accept the Terms and Conditions."
        )],
    )

    provisioned = models.BooleanField(default=False)

    locked = models.BooleanField(default=False)

    notes = models.TextField(
        "Private notes for admins",
        null=True, blank=True,
        help_text="These notes are only visible to allocation admins")

    def get_absolute_url(self):
        return reverse('horizon:allocation:requests:allocation_view',
                       args=[str(self.id)])

    def set_status(self, status):
        status = status.upper()
        status_abbreviations = [abbr for abbr, full_name in
                                self.REQUEST_STATUS_CHOICES]
        if status not in status_abbreviations:
            raise Exception()

        self.status = status

    def lock(self):
        # TODO: Consider restricting this method to certain statuses e.g. 'A'
        if not self.locked:
            self.locked = True
            # TODO: Passing this kwarg and handling for it in save() is
            # currently a workaround until save() is refactored.
            kwargs = {'locking': True}
            self.save(**kwargs)
        else:
            LOG.debug("{0}.lock() called but object is already locked."
                "".format(__name__))
        return

    def unlock(self):
        if self.locked:
            self.locked = False
            # TODO: Passing this kwarg and handling for it in save() is
            # currently a workaround until save() is refactored.
            kwargs = {'locking': True}
            self.save(**kwargs)
        else:
            LOG.debug("{0}.unlock() called but object is already unlocked."
                "".format(__name__))
        return

    # TODO: How many of the below methods are actually used?

    def is_active(self):
        """
        Return True if the allocation has been approved, false otherwise.
        """
        return self.status.lower() == 'a'

    # NOTE: Not used.
    # TODO: I don't think this is correct? It returns is_active() which only
    # evaluates for 'a' (accepted), but not 'r' (rejected)
    def is_decided(self):
        """
        Return True if the allocation has either been accepted or
        rejected, false otherwise.
        """
        return self.is_active()

    def is_rejected(self):
        """
        Return True if the allocation has either been accepted or
        rejected, false otherwise.
        """
        return self.status.lower() in ('r', 'j')

    def is_requested(self):
        return self.status.lower() in ('e', 'n', 'l')

    def amendment_requested(self):
        """
        Return True if the user has requested an extention
        """
        return self.status.lower() in ('x', 'j')

    def is_archived(self):
        return self.parent_request is not None

    def can_be_amended(self):
        return self.is_active() and not self.is_archived() and not self.locked

    def can_be_extended(self):
        return self.can_be_amended() and not self.is_archived()

    def can_be_edited(self):
        return (not self.is_active() and not self.is_archived() and
            not self.locked)

    def can_admin_edit(self):
        return self.can_be_edited()

    def can_user_edit(self):
        return (self.status.lower() in ('e', 'r', 'n', 'l') and
            not self.is_archived() and not self.locked)

    def can_user_edit_amendment(self):
        return (self.amendment_requested() and not self.is_archived() and
            not self.locked)

    def can_be_rejected(self):
        return self.is_requested() and not self.is_archived()

    def can_be_approved(self):
        return self.is_requested() and not self.is_archived()

    def can_reject_change(self):
        return self.can_approve_change()

    def can_approve_change(self):
        return self.amendment_requested() and not self.is_archived()

    def send_email_notification(self, template_name):
        """Sends an email to the requester notifying them that their
        allocation has been processed.
        """

        email_kwargs = {}
        # Required arguments
        try:
            email_kwargs['from_email'] = settings.ALLOCATION_EMAIL_FROM
            email_kwargs['to'] = [self.contact_email]
        except:
            LOG.critical("")
            raise
        # Optional arguments
        for kwarg, setting in [('cc', 'ALLOCATION_EMAIL_RECIPIENTS',),
            ('bcc', 'ALLOCATION_EMAIL_BCC_RECIPIENTS',),
            ('reply_to', 'ALLOCATION_EMAIL_REPLY_TO',)]:
            try:
                email_kwargs[kwarg] = getattr(settings, setting)
            except:
                pass

        template = get_template(template_name)
        context = self.create_email_context()
        text = template.render(context)

        email_kwargs['subject'], delimiter, email_kwargs['body'] = (
            text.partition('\n\n'))

        email = EmailMessage(**email_kwargs)
        email.send()

    def create_email_context(self):
        context = {'request': self}
        context['quotas'] = self.get_quotas_sorted_list(self)
        try:
            alloc_old = AllocationRequest.objects.filter(
                project_name=self.project_name, provisioned=True)[1]
            context['quotas_old'] = self.get_quotas_sorted_list(alloc_old)
        except:
            context['quotas_old'] = []
        return Context(context)

    def get_quotas_sorted_list(self, alloc):
        quotas = []
        for quota_group in alloc.quotas.all():
            for quota in quota_group.quota_set.all():
                quotas.append({
                    'index': quota_group.service_type.index,
                    'service_type': quota_group.service_type.name,
                    'resource': quota.resource.name,
                    'unit': quota.resource.unit,
                    'zone': quota_group.zone.display_name,
                    'quota': quota.quota,
                    'requested_quota': quota.requested_quota,
                })
        quotas_sorted = sorted(quotas, key=lambda k: k['index'])
        return quotas_sorted

    def send_notifications(self):
        if self.status in [self.NEW, self.SUBMITTED, self.UPDATE_PENDING]:
            if self.status == self.NEW:
                template = 'rcallocation/email_alert_acknowledge.txt'
            else:
                template = 'rcallocation/email_alert.txt'
            self.send_email_notification(template)
            #NOTE:STATE CHANGE
            if self.status == self.NEW:
                # N is a special state showing that the
                # request has been created but no email has
                # been sent. Progress it once it's been sent.
                self.status = self.SUBMITTED
                self.save()
        elif self.is_rejected():
            template = 'rcallocation/email_alert_rejected.txt'
            self.send_email_notification(template)

    def save(self, *args, **kwargs):
        # TODO: Temp solution until refactoring
        if 'locking' in kwargs:
            del kwargs['locking']
            super(AllocationRequest, self).save(*args, **kwargs)
            return
        if not kwargs.get('provisioning'):
            if not self.is_archived():
                self.modified_time = datetime.datetime.utcnow()
        if self.status == self.LEGACY_APPROVED:
            self.status = self.APPROVED
        elif self.status == self.LEGACY_REJECTED:
            self.status = self.DECLINED
        if 'provisioning' in kwargs:
            del kwargs['provisioning']
        super(AllocationRequest, self).save(*args, **kwargs)

    # def get_all_fields(self):
    #     """
    #     Returns a list of all non None fields, each entry containing
    #     the fields label, field name, and value (if the display value
    #     exists it is preferred)
    #     """
    #     fields = []
    #     for f in self._meta.fields:
    #         if f.editable:
    #             field_name = f.name
    #
    #             # resolve picklists/choices, with get_xyz_display() function
    #             try:
    #                 get_choice = 'get_' + field_name + '_display'
    #                 if hasattr(self, get_choice):
    #                     value = getattr(self, get_choice)()
    #                 else:
    #                     value = getattr(self, field_name)
    #             except AttributeError:
    #                 value = None
    #
    #             # only display fields with values and skip some fields entirely
    #             if not (value is None or field_name in ('id', 'status')):
    #                 fields.append(
    #                     {
    #                         'label': f.verbose_name,
    #                         'name': field_name,
    #                         'value': value,
    #                     }
    #                 )
    #     return fields

    def __unicode__(self):
        return '"{0}" {1}'.format(self.project_name, self.contact_email)

    # New methods

    def submit(self):
        # IF NEW
        return True

    def amend(self):
        return True

    def approve(self):
        return True

    def reject(self):
        return True

    def provision(self):
        return True

    def expire(self):
        return True


class Zone(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    display_name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.display_name


class ServiceType(models.Model):
    catalog_name = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    zones = models.ManyToManyField(Zone)
    index = models.IntegerField(default=99)
    required = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=64)
    service_type = models.ForeignKey(ServiceType)
    quota_name = models.CharField(max_length=32)
    unit = models.CharField(max_length=32)
    requestable = models.BooleanField(default=True)
    help_text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def codename(self):
        return "%s.%s" % (self.service_type.catalog_name, self.quota_name)

    class Meta:
        unique_together = ('service_type', 'quota_name')


class QuotaGroup(models.Model):
    allocation = models.ForeignKey(AllocationRequest, related_name='quotas')
    zone = models.ForeignKey(Zone)
    service_type = models.ForeignKey(ServiceType)

    class Meta:
        unique_together = ("allocation", "zone", "service_type")

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.allocation.id,
                                    self.service_type, self.zone)


class Quota(models.Model):
    group = models.ForeignKey(QuotaGroup)
    resource = models.ForeignKey(Resource)
    requested_quota = models.PositiveIntegerField(
        'Requested quota',
        default='0')
    quota = models.PositiveIntegerField(
        "Allocated quota",
        default='0')

    class Meta:
        unique_together = ("group", "resource")

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.group.allocation.id,
                                    self.resource, self.group.zone)


class ChiefInvestigator(models.Model):
    allocation = models.ForeignKey(AllocationRequest,
                                   related_name='investigators')

    title = models.CharField(
        'Title',
        blank=False,
        max_length=60,
        help_text="""The chief investigator's title"""
    )

    given_name = models.CharField(
        'Given name',
        blank=False,
        max_length=200,
        help_text="""The chief investigator's given name"""
    )

    surname = models.CharField(
        'Surname',
        blank=False,
        max_length=200,
        help_text="""The chief investigator's surname"""
    )

    dept = models.CharField(
        'Department',
        max_length=255,
        choices=DEPT_CHOICE,
        blank=False,
        null=True,
        help_text="""Select the Chief Investigator's department.
                  <br><br>If you cannot find the appropriate department,
                  school or faculty listed here, please select "0000 -
                  University General".
                  """
    )

    email = models.EmailField(
        'Institutional email address',
        blank=False,
        help_text="""Chief Investigator's institutional email address."""
    )

    institution = models.CharField(
        'Institution',
        blank=True,
        max_length=200,
        default='',
        help_text="""The name of the institution or university of
                    the chief investigator including the schools,
                    faculty and/or department."""
    )

    additional_researchers = models.TextField(
        'Please list all other primary investigators, partner investigators '
        'and other research collaborators',
        blank=True,
        max_length=1000,
        default='',
        help_text="""Include full names, and the name of their Research
                     Institution, University or Organisation they
                     belong to.""")

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.title, self.given_name, self.surname)


class Institution(models.Model):
    name = models.CharField(
        'Collaborating institutions',
        max_length=200,
        default='The University of Melbourne',
        help_text="""List one or more Research Institutions and Universities
                     this project intends to collaborate with. <br>
                     If this project is just for you, write the name of the
                     your Reserarch Institution or University. <br>
                     If you are running a public web service, list the
                     Research Institutions and Universities that will benefit
                     the most."""
    )

    allocation = models.ForeignKey(AllocationRequest,
                                   related_name='institutions')

    class Meta:
        unique_together = ("allocation", "name")

    def __unicode__(self):
        return self.name


class Publication(models.Model):
    publication = models.CharField(
        'Publication/Output',
        max_length=512,
        help_text="""Please provide any traditional and non-traditional
                research outputs using a citation style text reference
                for each. eg. include article/title, journal/outlet, year,
                DOI/link if available.""")

    allocation = models.ForeignKey(AllocationRequest,
                                   related_name='publications')

    def __unicode__(self):
        return self.publication


class Grant(models.Model):
    grant_type = models.CharField(
        "Type",
        choices=GRANT_TYPES,
        blank=False,
        null=False,
        default='arc',
        max_length=128,
        help_text="""Choose the grant type from the dropdown options."""
    )

    funding_body_scheme = models.CharField(
        "Funding body and scheme",
        blank=False,
        max_length=255,
        help_text="""For example, ARC Discovery Project."""
    )

    grant_id = models.CharField(
        'Grant ID',
        blank=True,
        max_length=200,
        help_text="""Specify the grant id."""
    )

    first_year_funded = models.IntegerField(
        'First year funded',
        blank=False,
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1970), MaxValueValidator(3000)],
        error_messages={
            'min_value': 'Please input a year between 1970 ~ 3000',
            'max_value': 'Please input a year between 1970 ~ 3000'},
        help_text="""Specify the first year funded"""
    )

    last_year_funded = models.IntegerField(
        'Last year funded',
        blank=False,
        default=datetime.datetime.now().year + 1,
        validators=[MinValueValidator(1970), MaxValueValidator(3000)],
        error_messages={
            'min_value': 'Please input a year between 1970 ~ 3000',
            'max_value': 'Please input a year between 1970 ~ 3000'},
        help_text="""Specify the last year funded"""
    )

    total_funding = models.FloatField(
        'Total funding (AUD)',
        validators=[MinValueValidator(1)],
        help_text="""Total funding amount in AUD"""
    )

    allocation = models.ForeignKey(AllocationRequest, related_name='grants')

    class Meta:
        unique_together = ("allocation", "grant_type", "funding_body_scheme",
                           "grant_id", "first_year_funded", "total_funding")

    def __unicode__(self):
        return "Funding : {0} , total funding: {1}".format(self.funding_body,
                                                           self.total_funding)
