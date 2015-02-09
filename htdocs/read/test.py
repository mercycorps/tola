from django.test import TestCase
from .models import Read, ReadType
from django.utils import timezone
from django.contrib.auth.models import User


# models test
class ReadTest(TestCase):

    read_type_4_test = ReadType.objects.latest('id')
    owner = User.objects.get(pk=1)

    def create_read(self, read_name="only a test", type=read_type_4_test, read_url="http://www.formhub.org", description="Test description", owner=owner):
        return Read.objects.create(read_name=read_name, type=type, read_url=read_url, description=description, create_date=timezone.now(), owner=owner)

    def test_read_creation(self):
        r = self.create_read()
        self.assertTrue(isinstance(r, Read))
        self.assertEqual(r.__unicode__(), r.read_title)