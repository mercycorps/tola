"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""
from django.db import connection, transaction

cursor = connection.cursor()
from os.path import exists
import csv
import unicodedata
import sys
import urllib2
from datetime import date
from activitydb.models import Country, Province, District

def run():
    print "Uploading Country Admin data"

country_id = 4

def getAllData():

    with open('fixtures/dist_prov.csv', 'rb') as csvfile:
        country = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in country:
            column_num = 0
            new_district = ""
            for column in row:
                if column_num == 1:
                    print "new_district="
                    new_district = column.replace('\n', ' ')
                    print new_district
                else:
                    print "query for province="
                    print column
                    getProvince = Province.objects.get(name=column, country=country_id)
                    if getProvince:
                        new_dist = District(name=new_district, province=getProvince)
                        new_dist.save()
                    else:
                        new_prov = Province(name=column, country=country_id)
                        new_prov.save()
                        new_dist = District(name=new_district, province=getProvince)
                        new_dist.save()

                column_num = 1

getAllData()