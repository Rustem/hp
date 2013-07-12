from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _


class TaskForm(forms.Form):

    descr = forms.CharField(required=True)
    dd = forms.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super(TaskForm, self).__init__(*args, **kwargs)

    def clean_dd(self):
        due_date = self.cleaned_data["dd"]
        now = datetime.datetime.utcnow()
        print now, due_date
        if now >= due_date:
            raise forms.ValidationError(_(
                "Deadline date must be later than creation date."))
        return due_date
