from django import forms
import json


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': 'multiple'}))

    def clean_file(self):
        json_array_str = self.cleaned_data['file'].read().decode('utf-8')

        try:
            json.loads(json_array_str)
            return json_array_str
        except:
            raise forms.ValidationError('Not serializable to JSON!')
