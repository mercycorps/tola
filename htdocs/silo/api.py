from silo.models import Silo, LabelValueStore
from django.http import HttpResponseBadRequest, JsonResponse
import json

def silo_data_api(request, id):
    if id <= 0:
        return HttpResponseBadRequest("The silo_id = %s is invalid" % id)

    data = LabelValueStore.objects(silo_id=id).to_json()
    json_data = json.loads(data)
    return JsonResponse(json_data, safe=False)