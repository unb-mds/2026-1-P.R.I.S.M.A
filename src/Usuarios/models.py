from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	processos_legislativos = models.ManyToManyField(
		'Processos.ProcessoLegislativo',
		related_name='users',
		blank=True,
	)
