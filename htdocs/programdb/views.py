from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import ProjectProposal, ProgramDashboard, Program, Country, Province, Village, District, ProjectAgreement, ProjectComplete, Community, Documentation
from silo.models import Silo, ValueStore, DataField
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import ProjectProposalForm, ProgramDashboardForm, ProjectAgreementForm, ProjectCompleteForm, DocumentationForm, CommunityForm
import logging
from django.shortcuts import render
from django.contrib import messages
from django.db import connections
from django.contrib.auth.models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ProgramDash(ListView):

    template_name = 'programdb/programdashboard_list.html'


    def get(self, request, *args, **kwargs):
        #set country to afghanistan for now until we have user data on country
        #use self.request.user to get users country
        #self.kwargs.pk = ID of program from dropdown
        set_country = "1"
        form = ProgramDashboardForm
        getPrograms = Program.objects.all().filter(funding_status="Funded", country=set_country)
        print int(self.kwargs['pk'])

        if int(self.kwargs['pk']) == 0:
            print "000"
            getDashboard = ProgramDashboard.objects.all()
        else:
             getDashboard = ProgramDashboard.objects.all().filter(program_id=self.kwargs['pk'])

        return render(request, self.template_name, {'form': form,'getDashboard':getDashboard,'getPrograms':getPrograms})

    def post(self, request, *args, **kwargs):
        form = self.ProgramDashboard(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            getDashboard = ProgramDashboard.objects.all().filter(program=request.FORM("program_id"))


        return render(request, self.template_name, {'form': form,'getDashboard':getDashboard,'getPrograms':getPrograms})

"""
Project Proposal
"""
class ProjectProposalList(ListView):

    model = ProjectProposal

    def get_context_data(self, **kwargs):
        context = super(ProjectProposalList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProjectProposalImport(ListView):

    model = Silo

    def get_context_data(self, **kwargs):
        context = super(ProjectProposalImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'programdb/projectproposal_import.html'


class ProjectProposalCreate(CreateView):
    """
    Project Proposal Form
    """

    model = ProjectProposal

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        #create a new dashbaord entry for the project
        latest = ProjectProposal.objects.latest('id')
        getProposal = ProjectProposal.objects.get(id=latest.id)
        getProgram = Program.objects.get(id=latest.program_id)

        create_dashboard_entry = ProgramDashboard(program=getProgram, project_proposal=getProposal)
        create_dashboard_entry.save()

        messages.success(self.request, 'Success, Proposal Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectProposalForm


class ProjectProposalUpdate(UpdateView):
    """
    Project Proposal Form
    """

    model = ProjectProposal

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Proposal Updated!')

        is_approved = self.request.GET.get('approved')

        if is_approved:
            update_dashboard = ProgramDashboard.objects.filter(project_proposal__id=self.request.GET.get('id')).update(project_proposal_approved=True)

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectProposalForm


class ProjectProposalDelete(DeleteView):
    """
    Project Proposal Form
    """

    model = ProjectProposal

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Proposal Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectProposalForm

"""
Project Agreement
"""
class ProjectAgreementList(ListView):

    model = ProjectAgreement

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProjectAgreementCreate(CreateView):
    """
    Project Agreement Form
    """

    model = ProjectAgreement

    def get_context_data(self, **kwargs):
        data = super(ProjectAgreementCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ProjectAgreement'] = ProjectAgreementForm(self.request.POST)
        else:
            data['ProjectAgreement'] = ProjectAgreementForm()
        return data

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        latest = ProjectAgreement.objects.latest('id')
        getAgreement = ProjectAgreement.objects.get(id=latest.id)

        update_dashboard = ProgramDashboard.objects.filter(project_proposal__id=self.request.POST['project_proposal']).update(project_agreement=getAgreement)

        messages.success(self.request, 'Success, Agreement Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectAgreementForm


class ProjectAgreementUpdate(UpdateView):
    """
    Project Agreement Form
    """

    model = ProjectAgreement

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectAgreementForm


class ProjectAgreementDelete(DeleteView):
    """
    Project Agreement Delete
    """

    model = ProjectAgreement

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/programdb/success')

    form_class = ProjectAgreementForm

"""
Project Complete
"""
class ProjectCompleteList(ListView):

    model = ProjectComplete

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProjectCompleteCreate(CreateView):
    """
    Project Complete Form
    """

    model = ProjectComplete

    def get_context_data(self, **kwargs):
        data = super(ProjectCompleteCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ProjectComplete'] = ProjectCompleteForm(self.request.POST)
        else:
            data['ProjectComplete'] = ProjectCompleteForm()
        return data

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        latest = ProjectComplete.objects.latest('id')
        getComplete = ProjectComplete.objects.get(id=latest.id)

        update_dashboard = ProgramDashboard.objects.filter(project_agreement__id=self.request.POST['project_proposal']).update(project_complete=getComplete)

        messages.success(self.request, 'Success, Completion Form Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectCompleteForm


class ProjectCompleteUpdate(UpdateView):
    """
    Project Complete Form
    """

    model = ProjectComplete

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectCompleteForm


class ProjectCompleteDelete(DeleteView):
    """
    Project Complete Delete
    """

    model = ProjectComplete

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/programdb/success')

    form_class = ProjectCompleteForm


class ProjectCompleteImport(ListView):

    model = Silo

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'programdb/projectcomplete_import.html'


"""
Documentation
"""
class DocumentationList(ListView):

    model = Documentation

    def get_context_data(self, **kwargs):
        context = super(DocumentationList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class DocumentationCreate(CreateView):
    """
    Documentation Form
    """

    model = Documentation

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationUpdate(UpdateView):
    """
    Documentation Form
    """

    model = ProjectProposal

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Documentation Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationDelete(DeleteView):
    """
    Documentation Form
    """

    model = Documentation

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


"""
Community
"""

class CommunityList(ListView):

    model = Community

    def get_context_data(self, **kwargs):
        context = super(CommunityList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CommunityCreate(CreateView):
    """
    Community Form
    """

    model = Community

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Community Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityUpdate(UpdateView):
    """
    Community Form
    """

    model = Community

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Community Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityDelete(DeleteView):
    """
    Community Form
    """

    model = Community

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Community Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


def doImport(request, pk):
    """
    Copy the selected Silo data into the Project Proposal tables letting the user map
    the columns first
    :param request:
    :return:
    """
    from_silo_id = pk

    getSourceFrom = DataField.objects.all().filter(silo__id=from_silo_id).values('name').distinct()
    getSourceTo = ProjectProposal._meta.get_all_field_names()
    users = User.objects.all()


    return render(request, "programdb/merge-column-form.html", {'getSourceFrom':getSourceFrom, 'getSourceTo':getSourceTo, 'from_silo_id':from_silo_id, 'users':users})

def doMerge(request, pk):
    """
    Copy the selected Silo data into the Project Proposal tables letting the user map
    the columns first
    :param request:
    :return:
    """
    from_silo_id = pk
    approved_by = None
    approval_submitted_by = None

    # Empty dict
    fields_to_insert = {}
    fields_to_ignore = {}

    #more then one record might be returning so get the row_numbers as a count and loop over each
    get_rows = ValueStore.objects.values('row_number').filter(field__silo__id=from_silo_id).distinct()
    for row in get_rows:
        #now loop over each column in the post and check if a mapping was made
        #request.POST[column] = Form field value
        #column = Form field name(variable)
        for column in request.POST:
            try:
                getSourceFrom = ValueStore.objects.get(field__silo__id=from_silo_id, field__name=str(column), row_number=row['row_number'])
            except Exception as e:
                getSourceFrom = None
                print e
                print "No value for: " + str(column)
                pass
            #if we found source data process it to be saved
            if getSourceFrom:
                #look for the program in the form and return the related object id
                if "program" in str(column):
                    program_value = getSourceFrom.char_store
                    print "column=" + str(column) + "CHAR STORE=" + program_value
                #look for the country in the form and return the related object id
                elif "country" in column:
                    country_value = getSourceFrom.char_store
                    print "column=" + str(column) + "CHAR STORE=" + country_value
                #look for the country in the form and return the related object id
                elif "province" in column:
                    province_value = getSourceFrom.char_store
                    print "column=" + str(column) + "CHAR STORE=" + province_value
                #look for the village in the form and return the related object id
                elif "district" in column:
                    district_value = getSourceFrom.char_store
                    print "column=" + str(column) + "CHAR STORE=" + district_value
                #look for the village in the form and return the related object id
                elif "village" in column:
                    village_value = getSourceFrom.char_store
                    print "column=" + str(column) + "CHAR STORE=" + village_value
                #look for the approved by user in the form and return the related object id
                elif "approve_by" in column:
                    approved_by = User.objects.get(id=request.POST[column])
                    print "column=" + str(column) + "CHAR STORE=" + request.POST[column]
                #look for the submittede by user in the form and return the related object id
                elif "submitted_by" in column:
                    approval_submitted_by = User.objects.get(id=request.POST[column])
                    print "column=" + str(column) + "CHAR STORE=" + request.POST[column]
                else:
                    if request.POST[column] != "Ignore" and request.POST[column] != "0" and str(column) != "csrfmiddlewaretoken" and str(column) != "from_column_id"  and str(column) != "from_silo_id":
                        fields_to_insert[str(request.POST[column])] = str(getSourceFrom.char_store)
                    else:
                        fields_to_ignore[str(request.POST[column])] = str(getSourceFrom.char_store)

        #set program ID and throw if not found
        try:
            programs, created = Program.objects.get_or_create(name__icontains=program_value)
            program_id = programs.pk
        except Exception as e:
            print e
            program_id = None
            messages.add_message(request, messages.INFO, "Program ID not found, a program is required for each new project proposal.")

        #set country ID and throw if not found
        # try:
        #     country, created = Country.objects.get_or_create(name__icontains=country_value)
        #     country_id = country.pk
        #     set_country_id=country_id
        # except:
        #     raise Exception("Country ID not found, a country is required for each new project proposal.")
        #commented out for now until country is added to form and hard coded to 1
        country_id = 1

        #set province ID and throw if not found
        try:
            province, created = Province.objects.get_or_create(name__icontains=province_value, country_id=country_id)
            province_id = province.pk
        except Exception as e:
            print e
            province_id = None
            messages.add_message(request, messages.INFO, "Province ID not found, a province is required for each new project proposal.")

        #set district ID and throw if not found
        try:
            district, created = District.objects.get_or_create(name__icontains=district_value, province_id=province_id)
            district_id = district.pk
        except Exception as e:
            print e
            district_id = None
            messages.add_message(request, messages.INFO, "District ID not found, a district is required for each new project proposal.")

        #set village ID and throw if not found
        try:
            village, created = Village.objects.get_or_create(name__icontains=village_value, district_id=district_id)
            village_id = village.pk
        except Exception as e:
            print e
            village_id = None
            messages.add_message(request, messages.INFO, "Village ID not found, a village is required for each new project proposal.")

        print fields_to_insert

        new_project_proposal = ProjectProposal.objects.create(approved_by=approved_by, approval_submitted_by=approval_submitted_by, program_id=program_id, country_id=country_id, province_id=province_id, district_id=district_id, village_id=village_id, **fields_to_insert)
        new_project_proposal.save()

    redirect_url = "/programdb/projectproposal_update/" + str(new_project_proposal.id)

    return HttpResponseRedirect(redirect_url)


