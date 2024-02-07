from rest_framework import viewsets

from backoffice_cache.decorators import set_cache_response
from partners.models import PartnerConfig
from partners.permissions import IsServiceAuthenticated
from partners.serializers import PartnerConfigSerializer


class PartnerConfigViewSet(viewsets.ModelViewSet):
    queryset = PartnerConfig.objects.all()
    serializer_class = PartnerConfigSerializer
    permission_classes = [IsServiceAuthenticated, ]
    is_cached = True

    @set_cache_response()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
