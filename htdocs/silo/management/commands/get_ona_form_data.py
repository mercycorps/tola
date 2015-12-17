from django.core.management.base import BaseCommand, CommandError
from silo.models import *

class Command(BaseCommand):
    help = 'Fetches a specific form data from ONA'

    def add_arguments(self, parser):
        parser.add_argument('read_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for read_id in options['read_id']:
            try:
                read = Read.objects.get(pk=read_id)

            except Read.DoesNotExist:
                raise CommandError('Read "%s" does not exist' % read_id)

            # now fetch the data from ONA and put it into a silo
            #self.stdout.write("read %s" % read_id, ending='')
            self.stdout.write('Successfully fetched the READ_ID from database "%s"' % read_id)