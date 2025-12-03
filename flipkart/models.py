from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class City(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.city

    @property
    def name(self):
        """Compatibility alias: return the city name for templates/code
        that expect a `name` attribute.
        """
        return self.city