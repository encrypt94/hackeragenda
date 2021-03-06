import re
import sys
import time
import urllib
import tweepy

from datetime import date, timedelta
from optparse import make_option
from dateutil.parser import parse

from django.core.management.base import BaseCommand
from django.conf import settings

from events.models import Event


def tweet_size(tweet):
    return len(re.sub("https://\S*", "X"*23, re.sub("http://\S*", "X"*22, tweet)))


def connect_to_twitter():
    if not hasattr(settings, "TWITTER_ACCESS_TOKEN") or not hasattr(settings, "TWITTER_ACCESS_SECRET"):
        print "Error: TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_SECRET must be set in the settings.py"
        sys.exit(1)

    auth = tweepy.OAuthHandler("KwayVtavdRYPKmnSuZO2w", "vvhA31BhosJdcpjmQJk8ORqp7M0whIDBlIAGqwAQ")
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
       make_option('--run',
            action='store_true',
            dest='run',
            default=False,
            help='Actually tweet'),
       make_option('--date',
            action='store',
            dest='date',
            default=None,
            help='custom date, default to today'),
    )

    def handle(self, *args, **options):
        if not options["run"]:
            print "Warning: won't tweet, use --run to actually tweet."
        else:
            self.twitter = connect_to_twitter()

        for tweet, location in self.generate_tweets(parse(options["date"]) if options["date"] is not None else date.today()):
            if not options["run"]:
                print tweet, location
            else:
                self.tweet(tweet, location)

    def tweet(self, t, location):
        print "Tweet:", t
        if location is None:
            self.twitter.update_status(t)
        else:
            map_picture_url = "https://open.mapquestapi.com/staticmap/v4/getmap?key=Kmjtd|luu7n162n1%%2C22%%3Do5-h61wh&size=500,600&zoom=12&center=%(lat)s,%(lon)s&pois=green_1,%(lat)s,%(lon)s,0,0|green_1,%(lat)s,%(lon)s,0,0" % {"lat": location[0], "lon": location[1]}
            urllib.urlretrieve(map_picture_url, "map.jpg")
            self.twitter.update_with_media("map.jpg", t)

        time.sleep(300)

    def generate_tweets(self, tweet_date):
        today_events = Event.objects.filter(agenda=settings.AGENDA).filter(start__gte=tweet_date).filter(start__lt=tweet_date + timedelta(days=1))
        this_week_other_events = Event.objects.filter(agenda=settings.AGENDA).filter(start__gte=tweet_date + timedelta(days=1)).filter(start__lt=tweet_date + timedelta(days=7))

        for tweet, location in self.format_tweets(today_events):
            yield tweet, location

        if tweet_date.weekday() == 0:
            for tweet, location in self.format_tweets(this_week_other_events):
                yield tweet, location

    def format_tweets(self, events):
        def format_title(x):
            return "\"%(title)s\" %(date)s%(time)s" % {
                "date": ("this %s" % x.start.strftime("%A")) if x.start.date() != date else "today",
                "time": (" at %s" % x.start.strftime("%H:%M")) if not x.all_day and (x.start.hour != 0 or x.start.minute != 0) else "",
                "title": x.title
            }

        for event in events:
            tweet = [format_title(event), event.url, "#" + "".join(event.source.replace("_", " ").title().split())]

            has_location = event.lat and event.lon

            size = 141 if not has_location else 118

            if tweet_size(" ".join(tweet)) > size:
                to_remove = tweet_size(" ".join(tweet)) - (size - 1)
                event.title = event.title[to_remove + 3:] + "..."
                tweet[0] = format_title(event)

            tweet = " ".join(tweet)
            yield (tweet.encode("Utf-8"), (event.lat, event.lon) if event.lat and event.lon else None)
