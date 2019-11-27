# Standard Library
import os

# Third party
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "randomdjangoprojectname.settings")

application = get_wsgi_application()
