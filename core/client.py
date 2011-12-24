import httplib2
import simplejson as json
import re

default_client = None

def get_client():
    return default_client

def setup_client(*args, **kwargs):
    global default_client
    default_client = Client(*args, **kwargs)

class Client(object):
    def __init__(self, host, ssl=True, user=None, password=None,
            apiversion='v1'):
        """
        Construct a new CORE client
        """
        # create our HTTP object
        self.http = httplib2.Http()

        # set our credentials
        self.http.add_credentials(user, password)

        if ssl:
            protocol = 'https'
        else:
            protocol = 'http'

        self.host = '%s://%s' % (protocol, host)
        self.base_url = "api/%s" % (apiversion,)

    _request_cache = {}
    def make_request(self, url, cache=True, has_base=False):
        def req():
            # make the request
            if has_base:
                url_parts = (self.host, url)
            else:
                url_parts = (self.host, self.base_url, url)
            full_url = '/'.join(url_parts)
            response, content = self.http.request(full_url)

            # load the data 
            return json.loads(content)
        
        # check our cache first
        if cache:
            if url not in self._request_cache:
                # cache it
                self._request_cache[url] = req()
            return self._request_cache[url]
        return req()
