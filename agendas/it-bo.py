# encoding: utf-8

import re
import time
import calendar
import requests
import feedparser

from bs4 import BeautifulSoup
from django.template.defaultfilters import slugify
from django.conf import settings
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from icalendar import Calendar
from HTMLParser import HTMLParser

from events.management.commands.fetch_events import event_source
from events.generics import generic_meetup, generic_eventbrite, generic_google_agenda, json_api

@event_source(background_color="#3EA86F", text_color="#000000", url="https://ofpcina.net", predefined_tags=[])
def ofpcina():
    """
    <p>L’ ofPCina : Un laboratorio gratuito, attrezzato per la sistemazione di PC mal o non funzionanti, aperto al pubblico, con a disposizione tecnici volontari che assistono i proprietari nella riparazione del proprio personal computer.</p>
    """
    for event in feedparser.parse("http://ofpcina.net/events/feed/").entries:
        yield {
            "title": "OfPCina",
            "url": event['link'],
            "start": time.strftime("%Y-%m-%d %H:%M", event['published_parsed']),
            "tags": ["fix","diy"]
        }


