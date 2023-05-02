from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class usuario(models.Model):
	dni = models.CharField('DNI', max_length=9, validators=[MinLengthValidator(9)])
	name = models.CharField('Nombre', max_length=50)
	firstSurname = models.CharField('Primer Apellido', max_length=70)
	secondSurname = models.CharField('Segundo Apellido', max_length=70)
	text = models.TextField('Texto', max_length=512)
	pdf = models.CharField('PDF', max_length=50, blank=True)

	def __str__(self):
		return str(self.id) + ' ' + self.dni + ' ' + self.name + ' ' + self.firstSurname + ' ' + self.secondSurname