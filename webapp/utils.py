import os
import re
import unicodedata
import urlparse


def _get_control_chars_regex():
    all_chars = (unichr(i) for i in xrange(0x10000))
    control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
    return  re.compile('[%s]' % re.escape(control_chars))


def strip_control_chars(s):
    """Strips control characters from s."""
    return _get_control_chars_regex().sub('', s)


def validate_url(url, allow_hash=True):
    parsed = urlparse.urlparse(url)
    if not parsed.scheme in ['http', 'https']:
        raise ValueError('The following url is invalid: %s, it has an'
                         'unsupported scheme, only http and https are valid.' % url)
    if not parsed.netloc:
        raise ValueError('The following url is invalid: %s, it doesn\'t seem to have a domain.' % uri)
    if not allow_hash and parsed.fragment:
        raise ValueError('Urls shouldn\'t have a hash fragment.')


def generate_random_string():
    return os.urandom(16).encode('hex')


class ValidatedModel(object):
    """Make sure that the instance is validated before it is put into the datastore."""

    def _pre_put_hook(self):
        self.validate()

    def validate(self):
        """Subclasses should override this."""
        raise NotImplemented("Subclasses of ValidatedModel should override the validate method.")


class AttributeHider(object):
    def __init__(self, obj, hide):
        self.hide = hide
        self.obj = obj
    def __getattr__(self, name):
        if not name in self.hide:
            return getattr(self.obj, name)