Asana Data
====
FREDS
Feed, Read, Edit, Display and Silo data from various mobile data collection platforms.

The Read app is intended for use with FormHub data collection platform.  You should be able
to add an additional app using Read as a template to import data or create new "reads"
from other data sources.  You only need to import the new app, add the new read templates
and update the base template to include your new app as sub-navigation to the main read.

## USING virtualenv
mkdir frds_project
cd frds_project
(Install virtualenv)
pip install virtualenv

cd frds_project

# Create Virtualenv
virtualenv —no-site-packages frds-venv
*use no site packages to prevent virtualenv from seeing your global packages

. frds-venv/bin/activate
*allows us to just use pip from command line by adding to the path rather than full path

##Activate Virtualenv
source frds-venv/bin/activate

## Fix probable mysql path issue (for mac)
export PATH=$PATH:/usr/local/mysql/bin
* or whatever path you have to your installed mysql_config file in the bin folder of mysql

pip install -r requirements.txt

# Run App
If your using more then one settings file change manage.py to point to local or dev file first
python manage.py runserver 0.0.0.0:8000
*0’s let it run on any local address i.e. localhost,127.0.0.1 etc.
