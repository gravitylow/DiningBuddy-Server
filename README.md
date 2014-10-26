CNU-Server
==========

Installation (Ubuntu)
-------
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install git apache2 libapache2-mod-wsgi python python-pip python-dev mongodb
    sudo pip install virtualenv
    sudo mkdir /var/www/api.gravitydevelopment.net
    sudo mkdir /var/log/apache2/api.gravitydevelopment.net
    sudo chown ubuntu /var/www/api.gravitydevelopment.net/
    cd /var/www/api.gravitydevelopment.net
    ssh-keygen -t rsa -C "CNU Deploy Key"
    eval "$(ssh-agent -s)
    ssh-add ~/.ssh/id_rsa
    cat ~/.ssh/id_rsa.pub
    
Add ssh key to github

    git clone git@github.com:gravitylow/CNU-Server.git cnu
    cd cnu
    virtualenv flask
    source flask/bin/activate
    sudo pip install flask pymongo simplejson python-dateutil pytz google-api-python-client pygal
    deactivate
    mkdir static
    mkdir static/menus
    mkdir static/graphs
    cd /etc/apache2/sites-available
    
Copy over data/apache2/api.gravitydevelopment.net.conf
Copy over data/apache2/ssl

    sudo a2enmod ssl
    sudo a2ensite api.gravitydevelopment.net
    sudo service apache2 restart
    sudo crontab -e
    
Copy over data/crontab
Copy over data/locations.json and data/graphs.json

    mongoimport --db cnu --collection locations --file locations.json
    mongoimport --db cnu --collection graphs --file graphs.json
    sudo vi /etc/apache2/ports.conf
    
Remove Listen 80
