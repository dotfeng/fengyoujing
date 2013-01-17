import sae
from feng import wsgi

application = sae.create_wsgi_app(wsgi.application)