import sae
from shopflow import wsgi

application = sae.create_wsgi_app(wsgi.application)