from google.appengine.ext import ndb

class Ueer(ndb.Model):
    username = ndb.StringProperty(required=True)
    primary_email = ndb.StringProperty(required=True)
    email_addresses = ndb.StringProperty(repeated=True)
    avatar_url = ndb.StringProperty(required=True)
    