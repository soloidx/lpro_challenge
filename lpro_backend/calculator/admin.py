from django.contrib import admin
from calculator import models


class OperationAdmin(admin.ModelAdmin):
    list_display = ("type", "cost")


class RecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Operation, OperationAdmin)
admin.site.register(models.Record, RecordAdmin)
