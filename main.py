import webapp2
from google.appengine.ext import ndb
import jinja2
import os


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
