from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RatSighting(models.Model):
    owner = models.ForeignKey(User, related_name='ratsightings', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    location_type = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=100)
    borough = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return "%s, %s, %s %d" % (self.address, self.borough, self.city, self.zip_code)

    class Meta:
        ordering = ('date_created',)