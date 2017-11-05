from rest_framework import fields
from rest_framework import serializers
from .models import RatSighting

class RatSightingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RatSighting
        fields = ('id', 'owner', 'date_created', 'location_type', 'zip_code', 'address', 'city', 'borough', 'latitude', 'longitude')

class RatSightingStatsQuerySerializer(serializers.Serializer):
    from_year = fields.IntegerField(min_value=1900, max_value=2100)
    from_month = fields.IntegerField(min_value=1, max_value=12)

    to_year = fields.IntegerField(min_value=1900, max_value=2100)
    to_month = fields.IntegerField(min_value=1, max_value=12)