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
    help = 'Fetches all reads that have autopull checked and belong to a silo

    def handle(self, *args, **options):
        silos = Silo.objects.filter(reads__autopull=True)
        for silo in silos:
            reads = silo.reads
            for read in reads.all():
                pass
                # pull from ona and save it in the silo