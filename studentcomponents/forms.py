from django import forms
from django.forms import ModelForm
from .models import StudentDetail, PaymentPaidRecord


class DateInput(forms.DateInput):
    input_type = 'date'


class PaymentForm(ModelForm):
    class Meta:
        model = PaymentPaidRecord
        fields = '__all__'
        widgets = {
            'fees_paid_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment'].empty_label = 'Select Student'

