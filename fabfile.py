from fabric.api import *


env.roledefs = {
    'app': [],
}


@roles('app')
def deploy():
    # Remove this line when you're happy that this Fabfile is correct
    raise RuntimeError("Please check the fabfile before using it")

    base_dir = '/usr/local/django/wagtailsites'
    virtualenv_dir = '/usr/local/django/virtualenvs/wagtailsites'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    supervisor_task = 'wagtailsites'

    with cd(base_dir):
        run('git pull origin master')
        run(pip + ' install -r requirements.txt')
        run(python + ' wagtailsites/manage.py migrate --settings=wagtailsites.settings.production --noinput')
        run(python + ' wagtailsites/manage.py collectstatic --settings=wagtailsites.settings.production --noinput')
        run(python + ' wagtailsites/manage.py compress --settings=wagtailsites.settings.production')
        run(python + ' wagtailsites/manage.py update_index --settings=wagtailsites.settings.production')

    sudo('supervisorctl restart ' + supervisor_task)
