import logging

from webapp.db import db
from webapp.podcasts.models import Podcast
from webapp.podcasts import crawler
from webapp.async import AsyncSuccess

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
            return AsyncSuccess(async_result=crawler.fetch(url, subscribe=self))
        return AsyncSuccess(success=self.subscribe(podcast))

    def unsubscribe(self, podcast):
        self.modify(pull__subscriptions=podcast)
        podcast.modify(dec__subscribers=1)
        return True

    def unsubscribe_by_url(self, url):
        podcast = Podcast.get_by_url(url)
        if not podcast:
            return False
        return AsyncSuccess(success=self.unsubscribe(podcast))

    def subscribe_multi(self, podcasts):
        not_already_subscribed = []
        for podcast in odcasts:
            if podcast not in self.subscriptions:
                not_already_subscribed.append(podcast)
            self.modify(push_all__subscriptions=not_already_subscribed)
        Podcast.objects(url__in=[p.url for p in not_already_subscribed]).update(inc__subscribers)

    def subscribe_multi_by_url(self, urls):
        podcasts = Podcast.get_multi_by_url(urls)
        already_fetched = []
        to_fetch = []
        for url in urls:
            if url in podcasts:
                already_fetched.append(podcasts[url])
            else:
                to_fetch.append(url)

        if already_fetched:
            self.subscribe_multi(already_fetched)

        res = None
        success = None
        if to_fetch:
            res = crawler.fetch(to_fetch, subscribe=self)
        else:
            success = True

        return AsyncSuccess(async_result=res, success=success)