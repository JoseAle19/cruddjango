from django import forms
from .models import User
# Libreria de bootstrap
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class UserForm(forms.ModelForm):
     
     password = forms.CharField(widget=forms.PasswordInput)
     login = forms.EmailField(widget=forms.EmailInput)
     date_from = forms.DateTimeField(widget=DateTimePickerInput())
     date_to = forms.DateTimeField(widget=DateTimePickerInput())
     class Meta:
        model = User
        fields = ['username', 'login', 'password', 'date_from', 'date_to', 'active_account']
    
     def clean_username(self):
         username = self.cleaned_data['username']
         query = User.objects.filter(username=username).query
         print(f"Consulta SQL: {query}")
         if User.objects.filter(username=username).exists():
             print("El usuario ya existe")
             raise forms.ValidationError('Este nombre de usuario ya está en uso.')
         return username
     
     def clean_email(self):
        email = self.cleaned_data['email']
        query = User.objects.filter(email=email).query
        print(f"Consulta SQL: {query}")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email