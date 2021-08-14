from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class TogglRequestForm(forms.Form):
    employee_id = forms.UUIDField()
    month = forms.IntegerField()
    year = forms.IntegerField()


class WorkSpaceIDForm(forms.Form):
    toggl_workspace_id = forms.CharField()


class TogglDataForm(forms.Form):
    toggl_email = forms.CharField()
    toggl_workspace_ids = SimpleArrayField(forms.CharField(max_length=100))
    toggl_token = forms.CharField()
