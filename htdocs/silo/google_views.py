import os, logging, httplib2, json, datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import GoogleCredentialsModel
from apiclient.discovery import build
import gdata.spreadsheets.client

from .models import Silo, Read, ReadType, ThirdPartyTokens, LabelValueStore, Tag

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds',
    redirect_uri=settings.GOOGLE_REDIRECT_URL)
    #redirect_uri='http://localhost:8000/oauth2callback/')


def picker_view(request):
    return render(request, 'picker.html')

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
    read_url = request.GET.get('link', None)
    file_id = request.GET.get('resource_id', None)
    if read_url == None or file_id == None:
        messages.error(request, "A Google Spreadsheet is not selected to import data to it.")
        return HttpResponseRedirect(reverse('listSilos'))

    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        #FLOW.params.update({'redirect_uri_after_step2': "/export_gsheet/%s/?link=%s&resource_id=%s" % (id, read_url, file_id)})
        request.session['redirect_uri_after_step2'] = "/export_gsheet/%s/?link=%s&resource_id=%s" % (id, read_url, file_id)
        return HttpResponseRedirect(authorize_url)

    credential_json = json.loads(credential.to_json())
    user = User.objects.get(username__exact=request.user)
    gsheet_endpoint = None
    read_type = ReadType.objects.get(read_type="Google Spreadsheet")
    try:
        gsheet_endpoint = Read.objects.get(silos__id=id, type=read_type, silos__owner=user.id, read_name='Google')
    except Read.MultipleObjectsReturned:
        gsheet_endpoints = Read.objects.get(silos__id=id, type=read_type, silos__owner=user.id, read_name='Google')
        for endpoint in gsheet_endpoints:
            if endpoint.resource_id:
                gsheet_endpoint = endpoint
    except Read.DoesNotExist:
        gsheet_endpoint = Read(read_name="Google", type=read_type, owner=user)
        gsheet_endpoint.save()
        silo = Silo.objects.get(id=id)
        silo.reads.add(gsheet_endpoint)
        silo.save()
    except Exception as e:
        messages.error(request, "An error occured: %" % e.message)

    if gsheet_endpoint.resource_id == "None" or gsheet_endpoint.resource_id == None:
        gsheet_endpoint.resource_id = file_id
        gsheet_endpoint.read_url = read_url
        gsheet_endpoint.save()

    #print("about to export to gsheet: %s" % gsheet_endpoint.resource_id)
    if export_to_google_spreadsheet(credential_json, id, gsheet_endpoint.resource_id) == True:
        link = "Your exported data is available at <a href=" + gsheet_endpoint.read_url + " target='_blank'>Google Spreadsheet</a>"
        messages.success(request, link)
    else:
        messages.error(request, 'Something went wrong.')
    return HttpResponseRedirect(reverse('listSilos'))

@login_required
def export_new_gsheet(request, id):
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        #FLOW.params.update({'redirect_uri_after_step2': "/export_new_gsheet/%s/" % id})
        request.session['redirect_uri_after_step2'] = "/export_new_gsheet/%s/" % id
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
    return HttpResponseRedirect(reverse('listSilos'))

@login_required
def oauth2callback(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, str(request.GET['state']), request.user):
        return  HttpResponseBadRequest()

    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(GoogleCredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    #print(credential.to_json())
    redirect_url = request.session['redirect_uri_after_step2']
    return HttpResponseRedirect(redirect_url)