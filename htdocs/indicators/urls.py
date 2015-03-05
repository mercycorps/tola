from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    ###INDICATOR PLANING TOOL
    #Home
    url(r'^home/(?P<id>\w+)/$', 'indicators.views.home', name='home'),
    
    #Dashboard
    url(r'^dashboard', 'indicators.views.dashboard', name='dashboard'),

    #View Program Indicators
    url(r'^programIndicator/(?P<id>\w+)/$', 'indicators.views.programIndicator', name='programIndicator'),
    
    #Edit Indicators to Program
    url(r'^editIndicator/(?P<id>\w+)/$', 'indicators.views.editIndicator', name='editIndicator'),
    
    #Add Indicators to Program
    url(r'^indicator', 'indicators.views.indicator', name='indicator'),
    
)