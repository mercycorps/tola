from silo import views
from silo.views import FeedViewSet,DataFieldViewSet,ValueStoreViewSet, UserViewSet, ReadViewSet, ReadTypeViewSet, SiloViewSet
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'silo', SiloViewSet)
router.register(r'users', UserViewSet)
router.register(r'feed', FeedViewSet)
router.register(r'datafield', DataFieldViewSet)
router.register(r'valuestore', ValueStoreViewSet)
router.register(r'read', ReadViewSet)
router.register(r'readtype', ReadTypeViewSet)





urlpatterns = patterns('',
                        #rest framework
                        url(r'^api/', include(router.urls)),
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

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

                        #read ODK form
                        url(r'^new_odk', 'silo.views.odk', name='odk'),

                        #show read or source
                        url(r'^show_read/(?P<id>\w+)/$', 'silo.views.showRead', name='showRead'),

                        #upload form
                        url(r'^file/(?P<id>\w+)/$', 'silo.views.uploadFile', name='uploadFile'),

                        #getJSON data
                        url(r'^json', 'silo.views.getJSON', name='getJSON'),

                        #updateUID data
                        url(r'^update', 'silo.views.updateUID', name='updateUID'),

                        #login data
                        url(r'^read/login/$', 'silo.views.getLogin', name='getLogin'),

                        url(r'^read/odk_login/$', 'silo.views.odkLogin', name='odkLogin'),


                        ###DISPLAY
                        #list all silos
                        url(r'^silos', 'silo.views.listSilos', name='listSilos'),

                        #show silo detail and sources
                        url(r'^silo/(?P<id>\w+)/$', 'silo.views.viewSilo', name='viewSilo'),

                        #merge form
                        url(r'^merge/(?P<id>\w+)/$', 'silo.views.mergeForm', name='mergeForm'),

                        #merge select columns
                        url(r'^merge_columns', 'silo.views.mergeColumns', name='mergeColumns'),

                        #list all silos
                        url(r'^display', 'silo.views.listSilos', name='listSilos'),

                        #view silo detail
                        url(r'^silo_detail/(?P<id>\w+)/$', 'silo.views.siloDetail', name='siloDetail'),

                        #edit single silo value
                        url(r'^value_edit/(?P<id>\w+)/$', 'silo.views.valueEdit', name='valueEdit'),

                        #delete single silo value
                        url(r'^value_delete/(?P<id>\w+)/$', 'silo.views.valueDelete', name='valueDelete'),

                        #edit single field
                        url(r'^field_edit/(?P<id>\w+)/$', 'silo.views.fieldEdit', name='fieldEdit'),


                        ###SILO
                        url(r'^do_merge', 'silo.views.doMerge', name='doMerge'),

                        #edit silo
                        url(r'^silo_edit/(?P<id>\w+)/$', 'silo.views.editSilo', name='editSilo'),

                        #merge silos
                        url(r'^doMerge', 'silo.views.doMerge', name='doMerge'),

                        #delete a silo
                        url(r'^silo_delete/(?P<id>\w+)/$','silo.views.deleteSilo', name='deleteSilo'),

                        ###FEED
                        url(r'^feed', 'silo.views.listFeeds', name='listFeeds'),
                        url(r'^export/(?P<id>\w+)/$', 'silo.views.export_silo', name='export_silo'),
                        url(r'^export_new_gsheet/(?P<id>\d+)/$', 'silo.views.export_new_gsheet', name='export_new_gsheet'),
                        url(r'^export_gsheet/(?P<id>\d+)/$', 'silo.views.export_gsheet', name='export_existing_gsheet'),
                        url(r'^oauth2callback/$', 'silo.views.oauth2callback', name='oauth2callback'),
                        
                        #create a feed
                        url(r'^create_feed', 'silo.views.createFeed', name='createFeed'),

                        #app include of readtoken urls
                        url(r'^readtoken/', include('readtoken.urls')),

                        #local login
                        (r'^accounts/login/',  login),
                        url(r'^accounts/logout/$', 'tola.views.logout_view', name='logout'),

                        #accounts
                        url(r'^accounts/profile/$', 'tola.views.profile', name='profile'),
                        url(r'^accounts/register/$', 'tola.views.register', name='register'),

                        #FAQ, Contact etc..
                        url(r'^contact', 'tola.views.contact', name='contact'),
                        url(r'^faq', 'tola.views.faq', name='faq'),
                        url(r'^documentation', 'tola.views.documentation', name='documentation'),


)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

