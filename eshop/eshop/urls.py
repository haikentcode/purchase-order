from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from purchase.views import UserViewSet, GroupViewSet
from purchase import urls as purchase_urls

# Docs
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('purchase/', include(purchase_urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]

# Docs
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
