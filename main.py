import webapp2
import jinja2
import os
import random
from google.appengine.api import user
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newacc.html')
        self.response.write(template.render())

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('userinfo.html')
        self.response.write(template.render())

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('mainpage.html')
        self.response.write(template.render())
    def post(self):
        user = user.get_current_user()
        email = user.email()
        username = self.request.get('username')
        pw = self.request.get('pw')
        self.redirect('/mainpage')

class CreateTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newtrip.html')
        self.response.write(template.render())

class TripInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('tripinfo.html')
        self.response.write(template.render())
    def post(self):
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        self.redirect('/tripinfo')

class JoinTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('jointrip.html')
        self.response.write(template.render())

class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newacc.html')
        self.response.write(template.render())

class EditTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('editrip.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newaccount', CreateAccountHandler),
    ('/userinfo', UserInfoHandler),
    ('/mainpage', MainPageHandler),
    ('/newtrip', CreateTripHandler),
    ('/tripinfo', TripInfoHandler),
    ('/jointrip', JoinTripHandler),
    ('/edittrip', EditTripHandler)
], debug=True)
