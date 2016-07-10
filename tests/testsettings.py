# -*- coding: utf-8 -*-
from __future__ import unicode_literals

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'djcompoundqueryset',

    'tests.testapp'
]

SITE_ID = 1
ROOT_URLCONF = 'core.urls'

SECRET_KEY = 'foobarred'

USE_L10N = True

