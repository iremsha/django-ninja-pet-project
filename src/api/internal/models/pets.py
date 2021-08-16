from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Кличка')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
