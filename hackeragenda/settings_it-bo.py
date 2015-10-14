# Django settings for hackeragenda project.

from settings import *

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

PREDEFINED_FILTERS = OrderedDict()
PREDEFINED_FILTERS["default"] = {
    "source": [],
    "exclude_source": [],
    "tag": [],
    "exclude_tag": ["meeting"],
}

PREDEFINED_FILTERS["all"] = {
    "source": [],
    "exclude_source": [],
    "tag": [],
    "exclude_tag": [],
}

AGENDA="it-bo"
