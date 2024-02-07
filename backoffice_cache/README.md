# Backoffice cache
Caching package for Backoffice

## Getting started

if you need to add caching to the endpoint, you should perform the following steps

### 1. Add a cache setting decorator from this module
if you need to cache an list endpoint

```sh
def set_cache_response(
        key_type: Literal['partner_id_and_origin', 'api_key']
):
```

**key_type** - authentication key type, for example "origin" or "api_key"


### 2. Inherit from a AbstractCacheMixin
```sh
class SportViewSet(AbstractCacheMixin, AbstractApiKeyAuthViewSet):
    ...
```

### 3. add the is_cached method in your View Set

```sh
class PartnerViewSet(GetSerializerMixin, GenericViewSet):
    """
    ViewSet for Partner model.
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsServiceAuthenticated, ]
    authentication_classes = [ServiceApiKeyAuthentication, ]
    is_cached = True
```

### 4. GetCacheMiddleware

**GetCacheMiddleware** must be placed after the Cors middleware
and before the middleware that makes queries to the database
```sh
    'django.middleware.csrf.CsrfViewMiddleware',
    'base.backoffice_cache.middlewares.GetCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
```


### 5. implement cache invalidation signals

you can use the **CacheService** from this module

    CacheService.invalidate_cache_from_pattern(pattern)
    CacheService.invalidate_cache_from_pattern_and_uri(pattern, uri_list)

implementation of key generation for invalidation custom

EXAMPLE

```sh
@receiver([post_save, ], sender=WidgetSettings)
def invalidate_bet_insights_cache_from_widget_settings(sender, instance: WidgetSettings, **kwargs):
    """
    Invalidate cache entries associated with bet insights widget settings from the specified WidgetSettings instance.

    This signal receiver function is triggered on post-save actions for WidgetSettings instances.
    It identifies the associated partner's API keys, constructs a cache pattern for bet insights widget settings,
    and invalidates cache entries based on this pattern.
    """
    uri_for_invalidate = [
        'api/v1/bet_insights/partner-widgets_settings/',
    ]
    cache_service = CacheService()
    partner_ids = Partner.objects.filter(pk=instance.product.partner.pk).values_list('service_partner_id', flat=True)
    for partner_id in partner_ids:
        cache_key_pattern = f'*{partner_id}*'
        cache_service.invalidate_cache_from_pattern_and_uri(
            pattern=cache_key_pattern,
            uri_list=uri_for_invalidate
        )
```

### 6. Write tests

When writing your TestCase, be sure to inherit from **ClearCacheTestMixin** from this module

Example
```sh
class BetInsightsSetUpTestMixin(ClearCacheTestMixin):
    ...
    # your methods
```
