from nectar_dashboard.rcallocation.forms import (AllocationAmendRequestForm,
                                         AllocationRequestForm)
from django.forms import TextInput
import datetime

class UserAllocationRequestForm(AllocationRequestForm):
    next_status = 'E'

    class Meta(AllocationRequestForm.Meta):
        exclude = ('project_id',
                   'status_explanation',) + AllocationRequestForm.Meta.exclude

    def __init__(self, **kwargs):
        super(UserAllocationRequestForm, self).__init__(**kwargs)
        self.instance.status = self.next_status


class UserAllocationRequestAmendForm(AllocationAmendRequestForm):
    next_status = 'X'

    class Meta(AllocationAmendRequestForm.Meta):
        exclude = ('project_id',
                   'funding_national_percent', 'funding_node',
                   'status_explanation', 'convert_project_trial'
                   ) + AllocationAmendRequestForm.Meta.exclude

        widgets = {
            'start_date': TextInput(attrs={'class': 'datepicker col-md-12',
                                           'style': 'border-radius:0;'}),
        }

    readonly = ('project_name', 'project_description', 'contact_email',)

    def __init__(self, **kwargs):
        instance = kwargs['instance']
        initial = kwargs['initial']
        initial['start_date'] = datetime.date.today
        super(UserAllocationRequestAmendForm, self).__init__(**kwargs)
        self.instance.status = self.next_status
        self.fields['start_date'].label = 'Extension start date'
        self.fields['estimated_project_duration'].label = \
            'Estimated extension duration'
