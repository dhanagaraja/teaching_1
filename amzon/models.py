from django.db import models

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

	@classmethod
	def create_product(cls, name, price, description=""):
		return cls.objects.create(name=name, price=price, description=description)

	@classmethod
	def get_product(cls, pk):
		return cls.objects.get(pk=pk)

	def update_product(self, **kwargs):
		for key, value in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, value)
		self.save()
		return self

	def delete_product(self):
		pk = self.pk
		self.delete()
		return pk
