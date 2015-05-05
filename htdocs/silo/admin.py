from django.contrib import admin
from .models import Silo, DataField, ValueStore, Read, ReadType, GoogleCredentialsModel

admin.site.register(GoogleCredentialsModel)
admin.site.register(Read)
admin.site.register(ReadType)

admin.site.register(Silo)
admin.site.register(DataField)
admin.site.register(ValueStore)