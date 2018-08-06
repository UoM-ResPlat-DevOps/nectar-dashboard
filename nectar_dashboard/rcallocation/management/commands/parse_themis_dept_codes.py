import os
import re
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from nectar_dashboard.rcallocation.models import AllocationRequest
from nectar_dashboard.rcallocation.requester_choices import DEPT_CHOICE

LOG = logging.getLogger('nectar_dashboard.rcallocation')


class Command(BaseCommand):
    help = """Converts Themis department codes into importable Python tuples.

    * Copy and paste each page of the department codes (i.e. Budg field in
      account strings) from Themis into text file (ensure each row is on a new
      line). The fields should end up tab-separated.
    * Run this command with --input=<raw text file>.
    * Add an optional --output argument if you wish to generate a file that can
      replace rcallocation/choices_dept.py.
    """

    def add_arguments(self, parser):
        parser.add_argument('-i', '--input',
            nargs=1,
            dest='input_file',
            help='Full path to the input text file (required).',
            required=True,
            type=str)
        parser.add_argument('-o', '--output',
            nargs=1,
            dest='output_file',
            help='Full path to an output Python file (optional).',
            default=False)

    def handle(self, *args, **options):
        LOG.debug("Options passed to command '{0}': {1}".format(
            __name__.split('.')[-1], str(options)))

        # Exclude departments that include these substrings
        exclude = [
            'HISTORICAL',
            '(Central Use Only)'
        ]

        # Parse text file and generate list of departments
        departments = []
        try:
            with open(options['input_file'][0]) as f:
                for line in f:
                    search = re.search(r'(\d{4}?)\t(.*?)\t', line)
                    if search is not None:
                        if not any(word in search.group() for word in exclude):
                            departments.append((
                                search.group(1),
                                search.group(1) + " - " + search.group(2),
                            ))
        except Exception as e:
            raise CommandError("Failed to open input file. " + str(e))

        # Output list of departments as a tuple, if output file specified
        if options['output_file']:
            try:
                with open(options['output_file'][0], 'w') as f:
                    f.write('DEPT_CHOICE = (\n')
                    for dept in departments:
                        f.write('    {0},\n'.format(repr(dept)))
                    f.write(')\n')
            except Exception as e:
                raise CommandError("Failed to write to output file. " + str(e))

        # Generate summary of potential changes (additions and deletions)
        current_depts = list(DEPT_CHOICE)
        additions = [x for x in departments if x not in set(current_depts)]
        deletions = [x for x in current_depts if x not in set(departments)]

        changes = []
        for dept in additions:
            changes.append([dept[0], 1, dept[1]])
        for dept in deletions:
            changes.append([dept[0], 0, dept[1]])
        ordered_changes = sorted(changes, key=lambda x: (x[0], x[1]))

        self.stdout.write(self.style.MIGRATE_HEADING(
            '\nChanges from current DEPT_CHOICE:'))
        for dept in ordered_changes:
            if dept[1] == 0:
                self.stdout.write(self.style.MIGRATE_FAILURE('  - ' + dept[2]))
            if dept[1] == 1:
                self.stdout.write(self.style.MIGRATE_SUCCESS('  + ' + dept[2]))

        # Generate summary of allocation requests affected by the changes
        deletions_dict = dict(deletions)
        deletions_dict_keys = deletions_dict.keys()

        self.stdout.write(self.style.MIGRATE_HEADING(
            '\nAffected allocation requests:'))
        none_affected = True
        for ar in AllocationRequest.objects.filter(parent_request=None):
            dept = ar.investigators.all()[0].dept
            if dept in deletions_dict_keys:
                self.stdout.write(self.style.MIGRATE_FAILURE(
                    '  * {0} has ChiefInvestigator.dept {1}'.format(
                    ar.project_name, deletions_dict[dept])
                ))
                none_affected = False

        if none_affected:
            self.stdout.write(self.style.MIGRATE_SUCCESS(
                '  * No allocation requests affected.'))
