from django.contrib import admin

from .models import Attribute, Operation, BasicOperation, InformationPack

admin.site.register(BasicOperation)
admin.site.register(Operation)
admin.site.register(Attribute)
admin.site.register(InformationPack)
