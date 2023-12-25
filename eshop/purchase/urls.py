from django.urls import include, path
from rest_framework import routers

from purchase.views import OrderViewSet, LineItemViewSet, SupplierViewSet

router = routers.DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'line_items', LineItemViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
