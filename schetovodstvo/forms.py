from django import forms
from .models import vedomost

class UploadFileForm(forms.Form):
    file = forms.FileField()

class criterii_filtar(forms.Form):
    DOCUMENT_CHOICES = [
        ('',''),
        ('фактура','фактура'),
        ('отчет за продажбите','отчет за продажбите'),
        ('ведомост за заплати','ведомост за заплати'),
        ('банково извлечение', 'банково извлечение')
        ]

    crit1=forms.CharField(required=False,label='Търсене в описание')
    crit2=forms.CharField(required=False,label='Проверка на сметка Дт-Кт')

    crit3=forms.ChoiceField(required=False,
                            label='Търсене по вид документ',
                            choices=DOCUMENT_CHOICES,
                            widget=forms.Select(attrs={'class': 'form-select'})
                            )
    crit4=forms.CharField(required=False,label='Търсене по месец - 202501')
class vedomost_form(forms.ModelForm):
    class Meta:
        model = vedomost
        fields = ['first_f','doc','date','firma','opisanie', 'suma', 'debit', 'credit']
        widgets = { 'first_f': forms.DateInput(attrs={'size': 8}),
                    'opisanie': forms.TextInput(attrs={'size': 40}),
                   'debit': forms.NumberInput(attrs={'size': 5}),
                   'credit': forms.NumberInput(attrs={'size': 5}),
                   'date': forms.DateInput(attrs={'size': 8}),


                   }
