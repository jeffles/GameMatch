import models
from django.contrib import admin
from django.contrib.auth.models import User


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('host',)

    def save_model(self, request, obj, form, change):
        obj.host = request.user
        obj.save()

admin.site.register(models.Event, EventAdmin)