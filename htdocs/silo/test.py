"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string

from django.test import TestCase
from django.test import Client
from django.test import RequestFactory

from silo.views import *
from silo.models import *
from silo.forms import *

class ReadTest(TestCase):
    fixtures = ['fixtures/read_types.json']
    show_read_url = '/show_read/'
    new_read_url = '/new_read/'
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="joe", email="joe@email.com", password="tola123")
    
    def test_new_read_get(self):
        """ Test the GET view of initRead view """
        request = self.factory.get(self.new_read_url)
        request.user = self.user
        response = initRead(request)
        self.assertEqual(response.status_code, 200)
    
    def test_new_read_post(self):
        read_type = ReadType.objects.get(read_type="JSON")
        upload_file = open('test.csv', 'rb')
        params = {
            'owner': self.user.pk,
            'type': read_type.pk,
            'read_name': 'TEST READ SOURCE',
            'description': 'TEST DESCRIPTION for test read source',
            'read_url': 'https://www.lclark.edu',
            'resource_id':'testsssszzz',
            'create_date': '2015-06-24 20:33:47',
            'file_data': upload_file,
        }
        request = self.factory.post(self.new_read_url, data = params)
        request.user = self.user
        
        response = initRead(request)
        if response.status_code == 302:
            if "/read/login" in response.url or "/file/" in response.url:
                self.assertEqual(response.url, response.url)
            else:
                self.assertEqual(response.url, "/read/login or /file/x")
        else:
            self.assertEqual(response.status_code, 200)
    
        # Now test the show_read view to make sure that I can retrieve the objec
        # that just got created using the POST method above.
        source = Read.objects.get(read_name='TEST READ SOURCE')
        response = self.client.get(self.show_read_url + str(source.pk) + "/")
        self.assertEqual(response.status_code, 200)


class SiloTest(TestCase):
    fixtures = ['fixtures/read_types.json']
    silo_edit_url = "/silo_edit/"
    upload_csv_url = "/file/"
    silo_detail_url = "/silo_detail/"
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="bob", email="bob@email.com", password="tola123")
        self.today = datetime.date.today()
        self.today.strftime('%Y-%m-%d')
        self.today = str(self.today)
    
    def test_new_silo(self):
        # Create a New Silo
        silo = Silo.objects.create(name="Test Silo", owner=self.user, public=False, create_date=self.today)
        self.assertEqual(silo.pk, 1)
        
        # Fetch the silo that just got created above
        request = self.factory.get(self.silo_edit_url)
        request.user = self.user
        response = editSilo(request, silo.pk)
        self.assertEqual(response.status_code, 200)
        
        # update the silo that just got created above
        params = {
            'owner': self.user.pk,
            'name': 'Test Silo Updated',
            'description': 'Adding this description in a unit-test.',
        }
        request = self.factory.post(self.silo_edit_url, data = params)
        request.user = self.user
        request._dont_enforce_csrf_checks = True
        response = editSilo(request, silo.pk)
        if response.status_code == 302:
            self.assertEqual(response.url, "/display")
        else:
            self.assertEqual(response.status_code, 200)
        
    def test_new_silodata(self):
        read_type = ReadType.objects.get(read_type="CSV")
        upload_file = open('test.csv', 'rb')
        read = Read.objects.create(owner=self.user, type=read_type, 
            read_name="TEST CSV IMPORT", description="unittest", create_date='2015-06-24 20:33:47', 
            file_data=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        params =  {
            "read_id": read.pk,
            "new_silo": "Test CSV Import",
        }
        request = self.factory.post(self.upload_csv_url, data = params)
        request.user = self.user
        request._dont_enforce_csrf_checks = True
        response = uploadFile(request, read.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/silo_detail/", response.url)
        
        silo = Silo.objects.get(name="Test CSV Import")
        request = self.factory.get(self.silo_detail_url)
        request.user = self.user
        
        response = siloDetail(request, silo.pk)
        self.assertEqual(response.status_code, 200)
        
        
    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, index)
    
    def test_read_form(self):
        read_type = ReadType.objects.get(read_type="CSV")
        upload_file = open('test.csv', 'rb')
        params = {
            'owner': self.user.pk,
            'type': read_type.pk,
            'read_name': 'TEST READ SOURCE',
            'description': 'TEST DESCRIPTION for test read source',
            'read_url': 'https://www.lclark.edu',
            'resource_id':'testsssszzz',
            'create_date': '2015-06-24 20:33:47',
            #'file_data': upload_file,
        }
        file_dict = {'file_data': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = ReadForm(params, file_dict)
        self.assertTrue(form.is_valid())

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