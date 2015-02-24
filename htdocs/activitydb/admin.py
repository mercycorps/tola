from django.contrib import admin
from .models import Country, Province, Office, Village, Program, Documentation, Template,District, Contribution, QuantitativeOutputs, ProgramDashboard, ProjectProposal, ProjectAgreement, ProjectComplete, Community

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Office)
admin.site.register(District)
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
admin.site.register(Community)