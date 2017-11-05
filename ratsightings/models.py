from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class RatSighting(models.Model):
    owner = models.ForeignKey(User, related_name='ratsightings', on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=date.today, null=False)
    location_type = models.CharField(max_length=100, null=False)
    zip_code = models.IntegerField(null=False)
    address = models.TextField(max_length=500, null=False)
    city = models.CharField(max_length=100, null=False)
    borough = models.CharField(max_length=100, null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)

    def __str__(self):
        return "%s, %s, %s %d" % (self.address, self.borough, self.city, self.zip_code)

    class Meta:
        ordering = ('-date_created',)