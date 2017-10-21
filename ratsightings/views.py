# Create your views here.
from .models import RatSighting
from .serializers import RatSightingSerializer
from rest_framework import viewsets


class RatSightingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = RatSighting.objects.all()
    serializer_class = RatSightingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)