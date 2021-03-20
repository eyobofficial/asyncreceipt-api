from django.urls import path, include

from rest_framework import routers

from .views import ReceiptViewSet


router = routers.DefaultRouter()
router.register(r'receipts', ReceiptViewSet)

urlpatterns = router.urls
