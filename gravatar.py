import base64
import collections
import hashlib
from   xmlrpclib import Fault, ServerProxy

API_ENDPOINT = 'https://secure.gravatar.com/xmlrpc'

def hash_email(email):
    """
    :param string email: email address
    :returns: the hash of ``email``, suitable for embedding in a URL to retrieve its assigned
        image, e.g., ``http://gravatar.com/avatar/<hash>``
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
    :type id: `string`
    :var url: unique URL to retrieve this image, even if it is unassigned
    :type url: `string`
    :var rating: rating for the image
    :type rating: `int` (see :class:`Rating`)
    """
    pass

class User(object):
    """
    Represents a user account.
    """

    def __init__(self, email, password=None, apikey=None):
        """
        At least one of ``password`` and ``apikey`` must be specified.

        :param string email: an email address belonging to the account
        :param string password: password for the account
        :param string apikey: API key for your application
        """
        self._server = ServerProxy(API_ENDPOINT+'?user='+hash_email(email))
        if password is None and apikey is None:
            raise ValueError("Must specify either 'password' or 'apikey' parameter")
        self.password = password
        self.apikey = apikey

    def exists(self, *emails):
        """
        :param emails: email addresses to check
        :type emails: vararg list of `string`
        :returns: dictionary where each key is an email address from the passed-in list and each
            value is a boolean of whether that email address belongs to a Gravatar account and has
            an image assigned to it.
        :rtype: {`string`: `boolean`}
        """
        hashes = dict([(hash_email(email), email) for email in emails])
        return dict([(hashes[hash], found==1)
                   for hash, found in self._call('exists', hashes=hashes.keys()).iteritems()])

    def emails(self):
        """
        :returns: dictionary where each key is an email address belonging to the user account and
            each value is the :class:`Image` assigned to it, or ``None`` if no image is assigned
        :rtype: {`string`: :class:`Image`}
        """
        return dict([(email, Image(id=userimage['userimage'], url=userimage['userimage_url'],
                                       rating=userimage['rating'])
                             if len(userimage['userimage']) > 0 else None)
                   for email, userimage in self._call('addresses').iteritems()])

    def images(self):
        """
        :returns: images belonging to the user account
        :rtype: list of :class:`Image`
        """
        return [Image(id=id, url=url, rating=int(rating))
                   for id, (rating, url) in self._call('userimages').iteritems()]

    def saveData(self, data, rating):
        """
        Save the data as a new image in the user account.

        :param string data: binary image data to save
        :param rating: rating for the new image
        :type rating: `int` (see :class:`Rating`)
        :returns: ID of new image
        :rtype: `string`
        """
        id = self._call('saveData', data=base64.b64encode(data), rating=rating)
        if not id:
            raise InvalidDataError()
        return id

    def saveUrl(self, url, rating):
        """
        Read the image pointed to by the URL and save it as a new image in the user account.

        :param string url: URL pointing to an image to save
        :param rating: rating for the new image
        :type rating: `int` (see :class:`Rating`)
        :returns: ID of new image
        :rtype: `string`
        """
        id = self._call('saveUrl', url=url, rating=rating)
        if not id:
            raise InvalidURLError(url)
        return id

    def useImage(self, id, *emails):
        """
        Assign the image identified by an ID to every email address passed in.

        :param string id: ID of image to assign
        :param emails: email addresses to assign the image to
        :type emails: vararg list of `string`
        """
        _check_email_success(self._call('useUserimage', userimage=id, addresses=emails))

    def removeImage(self, *emails):
        """
        For every email address passed in, unassign its image.

        :param emails: email addresses to be unassigned
        :type emails: vararg list of `string`
        """
        _check_email_success(self._call('removeImage', addresses=emails))

    def deleteImage(self, id):
        """
        Delete the image from the user account, and unassign it from any email addresses.

        :param string id: ID of image to delete
        """
        if not self._call('deleteUserimage', userimage=id):
            raise InvalidImageIdError(id)

    def test(self):
        """
        :returns: the server's number of seconds since the current epoch.
        :rtype: `int`
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
