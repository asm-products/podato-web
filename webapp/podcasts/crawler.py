import urllib

from webapp import utils

# Version of the crawler to use. None means the default version.
CRAWLER_MODULE_VERSION = None


class FetchError(Exception):
    pass

def fetch(url):
    #TODO: implement this without AppEngine
    raise NotImplemented

    utils.validate_url(url, allow_hash=False)
    hostname = modules.get_hostname("crawler", CRAWLER_MODULE_VERSION)
    request_url = "http://" + hostname + "/crawler/fetch?"+urllib.urlencode({"url": url})
    resp = urlfetch.fetch(request_url, "GET")
    if resp.status_code != 200:
        raise FetchError("Fetch error (%s): %s" % (resp.status_code, resp.content))
