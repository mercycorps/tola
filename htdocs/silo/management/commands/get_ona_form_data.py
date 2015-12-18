import requests, json
from requests.auth import HTTPDigestAuth

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.auth.models import User

from silo.models import LabelValueStore, Read, Silo, ThirdPartyTokens
from tola.util import siloToDict, combineColumns

class Command(BaseCommand):
    """
    Usage: python manage.py get_ona_form_data --username mkhan --read_ids 2 9 --silo_id 1
    """
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
                raise CommandError('Read "%s" does not exist for user, %s' % (read_id, user.username))

            # Fetch the data from ONA
            ona_token = ThirdPartyTokens.objects.get(user=user.pk, name="ONA")
            response = requests.get(read.read_url, headers={'Authorization': 'Token %s' % ona_token.token})
            data = json.loads(response.content)

            # import data into this silo
            num_rows = len(data)
            if num_rows == 0:
                continue

            counter = None
            #loop over data and insert create and edit dates and append to dict
            for counter, row in enumerate(data):
                lvs = LabelValueStore()
                lvs.silo_id = silo.pk
                for new_label, new_value in row.iteritems():
                    if new_label is not "" and new_label is not None and new_label is not "edit_date" and new_label is not "create_date":
                        setattr(lvs, new_label, new_value)
                lvs.create_date = timezone.now()
                result = lvs.save()

            if num_rows == (counter+1):
                combineColumns(silo_id)

            self.stdout.write('Successfully fetched the READ_ID, "%s", from database' % read_id)
