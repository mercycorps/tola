#!/bin/bash
# init
function pause(){
   read -p "$*"
}

echo "Should we do a pull from git Dev branch first? (y/n)"
read a
if [[ $a == "y" || $a == "Y" ]]; then
	cd ../
	sudo git checkout dev
	sudo git pull
	cd deploy_scripts
else
	echo "Skipping...";
fi

if P1=$(pgrep 'puppet')
then
  echo "Stopping puppet running at PID = $P1"
  sudo /sbin/service puppet stop
else
  echo "puppet service was already stopped."
fi

if P2=$(pgrep 'postfix')
then
  echo "Stopping postfix service running at PID = $P2 "
  sudo /sbin/service postfix stop
else
  echo "postfix was already stopped."
fi

cd ../htdocs

echo "Running Migrations..."
sudo py manage.py migrate

echo "Do you want to run fixtures as sudo and using py? (Y/n)"
read c

if [[ $c == "y" || $c == "Y" ]]; then
    sudo py manage.py loaddata fixtures/groups.json
    sudo py manage.py loaddata fixtures/country.json
    sudo py manage.py loaddata fixtures/province.json
    sudo py manage.py loaddata fixtures/district.json
    sudo py manage.py loaddata fixtures/program.json
    sudo py manage.py loaddata fixtures/read_type.json
    sudo py manage.py loaddata fixtures/silo.json
    sudo py manage.py loaddata fixtures/sector.json
else
  echo "Ok Skipping"
fi

echo "Do you want to run fixtures as you and using python? (Y/n)"
read c

if [[ $c == "y" || $c == "Y" ]]; then
    python manage.py loaddata fixtures/groups.json
    python manage.py loaddata fixtures/country.json
    python manage.py loaddata fixtures/province.json
    python manage.py loaddata fixtures/district.json
    python manage.py loaddata fixtures/program.json
    python manage.py loaddata fixtures/read_type.json
    python manage.py loaddata fixtures/silo.json
    python manage.py loaddata fixtures/sector.json
else
  echo "Ok Skipping"
fi

cd ../deploy_scripts

echo "Would you like to empty the mail Queue (y/n)?"
read e
if [[ $e == "y" || $e == "Y" ]]; then
	sudo postsuper -d ALL
fi

echo "Done"
