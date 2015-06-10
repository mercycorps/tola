import calendar
import time
import datetime
import hmac
import urllib2
import json
import base64
import urlparse
import hashlib


from django.http import HttpResponseRedirect, Http404
from silo.models import Silo, Read
from .models import Token
from forms import ReadForm, TokenFormSet, EditTokenFormSet
from django.shortcuts import render_to_response
from django.shortcuts import render

"""
List of Current Read sources that can be updated or edited
"""
def home(request):
    getReads = Read.objects.all()

    return render(request, 'readtoken/home.html', {'getReads': getReads, })


"""
Select a silo to store a new data set
"""
def getSilo(request, id):
    # get all of the silo info to pass to the form
    get_silo = Silo.objects.all()

    # display login form
    return render(request, 'readtoken/silo.html', {'get_silo': get_silo, 'read_id': id})


"""
Create a form to get feed info then save data to Read 
and re-direct to getJSON function
"""
def initRead(request):

    form = ReadForm
    formset = TokenFormSet(instance=Read())  # An unbound form

    if request.method == 'POST':  # If the form has been submitted...
        form = ReadForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save data to read
            read = form.save()
            read_id = read.pk

            token_formset = TokenFormSet(request.POST, instance=read)
            if token_formset.is_valid():
                token_formset.save()
                return HttpResponseRedirect('/readtoken/silo/' + str(read_id))  # Redirect after POST to getLogin


    return render(request, 'readtoken/read.html', {
        'form': form, 'formset': formset, 'read_id': id,
    })

"""
Show a read data source and allow user to edit it
"""
def showRead(request, id):
    getRead = Read.objects.get(pk=id)

    form = ReadForm(instance=getRead)
    formset = EditTokenFormSet(instance=getRead)  # An unbound form

    if request.method == 'POST':  # If the form has been submitted...
        form = EditTokenFormSet(request.POST, instance=getRead)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save data to read
            form.save()

        return HttpResponseRedirect('/readtoken/silo/' + str(getRead.id))  # Redirect after POST to getLogin

    return render(request, 'readtoken/edit_read.html', {
        'form': form, 'formset': formset, 'read_id': id,
    })


"""
Get JSON feed info from form then grab data
"""
def getJSON(request):
    # retrieve submitted Feed info from database
    read_obj = Read.objects.get(id=request.POST['id'])
    token_obj = Token.objects.get(read__id=request.POST['id'])

    # set date time stamp
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    today = str(today)

    #print tko.query
    print read_obj.owner_id

    #New silo or existing
    if request.POST['new_silo']:
        new_silo = Silo(name=request.POST['new_silo'], source=read_obj, create_date=today, owner_id=read_obj.owner_id)
        new_silo.save()
        silo_id = new_silo.id
    else:
        print "EXISTING"
        silo_id = request.POST['silo_id']


    #get auth info from form post then encode and add to the request header
    token = token_obj.read_token
    ms = int(round(time.time() * 1000))
    secret = bytes(token_obj.read_secret).encode("utf-8")

    #url =http://demo.devresults.com/api + path + token + timestamp
    apiUrl = read_obj.read_url + "/?t=%s&ms=%s" % (token, ms)

    #parse url into components
    uri = urlparse.urlparse(apiUrl)
    queryValues = urlparse.parse_qs(uri.query)

    #sort keys from query string
    sortedKeys = queryValues.keys()
    sortedKeys.sort()

    signature = reduce(lambda x, y: x + y,
        map(lambda key: key + "|" + queryValues[key][0] + "|", sortedKeys))
    sigbytes = bytes(signature).encode("utf-8")

    hashedSignature = hmac.new(secret, sigbytes, digestmod=hashlib.sha256).hexdigest()
    apiUrl += ("&s=%s" % hashedSignature)

    print apiUrl
    #retrieve JSON data from formhub via auth info
    json_file = urllib2.urlopen(apiUrl)

    #create object from JSON String
    data = json.load(json_file)
    json_file.close()
    #loop over data and insert create and edit dates and append to dict
    for row in data:
        for new_label, new_value in row.iteritems():
            if new_value is not "" and new_label is not None:
                #save to DB
                saveJSON(new_value, new_label, silo_id)

    #get fields to display back to user for verification
    getFields = DataField.objects.filter(silo_id=silo_id)

    #send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render_to_response("readtoken/show-columns.html", {'getFields': getFields, 'silo_id': silo_id})


"""
Set the PK for each row by allowing the user to select a column
"""
def updateUID(request):
    for row in request.POST['is_uid']:
        update_uid = DataField.objects.update(is_uid=1)

    get_silo = ValueStore.objects.all().filter(field__silo_id=request.POST['silo_id'])

    return render(request, "readtoken/show-data.html", {'get_silo': get_silo})


"""
Function call no template associated with this
Save JSON file data into data store and silo
"""
def saveJSON(new_value, new_label, silo_id):
    # Need a silo set object to gather silos into programs
    current_silo = Silo.objects.get(pk=silo_id)
    # set date time stamp
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    today = str(today)
    if new_value is not "" and new_value is not None:
        new_field = DataField(silo=current_silo, name=new_label, create_date=today, edit_date=today)
        new_field.save()
        #get the field id
        latest = DataField.objects.latest('id')

        new_value = ValueStore(field_id=latest.id, char_store=new_value, create_date=today, edit_date=today)

        new_value.save()
 
