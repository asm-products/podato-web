from webapp.db import db
from webapp.podcasts.models import Podcast
from webapp.podcasts import crawler

class SubscriptionHolder(object):
    subscriptions = db.ListField(db.ReferenceField(Podcast, reverse_delete_rule=db.PULL))

    def subscribe(self, podcast):
        if podcast in self.subscriptions:
            return False
        self.modify(push__subscriptions=podcast)
        return True

    def subscribe_by_url(self, url):
        podcast = Podcast.get_by_url(url)
        if podcast == None:
            crawler.fetch(url)
            return self.subscribe_by_url(url)
        return self.subscribe(podcast)

    def unsubscribe(self, podcast):
        return self.modify(pull_subscriptions=podcast)

    def unsubscribe_by_url(self, url):
        podcast = Podcast.get_by_url
        return self.unsubscribe(podcast)
