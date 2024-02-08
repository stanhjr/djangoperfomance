from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import viewsets
from partners.models import PartnerConfig
from partners.permissions import IsServiceAuthenticated
from partners.serializers import PartnerConfigSerializer


class PartnerConfigViewSet(viewsets.ModelViewSet):
    queryset = PartnerConfig.objects.all()
    serializer_class = PartnerConfigSerializer
    permission_classes = [IsServiceAuthenticated, ]
    is_cached = True

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
