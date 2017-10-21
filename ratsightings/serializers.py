from rest_framework import serializers
from .models import RatSighting

class RatSightingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RatSighting
        fields = ('id', 'owner', 'date_created', 'location_type', 'zip_code', 'address', 'city', 'borough', 'latitude', 'longitude')