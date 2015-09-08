from django.forms import widgets
from rest_framework import serializers
from silo.models import Silo, Read, ReadType
from django.contrib.auth.models import User


class SiloSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Silo
        fields = ('owner', 'name', 'reads', 'description', 'create_date', 'id')
        depth =1


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ReadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Read
        fields = ('owner', 'type', 'read_name', 'read_url')


class ReadTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReadType
        fields = ( 'read_type', 'description')