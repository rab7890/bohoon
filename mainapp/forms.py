from django import forms

from mainapp.models import Member


class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == "import_date" or field_name == "export_date" or field_name == "birth_date" or field_name == "birth_date":
                field.widget.attrs['type'] = "date"
                field.widget.input_type = "date"
        self.fields['group_type'].initial = "1"

    def clean(self):
        cleaned_data = super().clean()
        pass

    class Meta:
        model = Member
        exclude = ['is_deleted', 'deleted_date']
        widgets = {
            'import_date': forms.DateInput
        }
        labels = {
            'name': '이름'
        }