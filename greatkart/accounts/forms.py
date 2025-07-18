from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password','class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email','phon_number' ,'password']

    def clean(self):
        cleaned_data= super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
        



    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'
            self.fields[fields].widget.attrs['placeholder'] = fields.replace('_', ' ').title()



