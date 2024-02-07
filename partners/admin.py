from django.contrib import admin

from partners.models import PartnerConfig, ServiceApiKey


@admin.register(PartnerConfig)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceApiKey)
class ServiceApiKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('key', )
