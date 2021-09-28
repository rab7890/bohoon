from django import forms
from django.db.models import fields
from django.forms.widgets import PasswordInput, EmailInput
from django.contrib.auth.forms import AuthenticationForm
from mainapp.models import Member




class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            field.widget.attrs['autocomplete'] = "off"
            if field_name == "import_date" or field_name == "export_date" or field_name == "birth_date" or field_name == "birth_date":
                field.widget.attrs['max'] = "9999-12-31"
                field.widget.input_type = "date"
                self.fields['group_type'].initial = "1"
            if field_name == "address":
                field.widget.attrs['rows'] = "2"
            if field_name == "memo":
                field.widget.attrs['rows'] = "2"
            
          
                

    def clean(self):
        cleaned_data = super().clean()
        pass

    class Meta:
        model = Member
        fields= '__all__'
       
        




class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            if field_name == "username":
                field.widget.attrs['placeholder'] = "아이디 ( I D )"
            if field_name == "password":
                field.widget.attrs['placeholder'] = "패스워드 ( PASSWORD )"
               
    

    def clean(self):
        cleaned_data = super().clean()
        pass



        
     