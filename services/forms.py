from django import forms

from users.models import Company
from .models import Service, RequestService


class CreateNewService(forms.ModelForm):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)
    
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_hour', 'field']

    def __init__(self, *args, choices=None, ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields['field'].choices = choices
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'

class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestService
        fields = ['address', 'hours']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'hours': forms.NumberInput(attrs={'placeholder': 'Number of hours', 'min': 1})
        }

    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        
        print(f"Debug: Entered hours = {hours}")  # Debugging line

        if hours is None:
            raise forms.ValidationError("This field is required.")

        try:
            hours = int(hours)  # Ensure it's treated as an integer
        except ValueError:
            raise forms.ValidationError("Please enter a valid number.")

        if hours < 1:
            raise forms.ValidationError("Number of hours must be at least 1.")

        return hours  # Ensure it's returned properly
