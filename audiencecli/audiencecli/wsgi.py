import os
import sys

from django.core.wsgi import get_wsgi_application

# Add the project root and src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiencecli.settings')

application = get_wsgi_application()
