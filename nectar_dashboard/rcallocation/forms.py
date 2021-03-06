from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.forms import ModelForm, ValidationError
from django.forms import TextInput, Select, CharField, Textarea, HiddenInput
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.safestring import mark_safe

from nectar_dashboard.rcallocation.models import AllocationRequest, Quota, \
    ChiefInvestigator, Institution, Publication, Grant, QuotaGroup
from nectar_dashboard.rcallocation.utils import *


class BaseAllocationForm(ModelForm):
    error_css_class = 'has-error'

    class Meta:
        model = AllocationRequest
        exclude = ('status', 'created_by', 'submit_date', 'approver_email',
                   'modified_time', 'parent_request',
                   'funding_national_percent', 'funding_node', 'provisioned',
                   'project_id', 'notes', 'allocation_home', 'for_percentage_1',
                   'for_percentage_2', 'field_of_research_3',
                   'for_percentage_3',)

        widgets = {
            'start_date': TextInput(attrs={'class': 'datepicker2 col-md-12'}),
            'convert_trial_project': Select(
                attrs={'class': 'col-md-6'},
                choices=[
                    (False, 'No, start with a blank project.'),
                    (True, 'Yes, move resources from my pt- project to '
                           'this new project.'),
                ]),
        }

    readonly = ('contact_email',)
    __readonly_values = {}

    def __init__(self, **kwargs):
        super(BaseAllocationForm, self).__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                'form-control ' + field.widget.attrs.get('class', ''))
        # Make users reaccept terms if they edit/amend/extend their request
        self.initial['accepted_terms'] = ''

        # For readonly fields
        for field in self.readonly:
            # Store their original value
            self.__readonly_values[field] = self.initial[field]
            # Add readonly attribute to widget
            self.fields[field].widget.attrs.update({
                'readonly': 'readonly'
            })

        # TODO: Figure out a more correct way to set this?
        try:
            self.__locked = self.initial['locked']
        except KeyError:
            self.__locked = False

    def visible_fields(self):
        return [field for field in self
                if (not field.is_hidden)]

    def _clean_form(self):
        try:
            self.cleaned_data = self.clean()
        except ValidationError as e:
            self._errors[NON_FIELD_ERRORS] = self.error_class([e.message])

    def is_locked(self):
        return self.__locked

    def clean_project_name(self):
        data = self.cleaned_data['project_name']
        if data.startswith('pt-'):
            raise ValidationError("Projects can not start with pt-")

        return data

    def clean(self):
        cleaned_data = super(BaseAllocationForm, self).clean()

        if self.__locked:
            raise ValidationError("")

        for field in self.readonly:
            if cleaned_data.get(field) != self.__readonly_values[field]:
                self.add_error(field, "This field is read-only and must be set"
                    " to {0}.".format(self.__readonly_values[field]))

        return cleaned_data


class AllocationRequestForm(BaseAllocationForm):
    prefix = get_project_prefix()
    regex = ('^' + prefix + '[a-zA-Z][-_a-zA-Z0-9]{1,' + str(31-len(prefix))
        + '}$')
    project_name = CharField(
        validators=[RegexValidator(
            regex=regex,
            message='Letters, numbers, underscores and hyphens only. 32 '
                    'characters maximum. Must start with {prefix} and have at '
                    'least 2 characters.'.format(prefix=prefix)
            )],
        max_length=32,
        label='Project identifier',
        required=True,
        initial=prefix,
        help_text='A short name used to identify your project.<br>'
                  'Letters, numbers, underscores and hyphens only.<br>'
                  'Must be less than 32 characters.',
        widget=TextInput(attrs={'autofocus': 'autofocus'}))

    def clean(self):
        cleaned_data = super(AllocationRequestForm, self).clean()
        if 'project_name' in self._errors:
            return cleaned_data

        allocations = (AllocationRequest.objects
                       .filter(project_name=cleaned_data['project_name'],
                               parent_request_id=None))
        if self.instance:
            allocations = allocations.exclude(pk=self.instance.pk)

        if allocations:
            self._errors["project_name"] = \
                [mark_safe(
                    'That project identifier already exists. If your '
                    'allocation has been approved already, please go'
                    ' <a href="%s">here</a> '
                    'to amend it. Otherwise, choose a different identifier.'
                    % reverse('horizon:allocation:user_requests:index'))]
            del cleaned_data["project_name"]

        return cleaned_data


class AllocationAmendRequestForm(BaseAllocationForm):
    class Meta(BaseAllocationForm.Meta):
        pass


class BaseQuotaForm(ModelForm):
    error_css_class = 'has-error'

    class Meta:
        model = Quota
        fields = '__all__'

        widgets = {
            'resource': HiddenInput(),
        }


class QuotaForm(BaseQuotaForm):
    class Meta(BaseQuotaForm.Meta):
        model = Quota
        exclude = ('quota',)

    def __init__(self, **kwargs):
        super(QuotaForm, self).__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + 'form-control')
        self.fields['group'].required = False


class BaseQuotaGroupForm(forms.ModelForm):

    error_css_class = 'has-error'

    enabled = forms.BooleanField(required=False, widget=forms.HiddenInput(
        attrs={'class': 'quota-group-enabled'}))

    def __init__(self, **kwargs):
        self.service_type = kwargs.pop('service_type')
        super(BaseQuotaGroupForm, self).__init__(**kwargs)

    class Meta:
        model = QuotaGroup
        exclude = ('allocation',)


class QuotaGroupForm(BaseQuotaGroupForm):

    def __init__(self, **kwargs):
        super(QuotaGroupForm, self).__init__(**kwargs)
        self.fields['service_type'].widget = forms.HiddenInput()
        self.fields['service_type'].initial = self.service_type
        self.fields['zone'].required = False
        self.fields['zone'].queryset = self.service_type.zones
        if len(self.service_type.zones.all()) == 1:
            self.fields['zone'].widget = forms.HiddenInput()
            zone_initial = self.service_type.zones.all()[0].name
            self.fields['zone'].initial = zone_initial
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + ' form-control')

    def clean(self):
        cleaned_data = super(QuotaGroupForm, self).clean()
        enabled = cleaned_data.get('enabled')
        zone = cleaned_data.get('zone')
        if enabled and not zone:
            raise forms.ValidationError("Please specify a zone")


# Base ModelForm
class NectarBaseModelForm(ModelForm):
    error_css_class = 'has-error'

    class Meta:
        exclude = ('allocation_request',)


# ChiefInvestigatorForm
class ChiefInvestigatorForm(NectarBaseModelForm):
    class Meta(NectarBaseModelForm.Meta):
        model = ChiefInvestigator

    def __init__(self, **kwargs):
        super(ChiefInvestigatorForm, self).__init__(**kwargs)
        # make sure the empty is not permitted
        self.empty_permitted = False
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + 'form-control')


class InstitutionForm(NectarBaseModelForm):
    class Meta(NectarBaseModelForm.Meta):
        model = Institution

    def __init__(self, **kwargs):
        super(InstitutionForm, self).__init__(**kwargs)
        # make sure the empty is not permitted
        self.empty_permitted = False
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + 'form-control')


class PublicationForm(NectarBaseModelForm):
    class Meta(NectarBaseModelForm.Meta):
        model = Publication

    def __init__(self, **kwargs):
        super(PublicationForm, self).__init__(**kwargs)
        # make sure the empty is not permitted
        self.empty_permitted = False
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + 'form-control')


class GrantForm(NectarBaseModelForm):
    class Meta(NectarBaseModelForm.Meta):
        model = Grant

    def __init__(self, **kwargs):
        super(GrantForm, self).__init__(**kwargs)
        # make sure the empty is not permitted
        self.empty_permitted = False
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                field.widget.attrs.get('class', '') + 'form-control')
