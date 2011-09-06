import base64
import collections
import hashlib
from   xmlrpclib import Fault, ServerProxy

API_ENDPOINT = 'https://secure.gravatar.com/xmlrpc'

def hash_email(email):
    return hashlib.md5(email.strip().lower()).hexdigest()

def _check_email_success(response):
    for email, success in response.iteritems():
        if not success:
            raise InvalidEmailError(email)

class Rating:
    G = 0
    PG = 1
    R = 2
    X = 3

class GravatarError(Exception):
    pass

class SecureError(GravatarError):
    pass

class InternalError(GravatarError):
    pass

class AuthenticationError(GravatarError):
    pass

class ParameterMissingError(GravatarError):
    pass

class ParameterIncorrectError(GravatarError):
    pass

class MiscError(GravatarError):
    pass

class UnknownError(GravatarError):
    pass

class InvalidEmailError(GravatarError):
    pass

class InvalidUrlError(GravatarError):
    pass

class InvalidDataError(GravatarError):
    pass

Userimage = collections.namedtuple('Userimage', ['id', 'url', 'rating'])

class User(object):
    def __init__(self, email, password=None, apikey=None):
        """
        Construct an object representing a user account. At least one of `password` and `apikey`
        must be specified.
        :param email: an email address belonging to the account
        :param password: password for the account
        :param apikey: API key for your application
        """
        self._server = ServerProxy(API_ENDPOINT+'?user='+hash_email(email))
        if password is None and apikey is None:
            raise ValueError("Must specify either 'password' or 'apikey' parameter")
        self.password = password
        self.apikey = apikey

    def exists(self, *addresses):
        """
        Return a dictionary where each key is an email address from the passed-in list and each
        value is a boolean of whether that email address belongs to a Gravatar account and has an
        image assigned to it.
        :param varargs: list of email addresses to check
        """
        hashes = dict([(hash_email(email), email) for email in addresses])
        return dict([(hashes[hash], found==1)
                   for hash, found in self._call('exists', hashes=hashes.keys()).iteritems()])

    def addresses(self):
        """
        :returns: a dictionary where each key is an email address belonging to the user account and
        each value is the `Userimage`:class assigned to it, or `None` if no image is assigned
        """
        return dict([(email, Userimage(id=userimage['userimage'], url=userimage['userimage_url'],
                                       rating=userimage['rating'])
                             if len(userimage['userimage']) > 0 else None)
                   for email, userimage in self._call('addresses').iteritems()])

    def userimages(self):
        """
        :returns: a list of class:`Userimage`s belonging to the user account
        """
        return [Userimage(id=id, url=url, rating=int(rating))
                   for id, (rating, url) in self._call('userimages').iteritems()]

    def saveData(self, data, rating):
        """
        Save the data as a new image in the user account.
        :param data: binary image data to save
        :param rating: integer rating for the new image (see `Rating`:class)
        :returns: ID of new image
        """
        id = self._call('saveData', data=base64.b64encode(data), rating=rating)
        if not id:
            raise InvalidDataError()
        return id

    def saveUrl(self, url, rating):
        """
        Read the image pointed to by the URL and save it as a new image in the user account.
        :param url: URL pointing to an image to save
        :param rating: integer rating for the new image (see `Rating`:class)
        :returns: ID of new image
        """
        id = self._call('saveUrl', url=url, rating=rating)
        if not id:
            raise InvalidURLError(url)
        return id

    def useUserimage(self, id, *addresses):
        """
        Assign the image identified by an ID to every email address passed in.
        :param id: image ID to assign
        :param *varargs: list of email addresses
        """
        _check_email_success(self._call('useUserimage', userimage=id, addresses=addresses))

    def removeImage(self, *addresses):
        """
        For every email address passed in, unassign its image.
        :param *varargs: list of email addresses to be unassigned
        """
        _check_email_success(self._call('removeImage', addresses=addresses))

    def deleteUserimage(self, id):
        """
        Delete the image from the user account, and unassign it from any email addresses.
        """
        if not self._call('deleteUserimage', userimage=id):
            raise InvalidUserimageIdError(id)

    def test(self):
        """
        :returns: the server's number of seconds since the current epoch.
        """
        return self._call('test')['response']

    def _call(self, method, **kwargs):
        if self.password is not None:
            kwargs['password'] = self.password
        if self.apikey is not None:
            kwargs['apikey'] = self.apikey

        try:
            return getattr(self._server.grav, method)(kwargs)
        except Fault as fault:
            raise {
                -7: SecureError,
                -8: InternalError,
                -9: AuthenticationError,
                -10: ParameterMissingError,
                -11: ParameterIncorrectError,
                -100: MiscError,
            }.get(fault.faultCode, UnknownError)(fault.faultString)
