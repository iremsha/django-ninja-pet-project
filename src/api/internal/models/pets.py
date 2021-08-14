import uuid

from django.db import models


class PetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    birth_date = models.DateField(verbose_name='Дата рождения')
    name = models.CharField(max_length=255, verbose_name='Кличка')
