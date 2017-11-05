# Create your views here.
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from dateutil.relativedelta import relativedelta

from .models import RatSighting
from .serializers import RatSightingSerializer, RatSightingStatsQuerySerializer
from rest_framework import viewsets

class RatSightingDateRangeFilter(FilterSet):
    date_created = DateFromToRangeFilter()

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

class RatSightingStatsViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
        # Get the dates sent by the user
        serializer = RatSightingStatsQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.object

        from_date = datetime.date(year=data.from_year, month=data.from_month, day=1)
        to_date = datetime.date(year=data.to_year, month=data.to_month, day=1)

        if from_date >= to_date:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get date frame tuples for each month involved in date range
        ranges = []

        current = from_date
        while current < to_date:
            next_date = from_date + relativedelta(months=1)
            ranges.append((current, next_date))

            current = next_date


        # Map the results into a dictionary
        results = {}

        for range_from, range_to in ranges:
            query = RatSighting.objects.filter(date_created__gte=range_from, date_created__lt=range_to)
            results[range_from.strftime("%Y-%m")] = query.count()

        return Response(results)