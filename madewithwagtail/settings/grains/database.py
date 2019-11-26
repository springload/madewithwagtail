import dj_database_url

from madewithwagtail.settings import *

DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
