from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from datetime import date
import os
import urllib2
import json
import unicodedata
from django.http import HttpResponseRedirect
from django.db import models
from models import Indicator
from activitydb.models import Program
from indicators.forms import IndicatorForm
from django.shortcuts import render_to_response
from django.contrib import messages



def home(request, id):
    """
    Get all of the Programs
    """
    #set country to afghanistan for now until we have user data on country
    #use self.request.user to get users country
    #self.kwargs.pk = ID of program from dropdown
    set_country = "1"
    getPrograms = Program.objects.all().filter(funding_status="Funded", country=set_country)
    getIndicators = Indicator.objects.all().filter(program__id=id)

    return render(request, 'indicators/home.html',{'getPrograms':getPrograms, 'getIndicators': getIndicators})

def dashboard(request):

    return render(request, 'indicators/dashboard.html')

def indicator(request):
    """
    Create an Indicator
    """
    if request.method == 'POST': # If the form has been submitted...
        form = IndicatorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            new = form.save()
            messages.success(request, 'Success, Indicator Created!')
            return HttpResponseRedirect('/indicators/indicator') # Redirect after POST to getLogin
    else:
        form = IndicatorForm() # An unbound form

    return render(request, 'indicators/indicator.html', {'form': form,})

def editIndicator(request,id):
    """
    Edit an Indicator
    """
    if request.method == 'POST': # If the form has been submitted...
        form = IndicatorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            update = Indicator.objects.get(pk=id)
            form = IndicatorForm(request.POST, instance=update)
            new = form.save(commit=True)
            messages.success(request, 'Success, Indicator Saved!')
            return HttpResponseRedirect('/indicators/editIndicator/' + id)
        else:
            print "not valid"
    else:
        value= get_object_or_404(Indicator, pk=id)
        form = IndicatorForm(instance=value) # An unbound form

    return render(request, 'indicators/indicator.html', {'form': form,'value':value})



def programIndicator(request,id):
    """
    View the indicators for a program
    """
    IndicatorFormSet = modelformset_factory(Indicator,extra=0)
    formset = IndicatorFormSet(queryset=Indicator.objects.all().filter(program__id=id))

    if request.method == 'POST':
        #deal with posting the data
        formset = IndicatorFormSet(request.POST)
        if formset.is_valid():
            #if it is not valid then the "errors" will fall through and be returned
            formset.save()
        return HttpResponseRedirect('/indicators/programIndicator/' + id)

    return render(request, 'indicators/programIndicator.html', {'formset': formset})

def editProgram(request,id):
    """
    Edit a program
    """
    if request.method == 'POST': # If the form has been submitted...
        form = ProgramForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            update = Program.objects.get(pk=id)
            form = ProgramForm(request.POST, instance=update)
            new = form.save(commit=True)
            return HttpResponseRedirect('indicators/editProgram/' + id)
        else:
            print "not valid"
    else:
        value= get_object_or_404(Program, pk=id)
        form = ProgramForm(instance=value) # An unbound form

    return render(request, 'indicators/program.html', {'form': form,'value':value})


def tool(request):

    return render(request, 'indicators/tool.html')

