# flake8: noqa
from fabric.api import *

env.roledefs = {
    'app': [],
}


@roles('app')
def deploy():
    # Remove this line when you're happy that this Fabfile is correct
    raise RuntimeError("Please check the fabfile before using it")

    base_dir = '/usr/local/django/madewithwagtail'
    virtualenv_dir = '/usr/local/django/virtualenvs/madewithwagtail'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    supervisor_task = 'madewithwagtail'

    with cd(base_dir):
        run('git pull origin master')
        run(pip + ' install -r requirements.txt')
        run(python + ' madewithwagtail/manage.py migrate --settings=madewithwagtail.settings.production --noinput')
        run(python + ' madewithwagtail/manage.py collectstatic --settings=madewithwagtail.settings.production --noinput')
        run(python + ' madewithwagtail/manage.py compress --settings=madewithwagtail.settings.production')
        run(python + ' madewithwagtail/manage.py update_index --settings=madewithwagtail.settings.production')

    sudo('supervisorctl restart ' + supervisor_task)
