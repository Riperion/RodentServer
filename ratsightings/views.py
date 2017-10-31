# Create your views here.
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter

from .models import RatSighting
from .serializers import RatSightingSerializer
from rest_framework import viewsets

class RatSightingDateRangeFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = RatSighting
        fields = ['date_created']

class RatSightingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = RatSighting.objects.all()
    serializer_class = RatSightingSerializer
    filter_class = RatSightingDateRangeFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)