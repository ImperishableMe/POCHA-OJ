"""
WSGI config for online_judge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')

subprocess.Popen("python manage.py process_tasks",shell=True)

application = get_wsgi_application()
