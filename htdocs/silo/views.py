import datetime
import urllib2
import json
import base64
import csv
import operator

from django.http import HttpResponseRedirect
from .forms import ReadForm, UploadForm, SiloForm, MongoEditForm, NewColumnForm, EditColumnForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden,\
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest,\
    HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import RequestContext, Context
from django.db import models
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.db.models import Max
from django.db.models import F
from django.views.decorators.csrf import csrf_protect
import django_tables2 as tables
from django_tables2 import RequestConfig

from .models import Silo, Read, ReadType, ThirdPartyTokens, LabelValueStore, Tag
from .serializers import SiloSerializer, UserSerializer, ReadSerializer, ReadTypeSerializer

from .tables import define_table

from django.contrib.auth.decorators import login_required
from tola.util import siloToDict, combineColumns

from rest_framework import renderers, viewsets
from django.core.urlresolvers import reverse

from django.utils import timezone

# Edit existing silo meta data
@csrf_protect
@login_required
def editSilo(request, id):
    edited_silo = Silo.objects.get(pk=id)
    if request.method == 'POST':  # If the form has been submitted...
        tags = request.POST.getlist('tags')
        post_data = request.POST.copy()
        
        #empty the list but do not remove the dictionary element
        if tags: del post_data.getlist('tags')[:] 
        
        for i, t in enumerate(tags):
            if t.isdigit():
                post_data.getlist('tags').append(t)
            else:
                tag, created = Tag.objects.get_or_create(name=t, defaults={'owner': request.user})
                if created:
                    print("creating tag: %s " % tag)
                    tags[i] = tag.id    
                #post_data is a QueryDict in which each element is a list
                post_data.getlist('tags').append(tag.id)

        form = SiloForm(post_data, instance=edited_silo)
        if form.is_valid():
            updated = form.save()
            return HttpResponseRedirect('/silos/')
        else:
            messages.error(request, 'Invalid Form', fail_silently=False)
    else:
        form = SiloForm(instance=edited_silo)
    return render(request, 'silo/edit.html', {
        'form': form, 'silo_id': id,
    })

from silo.forms import *
import requests
from requests.auth import HTTPDigestAuth


def tolaCon(request):
    params = {'_method': 'OPTIONS'}
    #response = requests.post("https://tola-activity-dev.mercycorps.org/api/proposals/", params)
    response = requests.get("https://tola-activity-dev.mercycorps.org/api/")
    #jsondata = json.loads(response.content)['actions']['POST']
    jsondata = json.loads(response.content)
    print(jsondata)
    """
    data = {}
    for field in jsondata:
        data[field] = {'label': jsondata[field]['label'], 'type': jsondata[field]['type']}
    
    #print (data)
    """
    return render(request, 'silo/tolaactivity.html', {'data': jsondata })
    


@login_required
def saveAndImportRead(request):
    """ 
    Saves ONA read if not already in the db and then imports its data 
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("HTTP method, %s, is not supported" % request.method)

    read_type = ReadType.objects.get(read_type="JSON")
    name = request.POST.get('read_name', None)
    url = request.POST.get('read_url', None)
    owner = request.user
    description = request.POST.get('description', None)
    silo_id = None
    read = None
    silo = None
    provider = "ONA"
    try:
        silo_id = int(request.POST.get("silo_id", None))
    except Exception as e:
         print(e)
         return HttpResponse("Silo ID can only be an integer")

    try:
        read, created = Read.objects.get_or_create(read_name=name, owner=owner, 
            defaults={'read_url': url, 'type': read_type, 'description': description})
        if created: read.save()
    except Exception as e:
        print(e)
        return HttpResponse("Invalid name and/or URL")
    
    # Fetch the data from ONA
    ona_token = ThirdPartyTokens.objects.get(user=request.user, name=provider)
    response = requests.get(read.read_url, headers={'Authorization': 'Token %s' % ona_token.token})
    data = json.loads(response.content)

    existing_silo_cols = []
    new_cols = []
    show_mapping = False
    
    if silo_id <= 0:
        # create a new silo by the name of "name"
        silo = Silo(name=name, public=False, owner=owner)
        silo.save()
        silo.reads.add(read)
    else:
        # import into existing silo
        # Compare the columns of imported data with existing silo in case it needs merging
        silo = Silo.objects.get(pk=silo_id)
        lvs = json.loads(LabelValueStore.objects(silo_id=silo.id).to_json())
        for l in lvs:
            existing_silo_cols.extend(c for c in l.keys() if c not in existing_silo_cols)
        
        for row in data:
            new_cols.extend(c for c in row.keys() if c not in new_cols)
        
        for c in existing_silo_cols:
            if c == "silo_id" or c == "create_date": continue
            if c not in new_cols: show_mapping = True
            if show_mapping == True: 
                params = {'getSourceFrom':existing_silo_cols, 'getSourceTo':new_cols, 'from_silo_id':0, 'to_silo_id':silo.id}
                response = render_to_response("display/merge-column-form-inner.html", params, context_instance=RequestContext(request))
                response['show_mapping'] = '1'
                return response
    
    if silo:
        # import data into this silo
        num_rows = len(data)
        #loop over data and insert create and edit dates and append to dict
        for counter, row in enumerate(data):
            lvs = LabelValueStore()
            lvs.silo_id = silo.pk
            for new_label, new_value in row.iteritems():
                if new_label is not "" and new_label is not None and new_label is not "edit_date" and new_label is not "create_date":
                    setattr(lvs, new_label, new_value)
            lvs.create_date = timezone.now()
            result = lvs.save()
        if num_rows == (counter+1):
            combineColumns(silo_id)
            return HttpResponse("View silo data at <a href='/silo_detail/%s' target='_blank'>See your data</a>" % silo.pk)
    return HttpResponse(read.pk)

@login_required
def getOnaForms(request):
    data = {}
    auth_success = False
    ona_token = None
    form = None
    provider = "ONA"
    url_user_token = "https://ona.io/api/v1/user.json"
    url_user_forms = 'https://ona.io/api/v1/data'
    if request.method == 'POST':
        form = OnaLoginForm(request.POST)
        if form.is_valid():
            response = requests.get(url_user_token, auth=HTTPDigestAuth(request.POST['username'], request.POST['password']))
            if response.status_code == 401:
                messages.error(request, "Invalid username or password.")
            elif response.status_code == 200:
                auth_success = True
                token = json.loads(response.content)['api_token']
                ona_token, created = ThirdPartyTokens.objects.get_or_create(user=request.user, name=provider, token=token)
                if created: ona_token.save()
            else:
                messages.error(request, "A %s error has occured: %s " % (response.status_code, response.text))
    else:
        try:
            auth_success = True
            ona_token = ThirdPartyTokens.objects.get(name=provider, user=request.user)
        except Exception as e:
            auth_success = False
            form = OnaLoginForm()
    
    if ona_token and auth_success:
        onaforms = requests.get(url_user_forms, headers={'Authorization': 'Token %s' % ona_token.token})
        data = json.loads(onaforms.content)
        
    silos = Silo.objects.filter(owner=request.user)
    return render(request, 'silo/getonaforms.html', {
        'form': form, 'data': data, 'silos': silos
    })

@login_required
def providerLogout(request,provider):

    ona_token = ThirdPartyTokens.objects.get(user=request.user, name=provider)
    ona_token.delete()

    messages.error(request, "You have been logged out of your Ona account.  Any Tables you have created with this account ARE still available, but you must log back in here to update them.")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


#DELETE-SILO
@csrf_protect
def deleteSilo(request, id):
    owner = Silo.objects.get(id = id).owner
    
    if str(owner.username) == str(request.user):
        try:
            silo_to_be_deleted = Silo.objects.get(pk=id)
            silo_name = silo_to_be_deleted.name
            lvs = LabelValueStore.objects(silo_id=silo_to_be_deleted.id)
            num_rows_deleted = lvs.delete()
            silo_to_be_deleted.delete()
            messages.success(request, "Silo, %s, with all of its %s rows of data deleted successfully." % (silo_name, num_rows_deleted))
        except Silo.DoesNotExist as e:
            print(e)
        except Exception as es:
            print(es)
        return HttpResponseRedirect("/silos")
    else:
        messages.error(request, "You do not have permission to delete this silo")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

#READ VIEWS
@login_required
def home(request):
    """
    List of Current Read sources that can be updated or edited
    """
    try:
        user = User.objects.get(username__exact=request.user)
        get_reads = Read.objects.filter(owner=user)
    except User.DoesNotExist as e:
        messages.info(request, "There are no available silos")
        get_reads = None

    return render(request, 'read/home.html', {'getReads': get_reads, })

@login_required
def initRead(request):
    """
    Create a form to get feed info then save data to Read
    and re-direct to getJSON or uploadFile function
    """
    if request.method == 'POST':  # If the form has been submitted...
        form = ReadForm(request.POST, request.FILES)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save data to read
            new_read = form.save()
            id = str(new_read.id)
            if form.instance.file_data:
                redirect_var = "file/%s" % id
            else:
                redirect_var = "read/login"
            return HttpResponseRedirect('/' + redirect_var + '/')  # Redirect after POST to getLogin
        else:
            messages.error(request, 'Invalid Form', fail_silently=False)
    else:
        form = ReadForm()  # An unbound form

    return render(request, 'read/read.html', {
        'form': form,
    })

def showRead(request, id):
    """
    Show a read data source and allow user to edit it
    """
    get_read = Read.objects.get(pk=id)

    if request.method == 'POST':  # If the form has been submitted...
        form = ReadForm(request.POST, request.FILES, instance=get_read)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save data to read
            form.save()
            if form.instance.file_data:
                redirect_var = "file/" + id + "/"
            else:
                redirect_var = "read/login/?read_id=%s" % request.POST['read_id']
            return HttpResponseRedirect('/' + redirect_var)  # Redirect after POST to getLogin
        else:
            messages.error(request, 'Invalid Form', fail_silently=False)
    else:
        form = ReadForm(instance=get_read)  # An unbound form

    return render(request, 'read/read.html', {
        'form': form, 'read_id': id,
    })

@login_required
def uploadFile(request, id):
    """
    Upload CSV file and save its data
    """
    if request.method == 'POST':
        form = UploadForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            read_obj = Read.objects.get(pk=id)
            today = datetime.date.today()
            today.strftime('%Y-%m-%d')
            today = str(today)
            
            silo = None
            user = User.objects.get(username__exact=request.user)
            if request.POST.get("new_silo", None):
                silo = Silo(name=request.POST['new_silo'], owner=user, public=False, create_date=today)
                silo.save()
            else:
                silo = Silo.objects.get(id = request.POST["silo_id"])
        
            silo.reads.add(read_obj)
            silo_id = silo.id
    
            #create object from JSON String
            data = csv.reader(read_obj.file_data)
            
            labels = data.next() #First row of CSV should be Column Headers

            for row in data:
                lvs = LabelValueStore()
                lvs.silo_id = silo_id
                for col_counter, val in enumerate(row):
                    if labels[col_counter] is not "" and labels[col_counter] is not None: setattr(lvs, labels[col_counter], val) 
                lvs.create_date = timezone.now()
                lvs.save()
            
            return HttpResponseRedirect('/silo_detail/' + str(silo_id) + '/')
        else:
            messages.error(request, "There was a problem with reading the contents of your file" + form.errors)
            print form.errors

    user = User.objects.get(username__exact=request.user)
    # get all of the silo info to pass to the form
    get_silo = Silo.objects.filter(owner=user)
    
    # display login form
    return render(request, 'read/file.html', {
        'read_id': id, 'get_silo': get_silo,
    })


def getLogin(request):
    """
    Some services require a login provide user with a
    login to service if needed and select a silo
    """
    # get all of the silo info to pass to the form
    get_silo = Silo.objects.all()

    # display login form
    return render(request, 'read/login.html', {'get_silo': get_silo, 'read_id': request.GET.get('read_id', None)})

@login_required
def getJSON(request):
    """
    Get JSON feed info from form then grab data
    """
    if request.method == 'POST':
        # retrieve submitted Feed info from database
        read_obj = Read.objects.get(id = request.POST.get("read_id", None))

        # set date time stamp
        today = datetime.date.today()
        today.strftime('%Y-%m-%d')
        today = str(today)
        try:
            request2 = urllib2.Request(read_obj.read_url)
            #if they passed in a usernmae get auth info from form post then encode and add to the request header
            if request.POST['user_name']:
                username = request.POST['user_name']
                password = request.POST['password']
                base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
                request2.add_header("Authorization", "Basic %s" % base64string)
            #retrieve JSON data from formhub via auth info
            json_file = urllib2.urlopen(request2)
        except Exception as e:
            print e
            messages.error(request, 'Authentication Failed, Please double check your login credentials and URL!')

        silo = None
        
        user = User.objects.get(username__exact=request.user)
        if request.POST.get("new_silo", None):
            silo = Silo(name=request.POST['new_silo'], owner=user, public=False, create_date=today)
            silo.save()
        else:
            silo = Silo.objects.get(id = request.POST["silo_id"])
        
        silo.reads.add(read_obj)
        silo_id = silo.id
    
        #create object from JSON String
        data = json.load(json_file)
        json_file.close()
    
        #loop over data and insert create and edit dates and append to dict
        for row in data:
            lvs = LabelValueStore()
            lvs.silo_id = silo_id
            for new_label, new_value in row.iteritems():
                if new_value is not "" and new_label is not None and new_label is not "edit_date" and new_label is not "create_date":
                    setattr(lvs, new_label, new_value)
            lvs.create_date = timezone.now()
            lvs.save()
        messages.success(request, "Data imported correctly into MONGO")
        return HttpResponseRedirect('/silo_detail/' + str(silo_id) + '/')
    else:
        messages.error(request, "Invalid Request for importing JSON data")
        return HttpResponseRedirect("/")
#display
#INDEX
def index(request):

    # get all of the table(silo) info for logged in user and public data
    if request.user.is_authenticated():
        user = User.objects.get(username__exact=request.user)
        get_silos = Silo.objects.filter(owner=user)
    else:
        get_silos = None
    count_all = Silo.objects.count()
    count_max = count_all + (count_all * .10)
    get_public = Silo.objects.filter(public=1)
    return render(request, 'index.html',{'get_silos':get_silos,'get_public':get_public, 'count_all':count_all, 'count_max':count_max})


def toggle_silo_publicity(request):
    silo_id = request.GET.get('silo_id', None)
    silo = Silo.objects.get(pk=silo_id)
    silo.public = not silo.public
    silo.save()
    return HttpResponse("Your change has been saved")

#SILOS
@login_required
def listSilos(request):
    """
    Each silo is listed with links to details
    """
    user = User.objects.get(username__exact=request.user)
    
    #get all of the silos
    get_silos = Silo.objects.filter(owner=user).prefetch_related('reads')

    return render(request, 'display/silos.html',{'get_silos':get_silos})

#SILO-DETAIL Show data from source
@login_required
def siloDetail(request,id):
    """
    Show silo source details
    """
    owner = Silo.objects.get(id = id).owner
    public = Silo.objects.get(id = id).public

    if str(owner.username) == str(request.user) or public:
        table = LabelValueStore.objects(silo_id=id).to_json()
        decoded_json = json.loads(table)
        column_names = []
        #column_names = decoded_json[0].keys()
        for row in decoded_json:
            column_names.extend([k for k in row.keys() if k not in column_names])
    
        if decoded_json:
            silo = define_table(column_names)(decoded_json)
    
            #This is needed in order for table sorting to work
            RequestConfig(request).configure(silo)
    
            #send the keys and vars from the json data to the template along with submitted feed info and silos for new form
            return render(request, "display/stored_values.html", {"silo": silo, 'id':id})
        else:
            messages.error(request, "There is not data in Table with id = %s" % id)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You don't have the permission to see data in this table")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

#Add a new column on to a silo
@login_required
def newColumn(request,id):
    """
    FORM TO CREATE A NEW COLUMN FOR A SILO
    """
    silo = Silo.objects.get(id=id)
    form = NewColumnForm(initial={'silo_id': silo.id})

    if request.method == 'POST':
        form = NewColumnForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            client = MongoClient(uri)
            db = client.tola
            label = form.cleaned_data['new_column_name']
            value = form.cleaned_data['default_value']
            #insert a new column into the existing silo
            db.label_value_store.update_many(
                {"silo_id": silo.id},
                    {
                    "$set": {label: value},
                    },
                False
            )
            messages.info(request, 'Your column has been added', fail_silently=False)
        else:
            messages.error(request, 'There was a problem adding your column', fail_silently=False)
            print form.errors


    return render(request, "silo/new-column-form.html", {'silo':silo,'form': form})

#Add a new column on to a silo
@login_required
def editColumns(request,id):
    """
    FORM TO CREATE A NEW COLUMN FOR A SILO
    """
    silo = Silo.objects.get(id=id)
    doc = LabelValueStore.objects(silo_id=id).to_json()
    data = {}
    jsondoc = json.loads(doc)
    for item in jsondoc:
        for k, v in item.iteritems():
            #print("The key and value are ({}) = ({})".format(k, v))
            if k == "_id":
                #data[k] = item['_id']['$oid']
                pass
            elif k == "silo_id":
                silo_id = v
            elif k == "edit_date":
                edit_date = datetime.datetime.fromtimestamp(item['edit_date']['$date']/1000)
                data[k] = edit_date.strftime('%Y-%m-%d %H:%M:%S')
            elif k == "create_date":
                create_date = datetime.datetime.fromtimestamp(item['create_date']['$date']/1000)
                data[k] = create_date.strftime('%Y-%m-%d')
            else:
                data[k] = v
    form = EditColumnForm(initial={'silo_id': silo.id}, extra=data)

    if request.method == 'POST':
        form = EditColumnForm(request.POST or None, extra = data)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            client = MongoClient(uri)
            db = client.tola
            for label,value in form.cleaned_data.iteritems():
                #update the column name if it doesn't have delete in it
                if "_delete" not in label and str(label) != str(value) and label != "silo_id" and label != "suds" and label != "id":
                    #update a column in the existing silo
                    db.label_value_store.update_many(
                        {"silo_id": silo.id},
                            {
                            "$rename": {label: value},
                            },
                        False
                    )
                #if we see delete then it's a check box to delete that column
                elif "_delete" in label and value == 1:
                    column = label.replace("_delete", "")
                    db.label_value_store.update_many(
                        {"silo_id": silo.id},
                            {
                            "$unset": {column: value},
                            },
                        False
                    )


            messages.info(request, 'Updates Saved', fail_silently=False)
        else:
            messages.error(request, 'ERROR: There was a problem with your request', fail_silently=False)
            print form.errors


    return render(request, "silo/edit-column-form.html", {'silo':silo,'form': form})

#Delete a column from a table silo
@login_required
def deleteColumn(request,id,column):
    """
    DELETE A COLUMN FROM A SILO
    """
    silo = Silo.objects.get(id=id)
    client = MongoClient(uri)
    db = client.tola

    #delete a column from the existing table silo
    db.label_value_store.update_many(
        {"silo_id": silo.id},
            {
            "$unset": {column: ""},
            },
        False
    )

    messages.info(request, "Column has been deleted")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



#SHOW-MERGE FORM
@login_required
def mergeForm(request,id):
    """
    Merge different silos using a multistep column mapping form
    """
    getSource = Silo.objects.get(id=id)
    getSourceTo = Silo.objects.filter(owner=request.user)
    return render(request, "display/merge-form.html", {'getSource':getSource,'getSourceTo':getSourceTo})

#SHOW COLUMNS FOR MERGE FORM
def mergeColumns(request):
    """
    Step 2 in Merge different silos, map columns
    """
    from_silo_id = request.POST["from_silo_id"]
    to_silo_id = request.POST["to_silo_id"]

    lvs = json.loads(LabelValueStore.objects(silo_id__in = [from_silo_id, to_silo_id]).to_json())
    getSourceFrom = []
    getSourceTo = []
    for l in lvs:
        if from_silo_id == str(l['silo_id']):
            getSourceFrom.extend([k for k in l.keys() if k not in getSourceFrom])
        else:
            getSourceTo.extend([k for k in l.keys() if k not in getSourceTo])
    
    return render(request, "display/merge-column-form.html", {'getSourceFrom':getSourceFrom, 'getSourceTo':getSourceTo, 'from_silo_id':from_silo_id, 'to_silo_id':to_silo_id})

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
uri = 'mongodb://localhost/tola'
def doMerge(request):
    from_silo_id = request.POST['from_silo_id']
    to_silo_id = request.POST["to_silo_id"]

    try:
        from_silo_id = int(from_silo_id)
        to_silo_id = int(to_silo_id)
    except ValueError as e:
        from_silo_id = None
        to_silo_id = None
        print("The from_silo_id and/or the to_silo_id is not an integer")
    
    #conn = pymongo.Connection()
    #db = conn.tola
    client = MongoClient(uri)
    db = client.tola
    
    if from_silo_id != None and to_silo_id != None:
        for k in request.POST:
            if k != "silo_id" and k !=  "_id" and k != "to_silo_id" and k != "from_silo_id" and k != "csrfmiddlewaretoken": 
                from_field = request.POST.getlist(k)[0].lower()
                to_field = request.POST.getlist(k)[1].lower()
            
                if to_field == "Ignore":
                    "This field should be deleted from the silo_id = 'from_silo_id'"
                    #print ("FROM FIELD: %s and SILO_ID: %s" % (from_field, from_silo_id))
                    db.label_value_store.update_many( 
                        { "silo_id": from_silo_id }, 
                        { 
                            "$unset": {from_field: ""}, 
                        }, 
                        False #, False,  None, True 
                    )
                elif to_field == "0":
                    "Nothing should be done in this case because when the silo_id is updated to to_silo_id this field will become part of the to_silo_id "
                    pass
                else:
                    if from_field != to_field:
                        db.label_value_store.update_many(
                            { "silo_id": from_silo_id }, 
                            { 
                                "$rename": { from_field:  to_field },  
                                "$currentDate": { 'edit_date': True } 
                            }, 
                            False
                        )

        db.label_value_store.update_many( 
            { "silo_id": from_silo_id }, 
            { 
                "$set": { "silo_id": to_silo_id }, 
            }, 
            False #, False, None, True 
        )
        Silo.objects.filter(pk = from_silo_id).delete()
        
        combineColumns(to_silo_id)
    #messages.success(request, "Silos merged successfully")
    return HttpResponseRedirect("/silo_detail/%s" % to_silo_id)

#EDIT A SINGLE VALUE STORE
@login_required
def valueEdit(request,id):
    """
    Edit a value
    """
    doc = LabelValueStore.objects(id=id).to_json()
    data = {}
    jsondoc = json.loads(doc)
    silo_id = None
    for item in jsondoc:
        for k, v in item.iteritems():
            #print("The key and value are ({}) = ({})".format(k, v))
            if k == "_id":
                #data[k] = item['_id']['$oid']
                pass
            elif k == "silo_id":
                silo_id = v
            elif k == "edit_date":
                edit_date = datetime.datetime.fromtimestamp(item['edit_date']['$date']/1000)
                data[k] = edit_date.strftime('%Y-%m-%d %H:%M:%S')
            elif k == "create_date":
                create_date = datetime.datetime.fromtimestamp(item['create_date']['$date']/1000)
                data[k] = create_date.strftime('%Y-%m-%d')
            else:
                data[k] = v
    if request.method == 'POST': # If the form has been submitted...
        form = MongoEditForm(request.POST or None, extra = data) # A form bound to the POST data
        if form.is_valid():
            lvs = LabelValueStore.objects(id=id)[0]
            for lbl, val in form.cleaned_data.iteritems():
                if lbl != "id" and lbl != "silo_id" and lbl != "csrfmiddlewaretoken":
                    setattr(lvs, lbl, val)
            lvs.edit_date = timezone.now()
            lvs.save()
            return HttpResponseRedirect('/value_edit/' + id)
        else:
            print "not valid"
    else:
        form = MongoEditForm(initial={'silo_id': silo_id, 'id': id}, extra=data)

    return render(request, 'read/edit_value.html', {'form': form, 'silo_id': silo_id})

@login_required
def valueDelete(request,id):
    """
    Delete a value
    """
    silo_id = None
    lvs = LabelValueStore.objects(id=id)[0]
    owner = Silo.objects.get(id = lvs.silo_id).owner
    
    if str(owner.username) == str(request.user):
        silo_id = lvs.silo_id
        lvs.delete()
    else:
        messages.error(request, "You don't have the permission to delete records from this silo")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    messages.success(request, "Record deleted successfully")
    return HttpResponseRedirect('/silo_detail/%s/' % silo_id)

#FEED VIEWS
# API Classes

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SiloViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Silo.objects.all()
    serializer_class = SiloSerializer

class ReadViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Read.objects.all()
    serializer_class = ReadSerializer

class ReadTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ReadType.objects.all()
    serializer_class = ReadTypeSerializer

# End API Classes


def customFeed(request,id):
    """
    All tags in use on this system
    id = Silo
    """
    queryset = LabelValueStore.objects.exclude("silo_id").filter(silo_id=id).to_json()

    return render(request, 'feed/json.html', {"jsonData": queryset}, content_type="application/json")

def createFeed(request):
    """
    Create an XML or JSON Feed from a given Silo
    """
    getSilo = ValueStore.objects.filter(field__silo__id=request.POST['silo_id']).order_by('row_number')

    #return a dict with label value pair data
    formatted_data = siloToDict(getSilo)

    getFeedType = FeedType.objects.get(pk = request.POST['feed_type'])

    if getFeedType.description == "XML":
        xmlData = serialize(formatted_data)
        return render(request, 'feed/xml.html', {"xml": xmlData}, content_type="application/xhtml+xml")
    elif getFeedType.description == "JSON":
        jsonData = simplejson.dumps(formatted_data)
        return render(request, 'feed/json.html', {"jsonData": jsonData}, content_type="application/json")


from collections import OrderedDict
def export_silo(request, id):
    
    silo_name = Silo.objects.get(id=id).name
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % silo_name
    writer = csv.writer(response)

    silo_data = LabelValueStore.objects(silo_id=id)
    data = []
    num_cols = 0
    cols = OrderedDict()
    if silo_data:
        num_rows = len(silo_data)
        
        for row in silo_data:
            for i, col in enumerate(row):
                if col not in cols.keys():
                    num_cols = num_cols + 1
                    cols[col] = num_cols
        
        # Convert OrderedDict to Python list so that it can be written to CSV writer.
        cols = list(cols)
        writer.writerow(list(cols))
        
        # Populate a 2x2 list structure that corresponds to the number of rows and cols in silo_data
        for i in xrange(num_rows): data += [[0]*num_cols]        
        
        for r, row in enumerate(silo_data):
            for col in row:
                # Map values to column names and place them in the correct position in the data array
                data[r][cols.index(col)] = row[col]
            writer.writerow(data[r])
    return response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import GoogleCredentialsModel
from apiclient.discovery import build
import os, logging, httplib2, json, datetime

import gdata.spreadsheets.client


from django.http import JsonResponse

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds',
    redirect_uri=settings.GOOGLE_REDIRECT_URL)
    #redirect_uri='http://localhost:8000/oauth2callback/')


def export_to_google_spreadsheet(credential_json, silo_id, spreadsheet_key):


    # Create OAuth2Token for authorizing the SpreadsheetClient
    token = gdata.gauth.OAuth2Token(
        client_id = credential_json['client_id'],
        client_secret = credential_json['client_secret'],
        scope = 'https://spreadsheets.google.com/feeds',
        user_agent = "TOLA",
        access_token = credential_json['access_token'],
        refresh_token = credential_json['refresh_token'])

    # Instantiate the SpreadsheetClient object
    sp_client = gdata.spreadsheets.client.SpreadsheetsClient(source="TOLA")

    # authorize the SpreadsheetClient object
    sp_client = token.authorize(sp_client)
    #print(sp_client)
    
    
    # Create a WorksheetQuery object to allow for filtering for worksheets by the title
    worksheet_query = gdata.spreadsheets.client.WorksheetQuery(title="Sheet1", title_exact=True)
    
    
    # Get a feed of all worksheets in the specified spreadsheet that matches the worksheet_query
    worksheets_feed = sp_client.get_worksheets(spreadsheet_key, query=worksheet_query)
    #print("worksheets_feed: %s" % worksheets_feed)
    
    
    # Retrieve the worksheet_key from the first match in the worksheets_feed object
    worksheet_key = worksheets_feed.entry[0].id.text.rsplit("/", 1)[1]
    #print("worksheet_key: %s" % worksheet_key)
    
    silo_data = LabelValueStore.objects(silo_id=silo_id)
    
    # Create a CellBatchUpdate object so that all cells update is sent as one http request
    batch = gdata.spreadsheets.data.BuildBatchCellsUpdate(spreadsheet_key, worksheet_key)
    
    col_index = 0
    row_index = 1
    col_info = {}
    
    for row in silo_data:
        row_index = row_index + 1
        for i, col_name in enumerate(row):
            if col_name not in col_info.keys():
                col_index = col_index + 1
                col_info[col_name] = col_index
                batch.add_set_cell(1, col_index, col_name) #Add column names
            #print("%s = %s - %s: %s" % (col_info[col_name], col_name, type(row[col_name]),  row[col_name]))
            
            val = row[col_name]
            if col_name != "isd":
                try:
                    #val = str(val)#.encode('ascii', 'ignore')
                    val = val.encode('ascii', 'xmlcharrefreplace')
                except Exception as e:
                    try:
                        val = str(val)
                    except Exception as e1:                        
                        print(e)
                        print(val)
                        pass
            
                batch.add_set_cell(row_index, col_info[col_name], val)
    
    # By default a blank Google Spreadsheet has 26 columns but if our data has more column
    # then add more columns to Google Spreadsheet otherwise there would be a 500 Error!
    if col_index and col_index > 26:
        worksheet = worksheets_feed.entry[0]
        worksheet.col_count.text = str(col_index)

        # Send the worksheet update call to Google Server
        sp_client.update(worksheet, force=True)

    try:
        # Finally send the CellBatchUpdate object to Google
        sp_client.batch(batch, force=True)
    except Exception as e:
        print("ERROR: %s" % e)
        return False

    return True


@login_required
def export_gsheet(request, id):
    gsheet_endpoint = None
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        #return HttpResponseRedirect(authorize_url)
        messages.error(request, "You must first <a href='%s'>authorize</a> before you could export to Gooogle Spreadsheet." % authorize_url)
        return JsonResponse({"redirect_url": authorize_url})

    credential_json = json.loads(credential.to_json())

    user = User.objects.get(username__exact=request.user)
    gsheet_endpoint = None
    read_type = ReadType.objects.get(read_type="Google Spreadsheet")
    try:
        gsheet_endpoint = Read.objects.get(silos__id=id, type=read_type, silos__owner=user.id, read_name='Google')
    except Read.MultipleObjectsReturned:
        print("multiple records exist and that should NOT be the case")
    except Read.DoesNotExist:
        print("Remote End point does not exist; creating one...")
        url = request.GET.get('link', None)
        file_id = request.GET.get('resource_id', None)
        if url == None:
            print ("No link provided for the remote end point")
        if file_id == None:
            print("No file id is available")
        
        gsheet_endpoint = Read(read_name="Google", type=read_type, owner=user, read_url=url, resource_id=file_id)
        gsheet_endpoint.save()
        silo = Silo.objects.get(id=id)
        silo.reads.add(gsheet_endpoint)
        silo.save()
    except Exception as e:
        print(e)

    #print("about to export to gsheet: %s" % gsheet_endpoint.resource_id)
    if export_to_google_spreadsheet(credential_json, id, gsheet_endpoint.resource_id) == True:
        link = "Your exported data is available at <a href=" + gsheet_endpoint.read_url + " target='_blank'>Google Spreadsheet</a>"
        messages.success(request, link)
    else:
        messages.error(request, 'Something went wrong; try again; here we go.')
    return JsonResponse({"success": True})

@login_required
def export_new_gsheet(request, id):
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        #print("STEP1 authorize_url: %s", authorize_url)
        return HttpResponseRedirect(authorize_url)

    credential_json = json.loads(credential.to_json())
    silo_id = id
    silo_name = Silo.objects.get(pk=silo_id).name

    http = httplib2.Http()

    # Authorize the http object to be used with "Drive API" service object
    http = credential.authorize(http)

    # Build the Google Drive API service object
    service = build("drive", "v2", http=http)

    # The body of "insert" API call for creating a blank Google Spreadsheet
    body = {
        'title': silo_name,
        'description': "Exported Data from Mercy Corps TolaData",
        'mimeType': "application/vnd.google-apps.spreadsheet"
    }

    # Create a new blank Google Spreadsheet file in user's Google Drive
    google_spreadsheet = service.files().insert(body=body).execute()

    # Get the spreadsheet_key of the newly created Spreadsheet
    spreadsheet_key = google_spreadsheet['id']
    #print(spreadsheet_key)
    if export_to_google_spreadsheet(credential_json, silo_id, spreadsheet_key) == True:
        link = "Your exported data is available at <a href=" + google_spreadsheet['alternateLink'] + " target='_blank'>Google Spreadsheet</a>"
        messages.success(request, link)
    else:
        messages.error(request, 'Something went wrong; try again.')
    return HttpResponseRedirect("/silos/")

@login_required
def oauth2callback(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()

    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    #print(credential.to_json())
    return HttpResponseRedirect("/")


