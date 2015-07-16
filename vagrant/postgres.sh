#!/bin/bash


# Let us connect to the database from the localhost without credentials
su - vagrant -c "echo -n 'Changing postgres authorisation method ... ' && \
                 sudo sed -i 's/local\s\{1,\}all\s\{1,\}postgres\s\{1,\}peer/local all postgres trust/g' \
                             /etc/postgresql/9.3/main/pg_hba.conf && \
                 echo done! && \
                 sudo service postgresql restart"
