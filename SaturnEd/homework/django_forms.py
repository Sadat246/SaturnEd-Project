from django import forms

class DjangoForm(forms.Form):
   hw_class = forms.CharField(max_length=100, required=True)
   hw_name = forms.CharField(max_length=100, required=True)
   hw_date = forms.CharField(max_length=100, required=True)

#   def clean(self):
#       cleaned_data = super().clean()
#       actors = cleaned_data.get('actors', [])
#       if "Keanu Reeves" in actors and "Scarlett Johanson" in actors:
#           msg = "Scarlett Johanson never acted with Keanu Reeves"
#           raise forms.ValidationError(msg)
#       return cleaned_data

