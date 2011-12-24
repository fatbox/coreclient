from client import get_client

def is_api_collection(data):
    return isinstance(data, dict) and \
           'objects' in data

def is_api_object(data):
    return isinstance(data, dict) and \
            'resource_uri' in data

class ObjectException(Exception):
    pass

class Object(object):
    """
    Represents a single object returned from tastypie
    """
    url = None

    def __init__(self, data=None, url=None):
        if url:
            client = get_client()
            data = client.make_request(url, has_base=True)

        if not is_api_object(data):
            raise ObjectException("Not a valid object")

        self.data = data

    def __getitem__(self, name):
        return self.data[name]

    @classmethod
    def make_url(cls, filter=None):
        if filter:
            return '?'.join((cls.url, filter))
        return cls.url

class Objects(object):
    """
    A collection of objects

    This takes an API url that returns a collection and yields an iterator
    that follows the next links lazily
    """
    type = None

    def __init__(self, filter=None):
        if not isinstance(self.type, type(Object)):
            raise ObjectException("You need to specify a type for your object: %s" % self.__class__.__name__)

        self.url = self.type.make_url(filter)

    def __iter__(self):
        client = get_client()

        # make our first request
        data = client.make_request(self.url)

        while is_api_collection(data):
            # iterate through the data objects
            for obj in data['objects']:
                # act as a generator
                if isinstance(self.type, type(Object)):
                    # if self.type is an Object then return it
                    # instantiated with the data from the api call
                    yield self.type(data=obj)
                else:
                    # otherwise just return the data itself
                    yield obj

            if 'meta' in data and 'next' in data['meta'] and \
                    data['meta']['next'] is not None:
                # fetch the next set of objects
                data = client.make_request(data['meta']['next'], has_base=True)
            else:
                # we've reached the end of the object listing
                # signal to the while loop
                data = None


class DataArray(object):
    def get_data(self, name, default=None):
        """
        Return a data element associated with a device
        """
        for data in self['data']:
            if data['name'] == name:
                return data
        return default

    def match_data(self, regexp):
        """
        Return a list of any data elements that match the supplied regexp
        """
        output = []
        for data in self['data']:
            if re.search(regexp, data['name']):
                output.append(data)
        return output

class Device(Object, DataArray):
    url = 'device/'

    def get_automation_variable(self, name, default=None):
        vars = self['automation_variables'].split("\n")
        for var in vars:
            if var.strip() == "":
                continue
            n, v = var.split("=")
            if n == name:
                return v.strip()
        return default

    def get_service(self, key):
        """
        Return a service associated with a device
        """
        for service in self['services']:
            if service['service_key'] == key:
                return service

class Devices(Objects):
    type = Device



class Service(Object, DataArray):
    url = 'deviceservice'

class Services(Objects):
    type = Service
