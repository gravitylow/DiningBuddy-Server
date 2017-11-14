DiningBuddy-Server
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
    pip install -r requirements.txt
    deactivate
    mkdir static
    mkdir static/menus
    mkdir static/graphs
    sudo crontab -e
    
Add jobs from data/crontab and save

    mongoimport --db cnu --collection locations --file data/mongo/locations.json
    mongoimport --db cnu --collection graphs --file data/mongo/graphs.json
    cd /etc/apache2/sites-available
        
Copy data/apache2/api.gravitydevelopment.net.conf

Copy data/apache2/ssl

    sudo a2enmod ssl
    sudo a2enmod info
    sudo a2ensite api.gravitydevelopment.net
    sudo service apache2 restart
