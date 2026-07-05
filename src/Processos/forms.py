from django import forms
from .models import AnotacaoPrivada


class AnotacaoPrivadaForm(forms.ModelForm):
    class Meta:
        model = AnotacaoPrivada
        fields = ["texto_nota"]
        widgets = {
            "texto_nota": forms.Textarea(attrs={"rows": 4, "placeholder": "Escreva sua nota..."})
        }