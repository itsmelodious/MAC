import webapp2
import jinja2
import os
import random
from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class User(ndb.Model):
    name = ndb.StringProperty()
    music = ndb.StringProperty()
    food = ndb.StringProperty()
    personality = ndb.StringProperty()
    driver = ndb.BooleanProperty()
    # When we want to access user trips, query the trip with the user_key and list trips

class Trip(ndb.Model):
    tripname = ndb.StringProperty()
    trippassword = ndb.StringProperty()
    user_key = ndb.KeyProperty(kind=User)
    destination = ndb.StringProperty()

    def url(self):
        url = '/tripinfo?key=' + self.key.urlsafe()
        return url

class Car(ndb.Model):
    trip_key = ndb.KeyProperty(kind=Trip)
    seats = ndb.IntegerProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/mainpage')

        # This creates the login link
        login_url = users.create_login_url('/')

        template = jinja_environment.get_template('login.html')
        vals = {'login_url': login_url}
        self.response.write(template.render(vals))

class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newacc.html')
        self.response.write(template.render())

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(nickname, logout_url)
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
        template = jinja_environment.get_template('userinfo.html')
        self.response.write(template.render())


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('mainpage.html')
        self.response.write(template.render())
    def post(self):
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
    def post(self):
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        self.redirect('/jointrip')

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
