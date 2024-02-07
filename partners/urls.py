from rest_framework import routers


from partners.views import PartnerConfigViewSet

router = routers.DefaultRouter()
router.register(r'partner-config', PartnerConfigViewSet, basename='partner_config')

urlpatterns = router.urls
