import base64
import collections
import hashlib
from   xmlrpclib import Fault, ServerProxy

API_ENDPOINT = 'https://secure.gravatar.com/xmlrpc'

def hash_email(email):
    """
    :returns: the hash of an email address, suitable for embedding in a URL to retrieve its assigned image,
        e.g., ``http://gravatar.com/avatar/<hash>``
    """
    return hashlib.md5(email.strip().lower()).hexdigest()

def _check_email_success(response):
    for email, success in response.iteritems():
        if not success:
            raise InvalidEmailError(email)

class Rating:
    """
    Image rating.
    ====== =====
    Member Value
    ====== =====
    G      0
    PG     1
    R      2
    X      3
    ====== =====
    """
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

class InvalidImageIdError(GravatarError):
    pass

class Image(collections.namedtuple('Image', ['id', 'url', 'rating'])):
    """
    Represents an image in a user account.

    :var id: unique ID used to refer to this image
    :var url: unique URL to retrieve this image, even if it is unassigned
    :var rating: integer rating for the image (see `Rating`:class)
    """
    pass

class User(object):
    """
    Represents a user account.
    """

    def __init__(self, email, password=None, apikey=None):
        """
        At least one of ``password`` and ``apikey`` must be specified.

        :param email: an email address belonging to the account
        :param password: password for the account
        :param apikey: API key for your application
        """
        self._server = ServerProxy(API_ENDPOINT+'?user='+hash_email(email))
        if password is None and apikey is None:
            raise ValueError("Must specify either 'password' or 'apikey' parameter")
        self.password = password
        self.apikey = apikey

    def exists(self, *emails):
        """
        Return a dictionary where each key is an email address from the passed-in list and each
        value is a boolean of whether that email address belongs to a Gravatar account and has an
        image assigned to it.

        :param emails: vararg list of email addresses to check
        """
        hashes = dict([(hash_email(email), email) for email in emails])
        return dict([(hashes[hash], found==1)
                   for hash, found in self._call('exists', hashes=hashes.keys()).iteritems()])

    def emails(self):
        """
        :returns: a dictionary where each key is an email address belonging to the user account and
            each value is the `Image`:class assigned to it, or ``None`` if no image is assigned
        """
        return dict([(email, Image(id=userimage['userimage'], url=userimage['userimage_url'],
                                       rating=userimage['rating'])
                             if len(userimage['userimage']) > 0 else None)
                   for email, userimage in self._call('addresses').iteritems()])

    def images(self):
        """
        :returns: a list of `Image`:class objects belonging to the user account
        """
        return [Image(id=id, url=url, rating=int(rating))
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

    def useImage(self, id, *emails):
        """
        Assign the image identified by an ID to every email address passed in.

        :param id: ID of image to assign
        :param emails: vararg list of email addresses
        """
        _check_email_success(self._call('useUserimage', userimage=id, addresses=emails))

    def removeImage(self, *emails):
        """
        For every email address passed in, unassign its image.

        :param emails: vararg list of email addresses to be unassigned
        """
        _check_email_success(self._call('removeImage', addresses=emails))

    def deleteImage(self, id):
        """
        Delete the image from the user account, and unassign it from any email addresses.

        :param id: ID of image to delete
        """
        if not self._call('deleteUserimage', userimage=id):
            raise InvalidImageIdError(id)

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
