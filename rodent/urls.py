from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from ratsightings.views import RatSightingViewSet
from .views import UserViewSet, GroupViewSet

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'ratsightings', RatSightingViewSet)

schema_view = get_schema_view(title='Rodent API')

urlpatterns = [
    #url(r'^$', ratsightings.views.index, name='index'),
    #url(r'^map/', ratsightings.views.map, name='map'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/', include('djoser.urls')),
    url(r'^api/auth/', include('djoser.urls.authtoken')),
    url(r'^schema/$', schema_view),
]
