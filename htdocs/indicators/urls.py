from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    ###INDICATOR PLANING TOOL
    #Home
    url(r'^home', 'indicators.views.home', name='home'),
    
    #Dashboard
    url(r'^dashboard', 'indicators.views.dashboard', name='dashboard'),
    
    #Set up Program
    url(r'^program/', 'indicators.views.program', name='program'),
    
    #Edit Program
	url(r'^editProgram/(?P<id>\w+)/$', 'indicators.views.editProgram', name='editProgram'),
	    
    #View Program Indicators
	url(r'^programIndicator/(?P<id>\w+)/$', 'indicators.views.programIndicator', name='programIndicator'),
    
    #Set up Tool
    url(r'^tool', 'indicators.views.program', name='tool'),
    
    #Edit Indicators to Program
    url(r'^editIndicator/(?P<id>\w+)/$', 'indicators.views.editIndicator', name='editIndicator'),
    
    #Add Indicators to Program
    url(r'^indicator', 'indicators.views.indicator', name='indicator'),
    
)