from django.contrib.auth.models import User, Group
from ratsightings.models import RatSighting
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ratsightings = serializers.PrimaryKeyRelatedField(many=True, queryset=RatSighting.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'ratsightings')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')