from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'mechanics', views.MechanicViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'orders', views.RepairOrderViewSet)
router.register(r'order-services', views.OrderServiceViewSet)
router.register(r'order-parts', views.OrderPartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]