from silo.models import Silo, DataField, ValueStore
from read.models import Read, ReadType
from .serializers import SiloSerializer, DataFieldSerializer, ValueStoreSerializer, UserSerializer, ReadSerializer, ReadTypeSerializer

from django.contrib.auth.decorators import login_required
import json as simplejson
from tola.util import siloToDict

from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User


from rest_framework import renderers,viewsets

import operator
import csv


from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden,\
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest,\
    HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render

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

class FeedViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Silo.objects.all()
    serializer_class = SiloSerializer


class DataFieldViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = DataField.objects.all()
    serializer_class = DataFieldSerializer


class ValueStoreViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ValueStore.objects.all()
    serializer_class = ValueStoreSerializer

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
    #get all of the data fields for the silo
    #queryset = DataField.objects.filter(silo__id=id)
    queryset = ValueStore.objects.filter(field__silo=id).order_by('row_number','id').select_related('field').values('char_store', 'field__name')

    formatted_data = []

    #loop over the labels and populate the first list with lables
    for row in queryset:
        #append the label to the list
        formatted_data.append(row['field__name'])

        formatted_data.append(row['char_store'])

    #output list to json
    jsonData = simplejson.dumps(formatted_data)
    return render(request, 'feed/json.html', {"jsonData": jsonData}, content_type="application/json")

#Feeds
def listFeeds(request):
    """
    Get all Silos and Link to REST API pages
    """
    #get all of the silos
    getSilos = Silo.objects.all()

    return render(request, 'feed/list.html',{'getSilos': getSilos})

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

def export_silo(request, id):
    """
    Export a silo to a CSV file
    id = Silo
    """
    getSiloRows = ValueStore.objects.all().filter(field__silo__id=id).values('row_number').distinct().order_by('row_number')
    getColumns = DataField.objects.all().filter(silo__id=id).values('name').distinct()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    getSiloName = Silo.objects.get(pk=id)
    file = getSiloName.name + ".csv"

    response['Content-Disposition'] = 'attachment; filename=file'

    writer = csv.writer(response)

    #create a list of column names
    column_list = []
    value_list = []
    for column in getColumns:
        column_list.append(str(column['name']))
    #print the list of column names
    writer.writerow(column_list)

    #loop over each row of the silo
    for row in getSiloRows:
        getSiloColumns = ValueStore.objects.all().filter(field__silo__id=id, row_number=str(row['row_number'])).values_list('field__name', flat=True).distinct()
        print "row"
        print str(row['row_number'])
        #get a column value for each column in the row
        for x in column_list:
            if x in getSiloColumns:
                print x
                getSiloValues = ValueStore.objects.get(field__silo__id=id, row_number=str(row['row_number']), field__name=x)
                value_list.append(str(getSiloValues.char_store.encode(errors="ignore")))
            else:
                value_list.append("")


        #print the row
        writer.writerow(value_list)
        value_list = []


    return response


def createDynamicModel(request):
    """
    Create an XML or JSON Feed from a given Silo
    """
    getSilo = Silo.objects.filter(silo_id=request.POST['silo_id'])
    getValues = ValueStore.objects.filter(field__silo__id=request.POST['silo_id'])
    getFields = DataField.objects.filter(field__silo__id=request.POST['silo_id'])

    #return a dict with label value pair data
    formatted_data = siloToModel(getSilo['name'],getFields['name'])

    getFeedType = FeedType.objects.get(pk = request.POST['feed_type'])

    if getFeedType.description == "XML":
        xmlData = serialize(formatted_data)
        return render(request, 'feed/xml.html', {"xml": xmlData}, content_type="application/xhtml+xml")
    elif getFeedType.description == "JSON":
        jsonData = simplejson.dumps(formatted_data)
        return render(request, 'feed/json.html', {"jsonData": jsonData}, content_type="application/json")

from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import GoogleCredentialsModel
from apiclient.discovery import build
import os, logging, httplib2, json, datetime

import gdata.spreadsheets.client

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds',
    redirect_uri='http://localhost:8000/oauth2callback/')

@login_required
def google_export(request, id):
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        # 
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
        # Uncomment the line below if you want to create a new Google Spreadsheet
        google_spreadsheet = service.files().insert(body=body).execute()
        
        # Get the spreadsheet_key of the newly created Spreadsheet
        spreadsheet_key = google_spreadsheet['id']
        
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
        
        # Create a WorksheetQuery object to allow for filtering for worksheets by the title
        worksheet_query = gdata.spreadsheets.client.WorksheetQuery(title="Sheet1", title_exact=True)
        
        # Get a feed of all worksheets in the specified spreadsheet that matches the worksheet_query
        worksheets_feed = sp_client.get_worksheets(spreadsheet_key, query=worksheet_query)
        
        # Retrieve the worksheet_key from the first match in the worksheets_feed object
        worksheet_key = worksheets_feed.entry[0].id.text.rsplit("/", 1)[1]
        
        silo_data = ValueStore.objects.filter(field__silo__id=silo_id).order_by("row_number")
        num_cols = len(silo_data)
        
        # By default a blank Google Spreadsheet has 26 columns but if our data has more column
        # then add more columns to Google Spreadsheet otherwise there would be a 500 Error!
        if num_cols and num_cols > 26:
            worksheet = worksheets_feed.entry[0]
            worksheet.col_count.text = str(num_cols)
            
            # Send the worksheet update call to Google Server
            sp_client.update(worksheet, force=True)
        
        # Create a CellBatchUpdate object so that all cells update is sent as one http request
        batch = gdata.spreadsheets.data.BuildBatchCellsUpdate(spreadsheet_key, worksheet_key)
        
        # Get all of the column names for the current silo_id
        column_names = DataField.objects.filter(silo_id=1).values_list('name', flat=True)
        
        # Add column names to the batch object
        for i, col_name in enumerate(column_names):
            row_index = 1
            col_index = i + 1
            batch.add_set_cell(row_index, col_index, col_name)
        
        # Populate the CellBatchUpdate object with data
        for row in silo_data:
            row_index = row.row_number + 1
            col_index = row.field.id
            value = row.char_store
            batch.add_set_cell(row_index, col_index, value)
        
        # Finally send the CellBatchUpdate object to Google
        sp_client.batch(batch, force=True)

        link = "Your exported data is available at <a href=" + google_spreadsheet['alternateLink'] + " target='_blank'>Google Spreadsheet</a>"
        messages.success(request, link)
    return HttpResponseRedirect("/")

@login_required
def oauth2callback(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()

    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    #print(credential.to_json())
    return HttpResponseRedirect("/")
