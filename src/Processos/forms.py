from django import forms
from .models import AnotacaoPrivada
from .models import Marcador

class AnotacaoPrivadaForm(forms.ModelForm):
    class Meta:
        model = AnotacaoPrivada
        fields = ["texto_nota"]
        widgets = {
            "texto_nota": forms.Textarea(attrs={"rows": 4, "placeholder": "Escreva sua nota..."})
        }

class MarcadorForm(forms.ModelForm):
    class Meta:
        model = Marcador
        fields = ["nome_tag", "cor"]