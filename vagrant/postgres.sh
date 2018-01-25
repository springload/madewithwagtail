#!/bin/bash


# Let us connect to the database from the localhost without credentials
su - vagrant -c "echo -n 'Changing postgres authorisation method ... ' && \
                 sudo sed -i 's/local\s\{1,\}all\s\{1,\}postgres\s\{1,\}peer/local all postgres trust/g' \
                             /etc/postgresql/9.3/main/pg_hba.conf && \
                 echo done! && \
                 sudo service postgresql restart"

# Let us connect to the database from everywhere without credentials
su - vagrant -c "echo -n 'Opening postgres to public ' && \
                 sudo grep -q -F 'host	all	all	0.0.0.0/0	trust' /etc/postgresql/9.3/main/pg_hba.conf || \
                            echo 'host	all	all	0.0.0.0/0	trust' | sudo tee -a /etc/postgresql/9.3/main/pg_hba.conf && \
                 sudo sed -i \"s/.*#.*listen_addresses = 'localhost'/listen_addresses = '*'/g\" \
                             /etc/postgresql/9.3/main/postgresql.conf && \
                 echo done! && \
                 sudo service postgresql restart"
