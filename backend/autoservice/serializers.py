from rest_framework import serializers
from .models import (
    Client, Car, Mechanic, Service, Part, 
    RepairOrder, OrderService, OrderPart
)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class OrderServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = OrderService
        fields = '__all__'


class OrderPartSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source='part.name', read_only=True)
    
    class Meta:
        model = OrderPart
        fields = '__all__'


class RepairOrderSerializer(serializers.ModelSerializer):
    car_info = serializers.CharField(source='car.__str__', read_only=True)
    mechanic_name = serializers.CharField(source='mechanic.__str__', read_only=True)
    services = OrderServiceSerializer(many=True, read_only=True, source='order_services')
    parts = OrderPartSerializer(many=True, read_only=True, source='order_parts')
    
    class Meta:
        model = RepairOrder
        fields = '__all__'