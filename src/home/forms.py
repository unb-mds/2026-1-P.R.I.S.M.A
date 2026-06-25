from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
        )

from .models import AnotacaoPrivada

class AnotacaoPrivadaForm(forms.ModelForm):
    class Meta:
        model = AnotacaoPrivada
        fields = ["texto_nota"]
        widgets = {
            "texto_nota": forms.Textarea(attrs={"rows": 4, "placeholder": "Escreva sua nota..."})
        }