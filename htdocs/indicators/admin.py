from django.contrib import admin
from indicators.models import IndicatorType, Indicator

admin.site.register(IndicatorType)
admin.site.register(Indicator)
