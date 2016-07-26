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
    email = ndb.StringProperty()
    # When we want to access user trips, query the trip with the user_key and list trips

    def url(self):
        url = '/userinfo?key=' + self.key.urlsafe()
        return url

class Trip(ndb.Model):
    tripname = ndb.StringProperty()
    trippassword = ndb.StringProperty()
    user_key = ndb.KeyProperty(kind=User, repeated=True)
    destination = ndb.StringProperty()
    drivers = ndb.StringProperty(repeated=True)

    def url(self):
        url = '/tripinfo?key=' + self.key.urlsafe()
        return url

class Car(ndb.Model):
    trip_key = ndb.KeyProperty(kind=Trip)
    seats = ndb.IntegerProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in, then redirect to the main page.
        if user:
            if not User.query(User.email==user.email()).fetch():
                newuser = User(email=user.email())
                newuser.put()
            self.redirect('/mainpage')
        # This creates the sign in link.
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
        # userinfo = User.query().fetch() #should change to .get(userkey) so it only displays the info for the specific user
        # This creates the sign out link.
        logout_url = users.create_logout_url('/')
        vals = {'logout_url': logout_url, 'user': user}
        template = jinja_environment.get_template('userinfo.html')
        self.response.write(template.render(vals))

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        trips = Trip.query().fetch()
        vals = {'trips': trips, 'user':user}
        template = jinja_environment.get_template('mainpage.html')
        self.response.write(template.render(vals))

    def post(self):
        user = users.get_current_user()
        query = User.query(User.email==user.email()).get()
        userkey = query.key
        username = self.request.get('username')
        pw = self.request.get('pw')
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        drivers = self.request.get('driver')
        destination = self.request.get('destination')
        action = self.request.get('action')
        seats = self.request.get('seats')
        # trip_key_urlsafe = self.request.get('key')
        # trip_key = ndb.Key(urlsafe=trip_key_urlsafe)
        # trip = trip_key.get()
        if action == 'create':
            if drivers == "yes":
                # Create a new trip
                newtrip = Trip(tripname=tripname, trippassword=trippw, destination=destination, user_key= [userkey])
                newtrip.put()
            else:
                # Create a new trip
                newtrip = Trip(tripname=tripname, trippassword=trippw, destination=destination, user_key= [userkey])
                newtrip.put()
 #        else:
 #            # Loop through the list of trips.
 # #            for trip in Trip.query().fetch():
 # #                if trip.tripname == tripname and trip.trippassword == trippw:
 # #                    foundtrip = trip
 # #                    if drivers == "yes":
 # #                        newdriver = Car(trip_key=trip, seats=seats)
 # #                else:
 # #                    self.response.write('Error')
 # #
 # #
 # # #        if foundtrip:
 # # # do stuff
 # # #
 # # #
 # # #    If the user is a driver, add the user to the list of drivers.
 # # #    if drivers == 'yes':
 # # #        drivers_list.append(user.name)
        self.redirect('/mainpage')

class CreateTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newtrip.html')
        self.response.write(template.render())

class TripInfoHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)
        trip = key.get()
        vals = {'trip': trip}
        template = jinja_environment.get_template('tripinfo.html')
        self.response.write(template.render(vals))

        # user = users.get_current_user()


class JoinTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('jointrip.html')
        self.response.write(template.render())

    def post(self):
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        self.redirect('/jointrip') # why is it redirecting to jointrip? Shouldn't it go to tripinfo or mainpage?

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
