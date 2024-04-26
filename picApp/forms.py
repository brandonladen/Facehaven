from django import forms
from .models import MissingChild, FoundPerson
import datetime, re

class MissingChildForm(forms.ModelForm):
    class Meta:
        model = MissingChild
        fields = ['name', 'age', 'gender', 'image', 'date_missing', 'place_of_birth', 'last_seen', 'guardian_name', 'guardian_contact']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'date_missing': forms.DateInput(attrs={'type': 'date', 'class':'form-control right'}),
            'place_of_birth': forms.TextInput(attrs={'class':'form-control'}),
            'last_seen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place last seen'}),
            'guardian_name': forms.TextInput(attrs={'class':'form-control'}),
            'guardian_contact': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MissingChildForm, self).__init__(*args, **kwargs)
        
        # Set required attribute for specific fields
        self.fields['image'].required = True
        self.fields['gender'].required = True
        self.fields['last_seen'].required = True
        # self.fields['date_missing'].required = True
        self.fields['date_missing'].widget.attrs['max'] = str(datetime.date.today())

        
        # Set required attribute for non-mandatory fields to False
        self.fields['name'].required = False
        self.fields['age'].required = False
        self.fields['place_of_birth'].required = False
        self.fields['guardian_name'].required = False
        # self.fields['guardian_contact'].required = False
        self.fields['guardian_contact'].initial = '+254'

    # Add additional validation if needed
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_samaritan_contact(self):
        contact = self.cleaned_data['guardian_contact']
        # Regular expression to match Kenyan phone numbers with or without the country code
        phone_regex = re.compile(r'^(\+254)?[0-9]{9}$')
        if not phone_regex.match(contact):
            raise forms.ValidationError(
                "Please enter a valid Kenyan phone number.",
                code='invalid_phone_number'
            )
        return contact
    
    
class FoundPersonForm(forms.ModelForm):
    class Meta:
        model = FoundPerson
        fields = ['name', 'image', 'gender', 'date_found', 'time_found', 'place_found', 'samaritan_name', 'samaritan_contact']
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control left'}),
            'date_found': forms.DateInput(attrs={'type': 'date', 'class':'form-control right'}),
            'time_found': forms.TimeInput(attrs={'type': 'time','class':'form-control left'}),
            'image': forms.FileInput(attrs={'class':'form-control right'}),
            'gender': forms.Select(attrs={'class':'form-control left'}),
            'place_found': forms.TextInput(attrs={'class':'form-control right'}),
            'samaritan_name': forms.TextInput(attrs={'class':'form-control left'}),
            'samaritan_contact': forms.TextInput(attrs={'class':'form-control right'}),
        }

    def __init__(self, *args, **kwargs):
        super(FoundPersonForm, self).__init__(*args, **kwargs)
        
        # Set required attribute for specific fields
        self.fields['image'].required = True
        self.fields['gender'].required = True
        self.fields['place_found'].required = True
        self.fields['date_found'].required = True
        self.fields['time_found'].required = True
        
        # Set required attribute for non-mandatory fields to False
        self.fields['name'].required = False
        self.fields['samaritan_name'].required = False
        # self.fields['samaritan_contact'].required = False
        self.fields['samaritan_contact'].initial = '+254'
        
        self.fields['date_found'].widget.attrs['max'] = str(datetime.date.today())


    # Add additional validation if needed
    def clean(self):
        cleaned_data = super().clean()        
        return cleaned_data
    
    def clean_samaritan_contact(self):
        contact = self.cleaned_data['samaritan_contact']
        # Regular expression to match Kenyan phone numbers with or without the country code
        phone_regex = re.compile(r'^(\+254)?[0-9]{9}$')
        if not phone_regex.match(contact):
            raise forms.ValidationError(
                "Please enter a valid Kenyan phone number.",
                code='invalid_phone_number'
            )
        return contact

