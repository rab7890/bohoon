from django import forms

from mainapp.models import Member


class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'a'

    def clean(self):
        cleaned_data = super().clean()
        pass

    class Meta:
        model = Member
        fields = '__all__'