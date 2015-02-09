
from .views import ProjectProposalImport, ProjectProposalList, ProjectProposalCreate, ProjectProposalUpdate, ProjectProposalDelete, \
    ProgramDash, ProjectAgreementCreate, ProjectAgreementList, ProjectAgreementUpdate, ProjectAgreementDelete, ProjectCompleteCreate, ProjectCompleteUpdate,\
    ProjectCompleteList, ProjectCompleteDelete, ProjectCompleteImport, CommunityList, CommunityCreate, CommunityUpdate, CommunityDelete,\
    DocumentationList, DocumentationCreate, DocumentationUpdate, DocumentationDelete


try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here

urlpatterns = patterns('',

                       ###PROGRAMDB
                       url(r'^dashboard/(?P<pk>\w+)/$', ProgramDash.as_view(), name='dashboard'),

                       #project proposal
                       url(r'^projectproposal_list', ProjectProposalList.as_view(), name='projectproposal_list'),
                       url(r'^projectproposal_add', ProjectProposalCreate.as_view(), name='projectproposal_add'),
                       url(r'^projectproposal_update/(?P<pk>\w+)/$', ProjectProposalUpdate.as_view(), name='projectproposal_update'),
                       url(r'^projectproposal_delete/(?P<pk>\w+)/$', ProjectProposalDelete.as_view(), name='projectproposal_delete'),
                       url(r'^projectproposal_import', ProjectProposalImport.as_view(), name='projectproposal_import'),

                       url(r'^projectagreement_list', ProjectAgreementList.as_view(), name='projectagreement_list'),
                       url(r'^projectagreement_add', ProjectAgreementCreate.as_view(), name='projectagreement_add'),
                       url(r'^projectagreement_update/(?P<pk>\w+)/$', ProjectAgreementUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectagreement_delete/(?P<pk>\w+)/$', ProjectAgreementDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectproposal_import', ProjectProposalImport.as_view(), name='projectproposal_import'),

                       url(r'^projectcomplete_list', ProjectCompleteList.as_view(), name='projectcomplete_list'),
                       url(r'^projectcomplete_add/(?P<pk>\w+)/$', ProjectCompleteCreate.as_view(), name='projectproposal_add'),
                       url(r'^projectcomplete_update/(?P<pk>\w+)/$', ProjectCompleteUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectcomplete_delete/(?P<pk>\w+)/$', ProjectCompleteDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectcomplete_import', ProjectCompleteImport.as_view(), name='projectcomplete_import'),

                       url(r'^community_list', CommunityList.as_view(), name='community_list'),
                       url(r'^community_add', CommunityCreate.as_view(), name='community_add'),
                       url(r'^community_update/(?P<pk>\w+)/$', CommunityUpdate.as_view(), name='community_update'),
                       url(r'^community_delete/(?P<pk>\w+)/$', CommunityDelete.as_view(), name='community_delete'),

                       url(r'^documentation_list', DocumentationList.as_view(), name='documentation_list'),
                       url(r'^documentation_add', DocumentationCreate.as_view(), name='documentation_add'),
                       url(r'^documentation_update/(?P<pk>\w+)/$', DocumentationUpdate.as_view(), name='documentation_update'),
                       url(r'^documentation_delete/(?P<pk>\w+)/$', DocumentationDelete.as_view(), name='documentation_delete'),

                       url(r'^doimport/(?P<pk>\w+)/$', 'programdb.views.doImport' , name='doImport'),
                       url(r'^doMerge/(?P<pk>\w+)/$', 'programdb.views.doMerge', name='doMerge'),


                       )
