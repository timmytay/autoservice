from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import (
    Client, Car, Mechanic, Service, Part, 
    RepairOrder, OrderService, OrderPart
)
from .serializers import (
    ClientSerializer, CarSerializer, MechanicSerializer,
    ServiceSerializer, PartSerializer, RepairOrderSerializer,
    OrderServiceSerializer, OrderPartSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]


class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer
    permission_classes = [AllowAny]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [AllowAny]


class RepairOrderViewSet(viewsets.ModelViewSet):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    permission_classes = [AllowAny]


class OrderServiceViewSet(viewsets.ModelViewSet):
    queryset = OrderService.objects.all()
    serializer_class = OrderServiceSerializer
    permission_classes = [AllowAny]


class OrderPartViewSet(viewsets.ModelViewSet):
    queryset = OrderPart.objects.all()
    serializer_class = OrderPartSerializer
    permission_classes = [AllowAny]