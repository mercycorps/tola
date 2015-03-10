from django.contrib import admin
from .models import Country, Province, Office, Village, Program, Documentation, Template,District, Contribution, Sector, \
    QuantitativeOutputs, ProgramDashboard, ProjectProposal, ProjectAgreement, ProjectComplete, Community, Capacity, Monitor, \
    Benchmarks, Evaluate, ProjectType, TrainingAttendance, Beneficiary



admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Office)
admin.site.register(District)
admin.site.register(Village)
admin.site.register(Program)
admin.site.register(Contribution)
admin.site.register(Sector)
admin.site.register(QuantitativeOutputs)
admin.site.register(ProgramDashboard)
admin.site.register(ProjectProposal)
admin.site.register(ProjectAgreement)
admin.site.register(ProjectComplete)
admin.site.register(Documentation)
admin.site.register(Template)
admin.site.register(Community)
admin.site.register(Capacity)
admin.site.register(Monitor)
admin.site.register(Benchmarks)
admin.site.register(Evaluate)
admin.site.register(ProjectType)
admin.site.register(TrainingAttendance)
admin.site.register(Beneficiary)