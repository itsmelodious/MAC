import webapp2
import jinja2
import os
import random
from random import shuffle
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
    username = ndb.StringProperty()
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
    passengers = ndb.StringProperty(repeated=True)

    def url(self):
        url = '/tripinfo?key=' + self.key.urlsafe()
        return url


class Car(ndb.Model):
    trip_key = ndb.KeyProperty(kind=Trip)
    seats = ndb.IntegerProperty()
    driver_key = ndb.KeyProperty(kind=User)
    passengers = ndb.StringProperty(repeated=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in, then redirect to the main page.
        if user:
            if not User.query(User.email==user.email()).fetch():
                self.redirect('/home')
            else:
                self.redirect('/mainpage')
        # This creates the sign in link.
        login_url = users.create_login_url('/')
        template = jinja_environment.get_template('home.html')
        vals = {'login_url': login_url}
        self.response.write(template.render(vals))

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newacc.html')
        self.response.write(template.render())

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        userinfo = User.query(User.email==user.email()).get()
        # This creates the sign out link.
        logout_url = users.create_logout_url('/')
        vals = {'logout_url': logout_url, 'userinfo':userinfo}
        template = jinja_environment.get_template('userinfo.html')
        self.response.write(template.render(vals))

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        trips=[]
        user = users.get_current_user()
        query = User.query(User.email==user.email()).get()
        userkey = query.key
        for trip in Trip.query().fetch():
            if userkey in trip.user_key:
                trips.append(trip)
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

        if action == 'create':
            seats = int(self.request.get('seats'))
            newtrip = Trip(tripname=tripname, trippassword=trippw, destination=destination, user_key= [userkey], drivers = [query.name])
            newtrip.put()
            newcar = Car(trip_key=newtrip.key, seats=seats, driver_key= userkey)
            newcar.put()

        else:
            # Loop through the list of trips.
            foundtrip = None
            for trip in Trip.query().fetch():
                if trip.tripname == tripname and trip.trippassword == trippw:
                    foundtrip = True
            if foundtrip:
                if drivers == "yes":
                    seats = int(self.request.get('seats'))
                    trip = Trip.query(Trip.tripname==tripname).get()
                    trip.drivers.append(query.name)
                    trip.user_key.append(userkey)
                    newcar = Car(trip_key=trip.key, seats=seats, driver_key=userkey)
                    newcar.put()
                    trip.put()
                else:
                    trip = Trip.query(Trip.tripname==tripname).get()
                    tripkey = trip.key
                    cars = Car.query(Car.trip_key==tripkey).fetch()
                    trip.passengers.append(query.name)
                    car = random.choice(cars)
                    if len(car.passengers)<(car.seats-1):
                        car.passengers.append(query.name)
                    trip.user_key.append(userkey)
                    trip.put()
                    car.put()
            else:
                self.response.write('Error')
                return

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
        cars = Car.query(Car.trip_key==key).fetch()
        vals = {'trip': trip, 'cars': cars}
        template = jinja_environment.get_template('tripinfo.html')
        self.response.write(template.render(vals))
    def post(self):
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)
        trip = key.get()
        tripname = self.request.get('tripname')
        trippw = self.request.get('trippw')
        trip.tripname = tripname
        trip.trippassword = trippw
        trip.put()
        self.redirect(trip.url())

class JoinTripHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('jointrip.html')
        self.response.write(template.render())

class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('newacc.html')
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        name = self.request.get('name')
        username = self.request.get('username')
        personality = self.request.get('personality')
        music = self.request.get('music')
        food = self.request.get('food')
        newuser = User(email=user.email(), name=name, username=username, genInfo=genInfo, personality=personality, music=music, food=food)
        newuser.put()
        self.redirect('/mainpage')

class EditTripHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)
        trip = key.get()
        vals = {'trip':trip}
        template = jinja_environment.get_template('editrip.html')
        self.response.write(template.render(vals))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/newaccount', CreateAccountHandler),
    ('/userinfo', UserInfoHandler),
    ('/mainpage', MainPageHandler),
    ('/newtrip', CreateTripHandler),
    ('/tripinfo', TripInfoHandler),
    ('/jointrip', JoinTripHandler),
    ('/edittrip', EditTripHandler)
], debug=True)
