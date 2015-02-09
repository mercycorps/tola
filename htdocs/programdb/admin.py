from django.contrib import admin
from .models import Country, Province, Cluster, Village, Program, Contribution, QuantitativeOutputs, ProgramDashboard, ProjectProposal, ProjectAgreement, ProjectComplete

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Cluster)
admin.site.register(Village)
admin.site.register(Program)
admin.site.register(Contribution)
admin.site.register(QuantitativeOutputs)
admin.site.register(ProgramDashboard)
admin.site.register(ProjectProposal)
admin.site.register(ProjectAgreement)
admin.site.register(ProjectComplete)
admin.site.register(Documentation)
admin.site.register(Template)