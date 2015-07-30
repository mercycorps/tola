from django.contrib import admin
from .models import Silo, Read, ReadType, GoogleCredentialsModel

admin.site.register(GoogleCredentialsModel)
admin.site.register(Read)
admin.site.register(ReadType)

admin.site.register(Silo)