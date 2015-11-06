import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User

from rest_framework import renderers, viewsets

from .models import Silo, LabelValueStore
from .serializers import *

def silo_data_api(request, id):
    if id <= 0:
        return HttpResponseBadRequest("The silo_id = %s is invalid" % id)

    data = LabelValueStore.objects(silo_id=id).to_json()
    json_data = json.loads(data)
    return JsonResponse(json_data, safe=False)


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
