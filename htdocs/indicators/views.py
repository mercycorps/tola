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
from models import Program,Indicator
from indicators.forms import ProgramForm, IndicatorForm, ProgramIndicatorForm
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory


def home(request):
    """
    Get all of the Programs
    """
    getPrograms = Program.objects.all()

    return render(request, 'indicators/home.html',{'getPrograms':getPrograms})

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
            return HttpResponseRedirect('indicators/indicator/' + id)
        else:
            print "not valid"
    else:
        value= get_object_or_404(Indicator, pk=id)
        form = IndicatorForm(instance=value) # An unbound form

    return render(request, 'indicators/indicator.html', {'form': form,'value':value})


def program(request):
    """
    Create a program
    """
    if request.method == 'POST': # If the form has been submitted...
        form = ProgramForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            new = form.save()
            return HttpResponseRedirect('/indicators/indicator') # Redirect after POST to getLogin
    else:
        form = ProgramForm() # An unbound form

    return render(request, 'indicators/program.html', {'form': form,})

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

