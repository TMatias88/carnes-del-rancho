import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carnes_del_rancho.settings')
application = get_wsgi_application()
