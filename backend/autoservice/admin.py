from django.contrib import admin
from .models import Client, Car, Mechanic, Service, Part, RepairOrder

admin.site.register(Client)
admin.site.register(Car)
admin.site.register(Mechanic)
admin.site.register(Service)
admin.site.register(Part)
admin.site.register(RepairOrder)