import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gym_project.settings')
from django import setup
setup()
from django.test import Client
c = Client()
paths = ['/plans/add/','/register-member/','/login/','/dashboard/']
for path in paths:
    try:
        r = c.get(path)
        print('\nPATH:', path, 'STATUS:', r.status_code)
        ct = r.content.decode('utf-8')
        has = 'csrfmiddlewaretoken' in ct
        print('Has csrf token in HTML:', has)
        print('Cookies set by client after GET:', list(c.cookies.keys()))
    except Exception as e:
        print('Error fetching', path, e)
