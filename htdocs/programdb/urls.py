
from .views import ProjectProposalImport, ProjectProposalList, ProjectProposalCreate, ProjectProposalUpdate, ProjectProposalDelete, ProgramDash, ProjectAgreementCreate, ProjectAgreementUpdate, ProjectAgreementDelete, ProjectCompleteCreate, ProjectCompleteUpdate, ProjectCompleteDelete, ProjectCompleteImport


try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here

urlpatterns = patterns('',

                       ###PROGRAMDB
                       url(r'^dashboard', ProgramDash.as_view(), name='dashboard'),

                       #project proposal
                       url(r'^projectproposal_list', ProjectProposalList.as_view(), name='projectproposal_list'),
                       url(r'^projectproposal_add', ProjectProposalCreate.as_view(), name='projectproposal_add'),
                       url(r'^projectproposal_update/(?P<pk>\w+)/$', ProjectProposalUpdate.as_view(), name='projectproposal_update'),
                       url(r'^projectproposal_delete/(?P<pk>\w+)/$', ProjectProposalDelete.as_view(), name='projectproposal_delete'),
                       url(r'^projectagreement_add/(?P<pk>\w+)/$', ProjectAgreementCreate.as_view(), name='projectagreement_add'),
                       url(r'^projectagreement_update/(?P<pk>\w+)/$', ProjectAgreementUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectagreement_delete/(?P<pk>\w+)/$', ProjectAgreementDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectproposal_import', ProjectProposalImport.as_view(), name='projectproposal_import'),
                       url(r'^projectcomplete_add/(?P<pk>\w+)/$', ProjectCompleteCreate.as_view(), name='projectproposal_add'),
                       url(r'^projectcomplete_update/(?P<pk>\w+)/$', ProjectCompleteUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectcomplete_delete/(?P<pk>\w+)/$', ProjectCompleteDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectcomplete_import', ProjectCompleteImport.as_view(), name='projectcomplete_import'),
                       url(r'^doimport/(?P<pk>\w+)/$', 'programdb.views.doImport' , name='doImport'),
                       url(r'^doMerge/(?P<pk>\w+)/$', 'programdb.views.doMerge', name='doMerge'),


                       )
