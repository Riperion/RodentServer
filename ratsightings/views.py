# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.urls import reverse_lazy
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from django.utils import timezone
from django_filters.views import FilterView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import RatSighting
from django.contrib.auth.models import User
from .serializers import RatSightingSerializer, RatSightingStatsQuerySerializer
from rest_framework import viewsets
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class RatSightingList(LoginRequiredMixin, ListView):
    model = RatSighting
    paginate_by = 50

class UserProfile(LoginRequiredMixin, ListView):
    model = RatSighting
    paginate_by = 50
    template_name = 'ratsightings/profile.html'

    def get_queryset(self):
        username = self.kwargs.get("username", None)
        user = self.request.user

        if username is not None:
            user = get_object_or_404(User, username=username)

        return RatSighting.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)

        username = self.kwargs.get("username", None)
        user = self.request.user

        if username is not None:
            user = get_object_or_404(User, username=username)

        context['user'] = user

        return context

class RatSightingDetail(LoginRequiredMixin, DetailView):
    model = RatSighting

class RatSightingCreate(LoginRequiredMixin, CreateView):
    model = RatSighting
    template_name_suffix = "_create_form"
    fields = ('location_type', 'zip_code', 'address', 'city', 'borough', 'latitude', 'longitude')
    success_url = reverse_lazy("ratsighting-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.date_created = timezone.now()

        return super(RatSightingCreate, self).form_valid(form)

class RatSightingDateRangeFilter(FilterSet):
    date_created = DateFromToRangeFilter()

    class Meta:
        model = RatSighting
        fields = ['date_created']

class StatsView(LoginRequiredMixin, ListView):
    model = RatSighting
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        context['histogram'] = RatSighting.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(count=Count('id')).values('month', 'count').order_by()
        return context

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
        # # Get the dates sent by the user
        # serializer = RatSightingStatsQuerySerializer(data=request.query_params)
        # if not serializer.is_valid():
        #     return Response(
        #         data=serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # data = serializer.data
        #
        # from_date = datetime.date(year=data["from_year"], month=data["from_month"], day=1)
        # to_date = datetime.date(year=data["to_year"], month=data["to_month"], day=1)
        #
        # if from_date >= to_date:
        #     return Response(
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        #
        # # Get date frame tuples for each month involved in date range
        # ranges = []
        #
        # current = from_date
        # while current < to_date:
        #     next_date = from_date + relativedelta(months=1)
        #     ranges.append((current, next_date))
        #
        #     current = next_date
        #
        #
        # # Map the results into a dictionary
        # results = {}
        #
        # for range_from, range_to in ranges:
        #     query = RatSighting.objects.filter(date_created__gte=range_from, date_created__lt=range_to)
        #     results[range_from.strftime("%Y-%m")] = query.count()

        results = RatSighting.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(count=Count('id')).values('month', 'count').order_by()
        return Response(results)