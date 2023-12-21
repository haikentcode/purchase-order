from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from purchase.views import UserViewSet, GroupViewSet
from purchase import urls as purchase_urls

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('purchase/', include(purchase_urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
