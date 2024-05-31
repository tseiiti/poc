from django.db import models

class Product(models.Model):
	code = models.CharField(max_length = 10)
	description = models.CharField(max_length = 255)
	color = models.CharField(max_length = 50, null=True)
	size = models.CharField(max_length = 10, null=True)
	quantity = models.IntegerField()
	unit_price = models.FloatField()

	def __str__(self):
		return self.description