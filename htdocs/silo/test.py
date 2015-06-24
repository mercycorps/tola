"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from silo.views import *


class LoginTest(TestCase):
    fixtures = ['fixtures/read_types.json']
    
    read_url = '/new_read/'
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="joe", email="joe@email.com", password="tola123")
    
    def test_login(self):    
        c = Client()
        response = c.post('/accounts/login/', {'username': 'jj', 'password': 'kkk'})
        self.assertEqual(response.status_code, 200)
    
    def test_new_read_get(self):
        request = self.factory.get(self.read_url)
        request.user = self.user
        response = initRead(request)
        self.assertEqual(response.status_code, 200)
    
    def test_new_read_post(self):
        read_type = ReadType.objects.get(read_type="JSON")
        params = {
            'owner': self.user.pk,
            'type': read_type.pk,
            'read_name': 'TEST READ SOURCE',
            'description': 'TEST DESCRIPTION for test read source',
            'read_url': 'https://www.lclark.edu',
            'resource_id':'testsssszzz',
            'create_date': '2015-06-24 20:33:47',
        }
        request = self.factory.post(self.read_url, data = params)
        request.user = self.user
        
        response = initRead(request)
        if response.status_code == 302:
            if "/read/login" in response.url or "/file/" in response.url:
                self.assertEqual(response.url, response.url)
            else:
                self.assertEqual(response.url, "/read/login or /file/x")
        else:
            self.assertEqual(response.status_code, 200)
        print(response)
    
    def test_new_silo(self):
        pass
    
    def test_update_silo(self):
        pass
    
    def test_view_silo(self):
        pass
    
    def test_new_silodata(self):
        pass
    
    def test_delete_data_from_silodata(self):
        pass
    
    def test_update_data_in_silodata(self):
        pass
        
    def test_read_data_from_silodata(self):
        pass
    
    def test_delete_silodata(self):
        pass
    
    def test_delete_silo(self):
        pass