import webapp2
import jinja2
import os
import random
from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

drivers_list = []

class User(ndb.Model):
    name = ndb.StringProperty()
    music = ndb.StringProperty()
    food = ndb.StringProperty()
    personality = ndb.StringProperty()
    # When we want to access user trips, query the trip with the user_key and list trips
    def url(self):
        url = '/userinfo?key=' + self.key.urlsafe()
        return url


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
        userinfo = User.query().fetch()
        logout_url = users.create_logout_url('/')
        vals = {'logout_url': logout_url, 'userinfo':userinfo}
        template = jinja_environment.get_template('userinfo.html')
        self.response.write(template.render(vals))



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
        user = users.get_current_user()
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        drivers = self.request.get('driver')
        destination = self.request.get('destination')
        action = self.request.get('action')
        #query the trips and set it to variable trips
        if action == 'create':
            newtrip = Trip(tripname=tripname, trippassword=trippw, destination=destination, user_key=user)
            newtrip.put()
        else:
            foundtrip = None
            for trip in Trip.query().fetch():
                if trip.tripname == tripname and trip.trippassword == trippw:
                    foundtrip = trip
            if foundtrip:
                # do stuff
            else:
            #display this trip does not exist
        # vvvv don't want to make a new trip every time we join a trip b/c currently create a trip and join a trip are linking to the same page.

        if drivers == 'yes':
            drivers_list.append(user.name)
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
