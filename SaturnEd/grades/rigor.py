from django import forms

Levels = [
   ("Regular", "Regular"),
   ("Honors", "Honors"),
   ("AP", "AP"),
]

class RigorForm(forms.Form):
   level = forms.MultipleChoiceField(
       required=True,
       widget=forms.SelectMultiple,
       choices=Levels,
   )
   class_name = forms.CharField(max_length=100, required=True)
   grade = forms.IntegerField(required=True)

   def clean(self):
       cleaned_data = super().clean()
       levels = cleaned_data.get('level', [])
    #    if "Keanu Reeves" in singers and "Scarlett Johanson" in singers:
    #        msg = "Scarlett Johanson never acted with Keanu Reeves"
    #        raise forms.ValidationError(msg)
       return cleaned_data
