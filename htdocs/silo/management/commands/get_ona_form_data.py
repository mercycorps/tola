import json

from django.core.management.base import BaseCommand, CommandError
from silo.models import *

import requests
from requests.auth import HTTPDigestAuth


class Command(BaseCommand):
    help = 'Fetches a specific form data from ONA'

    def add_arguments(self, parser):
        parser.add_argument("-u", "--username", type=str, required=True)
        parser.add_argument('--read_ids', nargs='*', type=int)
        parser.add_argument('--silo_id', nargs='?', type=int)

    def handle(self, *args, **options):
        silo = None
        read = None
        silo_id = options['silo_id']
        username = options['username']
        user = User.objects.get(username__exact=username)
        reads = Read.objects.filter(owner=user)

        try:
            silo = Silo.objects.get(pk=silo_id)
        except Silo.DoesNotExist:
            raise CommandError('Silo "%s" does not exist' % silo_id)

        for read_id in options['read_ids']:
            try:
                read = reads.filter(pk=read_id)[0]
            except Read.DoesNotExist:
                raise CommandError('Read "%s" does not exist' % read_id)

            # Fetch the data from ONA
            ona_token = ThirdPartyTokens.objects.get(user=user.pk, name="ONA")
            response = requests.get(read.read_url, headers={'Authorization': 'Token %s' % ona_token.token})
            #data = json.loads(response.content)
            # now fetch the data from ONA and put it into a silo
            #self.stdout.write("read %s" % read_id, ending='')
            self.stdout.write('Successfully fetched the READ_ID, "%s", from database' % read_id)
            self.stdout.write(str(response.content))