from feed import views
from feed.views import FeedViewSet,DataFieldViewSet,ValueStoreViewSet, UserViewSet, ReadViewSet, ReadTypeViewSet, SiloViewSet
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
                        url(r'^$', 'display.views.index', name='index'),

                        #base template for layout
                        url(r'^$', TemplateView.as_view(template_name='base.html')),

                        #rest Custom Feed
                        url(r'^api/custom/(?P<id>[0-9]+)/$','feed.views.customFeed',name='customFeed'),

                        #ipt app specific urls
                        #url(r'^indicators/', include('indicators.urls')),

                        #enable admin documentation:
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        #enable the admin:
                        url(r'^admin/', include(admin.site.urls)),

                        #home
                        url(r'^home', 'display.views.listSilos', name='listSilos'),

                        ###READ
                        #read init form
                        url(r'^read/home', 'read.views.home', name='home'),

                        #read init form
                        url(r'^new_read', 'read.views.initRead', name='initRead'),

                        #read ODK form
                        url(r'^new_odk', 'read.views.odk', name='odk'),

                        #show read or source
                        url(r'^show_read/(?P<id>\w+)/$', 'read.views.showRead', name='showRead'),

                        #upload form
                        url(r'^file/(?P<id>\w+)/$', 'read.views.uploadFile', name='uploadFile'),

                        #getJSON data
                        url(r'^json', 'read.views.getJSON', name='getJSON'),

                        #updateUID data
                        url(r'^update', 'read.views.updateUID', name='updateUID'),

                        #login data
                        url(r'^read/login/$', 'read.views.getLogin', name='getLogin'),

                        url(r'^read/odk_login/$', 'read.views.odkLogin', name='odkLogin'),


                        ###DISPLAY
                        #list all silos
                        url(r'^silos', 'display.views.listSilos', name='listSilos'),

                        #show silo detail and sources
                        url(r'^silo/(?P<id>\w+)/$', 'display.views.viewSilo', name='viewSilo'),

                        #merge form
                        url(r'^merge/(?P<id>\w+)/$', 'display.views.mergeForm', name='mergeForm'),

                        #merge select columns
                        url(r'^merge_columns', 'display.views.mergeColumns', name='mergeColumns'),

                        #list all silos
                        url(r'^display', 'display.views.listSilos', name='listSilos'),

                        #view silo detail
                        url(r'^silo_detail/(?P<id>\w+)/$', 'display.views.siloDetail', name='siloDetail'),

                        #edit single silo value
                        url(r'^value_edit/(?P<id>\w+)/$', 'display.views.valueEdit', name='valueEdit'),

                        #delete single silo value
                        url(r'^value_delete/(?P<id>\w+)/$', 'display.views.valueDelete', name='valueDelete'),

                        #edit single field
                        url(r'^field_edit/(?P<id>\w+)/$', 'display.views.fieldEdit', name='fieldEdit'),


                        ###SILO
                        url(r'^do_merge', 'silo.views.doMerge', name='doMerge'),

                        #edit silo
                        url(r'^silo_edit/(?P<id>\w+)/$', 'silo.views.editSilo', name='editSilo'),

                        #merge silos
                        url(r'^doMerge', 'silo.views.doMerge', name='doMerge'),

                        #delete a silo
                        url(r'^silo_delete/(?P<id>\w+)/$','silo.views.deleteSilo', name='deleteSilo'),

                        ###FEED
                        url(r'^feed', 'feed.views.listFeeds', name='listFeeds'),
                        url(r'^export/(?P<id>\w+)/$', 'feed.views.export_silo', name='export_silo'),
                        #url(r'^export_google/(?P<id>\w+)/$', 'feed.views.export_google', name='export_google'),
                        url(r'^export_google/(?P<id>\d+)/$', 'feed.views.google_export', name='export_google'),
                        url(r'^oauth2callback/$', 'feed.views.oauth2callback', name='oauth2callback'),
                        
                        #create a feed
                        url(r'^create_feed', 'feed.views.createFeed', name='createFeed'),

                        #home
                        url(r'^contact', 'tola.views.contact', name='contact'),
                        url(r'^faq', 'tola.views.faq', name='faq'),
                        url(r'^documentation', 'tola.views.documentation', name='documentation'),

                        #app include of readtoken urls
                        url(r'^readtoken/', include('readtoken.urls')),

                        #app include of activitydb urls
                        url(r'^activitydb/', include('activitydb.urls')),

                        #app include of activitydb urls
                        url(r'^indicators/', include('indicators.urls')),

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

