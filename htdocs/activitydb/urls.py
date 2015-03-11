
from .views import ProjectProposalImport, ProjectProposalList, ProjectProposalCreate, ProjectProposalUpdate, ProjectProposalDelete, \
    ProgramDash, ProjectAgreementCreate, ProjectAgreementList, ProjectAgreementUpdate, ProjectAgreementDelete, ProjectAgreementImport, ProjectCompleteCreate, ProjectCompleteUpdate,\
    ProjectCompleteList, ProjectCompleteDelete, ProjectCompleteImport, CommunityList, CommunityCreate, CommunityUpdate, CommunityDelete,\
    DocumentationList, DocumentationCreate, DocumentationUpdate, DocumentationDelete,ProjectDash, MonitorList,MonitorCreate, MonitorDelete, MonitorUpdate,\
    BenchmarkCreate, BenchmarkDelete, BenchmarkUpdate, TrainingUpdate, TrainingCreate, TrainingDelete, TrainingList, QuantitativeOutputsList, QuantitativeOutputsCreate, QuantitativeOutputsUpdate, QuantitativeOutputsDelete


try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here

urlpatterns = patterns('',

                       ###activitydb
                       url(r'^dashboard/(?P<pk>\w+)/$', ProgramDash.as_view(), name='dashboard'),
                       url(r'^dashboard/project/(?P<pk>\w+)/$', ProjectDash.as_view(), name='project_dashboard'),

                       #project proposal
                       url(r'^projectproposal_list/(?P<pk>\w+)/$', ProjectProposalList.as_view(), name='projectproposal_list'),
                       url(r'^projectproposal_add', ProjectProposalCreate.as_view(), name='projectproposal_add'),
                       url(r'^projectproposal_update/(?P<pk>\w+)/$', ProjectProposalUpdate.as_view(), name='projectproposal_update'),
                       url(r'^projectproposal_delete/(?P<pk>\w+)/$', ProjectProposalDelete.as_view(), name='projectproposal_delete'),
                       url(r'^projectproposal_import', ProjectProposalImport.as_view(), name='projectproposal_import'),

                       url(r'^projectagreement_list/(?P<pk>\w+)/$', ProjectAgreementList.as_view(), name='projectagreement_list'),
                       url(r'^projectagreement_add/(?P<pk>\w+)/$', ProjectAgreementCreate.as_view(), name='projectagreement_add'),
                       url(r'^projectagreement_update/(?P<pk>\w+)/$', ProjectAgreementUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectagreement_delete/(?P<pk>\w+)/$', ProjectAgreementDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectagreement_import', ProjectAgreementImport.as_view(), name='projectagreement_import'),

                       url(r'^projectcomplete_list/(?P<pk>\w+)/$', ProjectCompleteList.as_view(), name='projectcomplete_list'),
                       url(r'^projectcomplete_add/(?P<pk>\w+)/$', ProjectCompleteCreate.as_view(), name='projectcomplete_add'),
                       url(r'^projectcomplete_update/(?P<pk>\w+)/$', ProjectCompleteUpdate.as_view(), name='projectcomplete_update'),
                       url(r'^projectcomplete_delete/(?P<pk>\w+)/$', ProjectCompleteDelete.as_view(), name='projectcomplete_delete'),
                       url(r'^projectcomplete_import', ProjectCompleteImport.as_view(), name='projectcomplete_import'),

                       url(r'^community_list/(?P<pk>\w+)/$', CommunityList.as_view(), name='community_list'),
                       url(r'^community_add', CommunityCreate.as_view(), name='community_add'),
                       url(r'^community_update/(?P<pk>\w+)/$', CommunityUpdate.as_view(), name='community_update'),
                       url(r'^community_delete/(?P<pk>\w+)/$', CommunityDelete.as_view(), name='community_delete'),

                       url(r'^documentation_list/(?P<pk>\w+)/$', DocumentationList.as_view(), name='documentation_list'),
                       url(r'^documentation_add', DocumentationCreate.as_view(), name='documentation_add'),
                       url(r'^documentation_update/(?P<pk>\w+)/$', DocumentationUpdate.as_view(), name='documentation_update'),
                       url(r'^documentation_delete/(?P<pk>\w+)/$', DocumentationDelete.as_view(), name='documentation_delete'),

                       url(r'^monitor_list/(?P<pk>\w+)/$', MonitorList.as_view(), name='monitor_list'),
                       url(r'^monitor_add/(?P<id>\w+)/$', MonitorCreate.as_view(), name='monitor_add'),
                       url(r'^monitor_update/(?P<pk>\w+)/$', MonitorUpdate.as_view(), name='monitor_update'),
                       url(r'^monitor_delete/(?P<pk>\w+)/$', MonitorDelete.as_view(), name='monitor_delete'),

                       url(r'^benchmark_add/(?P<id>\w+)/$', BenchmarkCreate.as_view(), name='benchmark_add'),
                       url(r'^benchmark_update/(?P<pk>\w+)/$', BenchmarkUpdate.as_view(), name='benchmark_update'),
                       url(r'^benchmark_delete/(?P<pk>\w+)/$', BenchmarkDelete.as_view(), name='benchmark_delete'),

                       url(r'^training_list/(?P<pk>\w+)/$', TrainingList.as_view(), name='training_list'),
                       url(r'^training_add/(?P<id>\w+)/$', TrainingCreate.as_view(), name='training_add'),
                       url(r'^training_update/(?P<pk>\w+)/$', TrainingUpdate.as_view(), name='training_update'),
                       url(r'^training_delete/(?P<pk>\w+)/$', TrainingDelete.as_view(), name='training_delete'),

                       url(r'^quantitative_list/(?P<pk>\w+)/$', QuantitativeOutputsList.as_view(), name='quantitative_list'),
                       url(r'^quantitative_add/(?P<id>\w+)/$', QuantitativeOutputsCreate.as_view(), name='quantitative_add'),
                       url(r'^quantitative_update/(?P<pk>\w+)/$', QuantitativeOutputsUpdate.as_view(), name='quantitative_update'),
                       url(r'^quantitative_delete/(?P<pk>\w+)/$', QuantitativeOutputsDelete.as_view(), name='quantitative_delete'),

                       url(r'^doimport/(?P<pk>\w+)/$', 'activitydb.views.doImport' , name='doImport'),
                       url(r'^doMerge/(?P<pk>\w+)/$', 'activitydb.views.doMerge', name='doMerge'),

                       url(r'^doMerge/(?P<pk>\w+)/$', 'activitydb.views.doMerge', name='doMerge'),
                       url(r'^province/(?P<province>[-\w]+)/province_json/', 'activitydb.views.province_json', name='province_json'),

                       )
