from silo import views
from silo.views import  UserViewSet, ReadViewSet, ReadTypeViewSet, SiloViewSet
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from silo.api import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'silo', SiloViewSet)
router.register(r'users', UserViewSet)
router.register(r'read', ReadViewSet)
router.register(r'readtype', ReadTypeViewSet)





urlpatterns = patterns('',
                        #rest framework
                        url(r'^api/', include(router.urls)),
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                        url(r'^api/silodata/(?P<id>[0-9]+)/$', 'silo.api.silo_data_api', name='silodata'),

                        #index
                        url(r'^$', 'silo.views.index', name='index'),

                        #base template for layout
                        url(r'^$', TemplateView.as_view(template_name='base.html')),

                        #rest Custom Feed
                        url(r'^api/custom/(?P<id>[0-9]+)/$','silo.views.customFeed',name='customFeed'),

                        #ipt app specific urls
                        #url(r'^indicators/', include('indicators.urls')),

                        #enable admin documentation:
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        #enable the admin:
                        url(r'^admin/', include(admin.site.urls)),

                        #home
                        url(r'^home', 'silo.views.listSilos', name='listSilos'),

                        ###READ
                        #read init form
                        url(r'^read/home', 'silo.views.home', name='home'),

                        #read init form
                        url(r'^new_read', 'silo.views.initRead', name='initRead'),

                        #show read or source
                        url(r'^show_read/(?P<id>\w+)/$', 'silo.views.showRead', name='showRead'),

                        #upload form
                        url(r'^file/(?P<id>\w+)/$', 'silo.views.uploadFile', name='uploadFile'),

                        #getJSON data
                        url(r'^json', 'silo.views.getJSON', name='getJSON'),

                        #login data
                        url(r'^read/login/$', 'silo.views.getLogin', name='getLogin'),
                        url(r'^onalogin/$', 'silo.views.getOnaForms', name='getOnaForms'),
                        url(r'^provider_logout/(?P<provider>\w+)/$', 'silo.views.providerLogout', name='providerLogout'),
                        url(r'^saveAndImportRead/$', 'silo.views.saveAndImportRead', name='saveAndImportRead'),
                        url(r'^tolacon/$', 'silo.views.tolaCon', name='tolacon'),
                        url(r'^toggle_silo_publicity/$', 'silo.views.toggle_silo_publicity', name='toggle_silo_publicity'),
                        
                        ###DISPLAY
                        #list all silos
                        url(r'^silos', 'silo.views.listSilos', name='listSilos'),

                        #merge form
                        url(r'^merge/(?P<id>\w+)/$', 'silo.views.mergeForm', name='mergeForm'),

                        #merge select columns
                        url(r'^merge_columns', 'silo.views.mergeColumns', name='mergeColumns'),
                        url(r'^doMerge', 'silo.views.doMerge', name='doMerge'),
                        
                        #view silo detail
                        url(r'^silo_detail/(?P<id>\w+)/$', 'silo.views.siloDetail', name='siloDetail'),

                        #edit single silo value
                        url(r'^value_edit/(?P<id>\w+)/$', 'silo.views.valueEdit', name='valueEdit'),

                        #delete single silo value
                        url(r'^value_delete/(?P<id>\w+)/$', 'silo.views.valueDelete', name='valueDelete'),

                        #edit silo
                        url(r'^silo_edit/(?P<id>\w+)/$', 'silo.views.editSilo', name='editSilo'),

                        #delete a silo
                        url(r'^silo_delete/(?P<id>\w+)/$','silo.views.deleteSilo', name='deleteSilo'),

                        #new silo column
                        url(r'^new_column/(?P<id>\w+)/$', 'silo.views.newColumn', name='newColumn'),

                        #edit silo columns
                        url(r'^edit_columns/(?P<id>\w+)/$', 'silo.views.editColumns', name='editColumns'),

                        #delete silo column
                        url(r'^delete_column/(?P<id>\w+)/(?P<column>\w+)/$', 'silo.views.deleteColumn', name='deleteColumn'),

                        ###FEED
                        url(r'^export/(?P<id>\w+)/$', 'silo.views.export_silo', name='export_silo'),
                        url(r'^export_new_gsheet/(?P<id>\d+)/$', 'silo.views.export_new_gsheet', name='export_new_gsheet'),
                        url(r'^export_gsheet/(?P<id>\d+)/$', 'silo.views.export_gsheet', name='export_existing_gsheet'),
                        url(r'^oauth2callback/$', 'silo.views.oauth2callback', name='oauth2callback'),

                        #create a feed
                        url(r'^create_feed', 'silo.views.createFeed', name='createFeed'),

                        #local login
                        url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                        url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),

                        url(r'^accounts/logout/$', 'tola.views.logout_view', name='logout'),

                        #accounts
                        url(r'^accounts/profile/$', 'tola.views.profile', name='profile'),
                        url(r'^accounts/register/$', 'tola.views.register', name='register'),

                        #Auth backend URL's
                        url('', include('django.contrib.auth.urls', namespace='auth')),
                        url('', include('social.apps.django_app.urls', namespace='social')),

                        #FAQ, Contact etc..
                        url(r'^contact', 'tola.views.contact', name='contact'),
                        url(r'^faq', 'tola.views.faq', name='faq'),
                        url(r'^documentation', 'tola.views.documentation', name='documentation'),


)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

