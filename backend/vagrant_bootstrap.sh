# Add the public GPG key
wget -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Create a file with the repository address
echo deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main | sudo tee /etc/apt/sources.list.d/postgresql.list

# Remove any older postgresql installation you may have (ex:)
apt-get remove postgresql postgresql-contrib postgresql-client 

# Install the PostgreSQL
apt-get update
apt-get install postgresql-9.5 postgresql-server-dev-9.5 postgresql-contrib-9.5 -y --force-yes

# Create the user to access the db. (vagrant sample)
postgres psql -c "CREATE USER vagrant WITH SUPERUSER CREATEDB ENCRYPTED PASSWORD 'vagrant'"

# Change the port
sed -i "s/port = 5433/port = 5432/" /etc/postgresql/9.5/main/postgresql.conf

# Restar de DB
/etc/init.d/postgresql restart


## If you get a locale error follow those instructions

# error message: PG::InvalidParameterValue: ERROR: encoding "UTF8" does not match locale "en_US"

# generate the locales
 locale-gen en_US.UTF-8
 update-locale LANG=en_US.UTF-8

# drop and recreate the default cluster
 pg_dropcluster --stop 9.5 main
 pg_createcluster --start -e UTF-8 9.5 main

# recreate our database user
sudo -u postgres psql -c "CREATE USER vagrant WITH SUPERUSER CREATEDB ENCRYPTED PASSWORD 'vagrant'"
echo "Creating Database .... "
sudo -u postgres psql -c "CREATE DATABASE flask_jwt_auth"

echo "Creating Test Database .... "
sudo -u postgres psql -c "CREATE DATABASE flask_jwt_auth_test"
# sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE myproject vagrant"

echo "Adding Host Name"
echo "0.0.0.0  account.track.com" >> /etc/hosts

# Install git for version control, pip for install python packages
echo 'Installing git, Python 2, and pip...'
# libfreetype6-dev ziblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
sudo apt-get -qq install git python python-pip python-dev libjpeg-dev libpq-dev libtiff5-dev zlib1g-dev > /dev/null 2>&1
curl -s https://bootstrap.pypa.io/get-pip.py | python2.7 > /dev/null 2>&1


# Install virtualenv / virtualenvwrapper
echo 'Installing and configuring virtualenv and virtualenvwrapper...'
pip install --quiet virtualenvwrapper==4.7.0 Pygments==2.1.1
mkdir ~vagrant/virtualenvs
chown vagrant:vagrant ~vagrant/virtualenvs
printf "\n\n# Virtualenv settings\n" >> ~vagrant/.bashrc
printf "export PYTHONPATH=/usr/lib/python2.7" >> ~vagrant/.bashrc
printf "export WORKON_HOME=~vagrant/virtualenvs\n" >> ~vagrant/.bashrc
printf "export PROJECT_HOME=/vagrant\n" >> ~vagrant/.bashrc
printf "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7\n" >> ~vagrant/.bashrc
printf "source /usr/local/bin/virtualenvwrapper.sh\n" >> ~vagrant/.bashrc

# Some useful aliases for getting started, MotD
echo 'Setting up message of the day, and some aliases...'
cp /vagrant/examples/motd.txt /etc/motd
printf "\nUseful Aliases:\n" >> ~vagrant/.bashrc
printf "alias menu='cat /etc/motd'\n" >> ~vagrant/.bashrc
printf "alias runserver='python manage.py runserver 0.0.0.0:8000'\n" >> ~vagrant/.bashrc
printf "alias ccat='pygmentize -O style=monokai -f terminal -g'\n" >> ~vagrant/.bashrc

# Complete
echo ""
echo "Vagrant install complete."
echo "Now try logging in:"
echo "    $ vagrant ssh"
