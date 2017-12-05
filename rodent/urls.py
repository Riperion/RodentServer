from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django_filters.views import FilterView
from rest_framework import routers

from ratsightings.views import RatSightingViewSet, RatSightingStatsViewSet, RatSightingList, RatSightingCreate, RatSightingDetail, UserProfile, \
    StatsView
from .views import UserViewSet, GroupViewSet, signup

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'ratsightings', RatSightingViewSet)
router.register(r'stats', RatSightingStatsViewSet, base_name="Stats")

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    #url(r'^map/', ratsightings.views.map, name='map'),
    url(r'^ratsightings/$', RatSightingList.as_view(), name="ratsighting-list"),
    url(r'^ratsightings/add/$', RatSightingCreate.as_view(), name="ratsighting-add"),
    url(r'^ratsightings/(?P<pk>[0-9]+)/$', RatSightingDetail.as_view(), name="ratsighting-detail"),
    url(r'^api/', include(router.urls, namespace="rodent-api")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/', include('djoser.urls')),
    url(r'^api/auth/', include('djoser.urls.authtoken')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', UserProfile.as_view(), name="profile"),
    url(r'^accounts/profile/(?P<username>\w+)/$', UserProfile.as_view(), name='named-profile'),
    url(r'^accounts/register/$', signup, name="register"),
    url(r'^$', TemplateView.as_view(template_name="registration/registration_complete.html"), name='registration-complete'),
    url(r'^stats/$', StatsView.as_view(template_name="ratsightings/ratsighting_stats.html"), name='stats'),

]
