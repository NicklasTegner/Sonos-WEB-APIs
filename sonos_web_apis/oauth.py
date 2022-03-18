import base64
import random
import string

import requests

from .exceptions import SonosBadRequestException
from .exceptions import SonosException
from .exceptions import SonosNotAUthorizedException
from .exceptions import SonosUnauthorizedRequestException
from .exceptions import SonosUnexpectedApiException
from .utils import API_URLS

_access_token_info = None
_oauth_class = None

class Oauth:
    """This is the authorization class for the Sonos Cloud APIs."""
    
    def __init_(self, client_id:str, client_secret:str, redirect_uri:str):
        """Initialization

        Args:
            client_id (str): Your sonos client id
            client_secret (str): Your sonos client secret
            redirect_uri (str): The same redirect uri, you have specified on the setting page for your snos application.
        
        :meta public:
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._state = None
        self.authorized = False
    
    def get_oauth_url(self) -> str:
        """Get the sonos authorization url with scopes, state and your parameters formatted. This is what you'll redirect your users to, for them to authorize your application.

        Returns:
            authorization url (str): The url
        """
        self._state = ''.join(random.choices(string.ascii + string.digits, k=20))
        return API_URLS.AUTHORIZATION_URL+"?client_id="+self.client_id+"response_type=code&state"+self._state+"scope=playback-control-all&redirect_uri="+self.redirect_uri
    
    def authorize(self, code:str) -> bool:
        """This is what gets the access and refresh token from the Sonos API. Call this, after your user gets redirected back to your application, with an authorization code.

        Args:
            code (str): The code returned from the oauth2 flow.n_

        Raises:
            SonosBadRequestException: Something was wrong with the request. More information is attached to the exception object
            SonosUnauthorizedRequestException: You don't have permission to use the api.
            SonosUnexpectedApiException: Something else went wrong. Shouldn't really happen. More information is attached to the exception object.

        Returns:
            authorized (bool): True if the retrival of an access token was successful, False otherwise.
        """
        global _access_token_info, _oauth_class
        client_id_plus_secret = self.client_id+":"+self.client_secret
        result = requests.post(API_URLS.ACCESS_TOKEN_URL, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "charset": "utf-8",
            "Authorization": "Basic " + base64.b64encode(client_id_plus_secret.encode("ascii")).decode("ascii")
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "state": self._state
        })
        if result.status_code == 400:
            raise SonosBadRequestException(result.json()["message"])
        if result.status_code == 401:
            raise SonosUnauthorizedRequestException("invalid_request")
        if result.status_code == 200: # success
            _access_token_info = result.json()
            _oauth_class = self
            self.authorize = True
            return True
        else:
            raise SonosUnexpectedApiException("{0:\n{1}".format(result.status_code, result.json()))
            return False

    def refresh_access_token(self) -> bool:
        """Refresh an existing access token.

        Raises:
            SonosBadRequestException: Something was wrong with the request. More information is attached to the exception object
            SonosUnauthorizedRequestException: You don't have permission to use the api.
            SonosUnexpectedApiException: Something else went wrong. Shouldn't really happen. More information is attached to the exception object.

        Returns:
            authorized (bool): True if the retrival of an access token was successful, False otherwise.
        """
        global _access_token_info
        client_id_plus_secret = self.client_id+":"+self.client_secret
        if not self.authorize:
            raise SonosNotAUthorizedException("The library is not authorized yet.")
        result = requests.post(API_URLS.REFRESH_TOKEN_URL, headers={
		"Content-Type": "application/x-www-form-urlencoded",
		"charset": "utf-8",
		"Authorization": "Basic " + base64.b64encode(client_id_plus_secret.encode("ascii")).decode("ascii")
	},data={
		"grant_type": "refresh_token",
		"refresh_token": _access_token_info["refresh_token"]
	})
        if result.status_code == 400:
            raise SonosBadRequestException(result.json()["message"])
        if result.status_code == 401:
            raise SonosUnauthorizedRequestException("invalid_request")
        if result.status_code == 200:
            _access_token_info = result.json()
            self.authorize = True
            return True
        else:
            raise SonosUnexpectedApiException("{0:\n{1}".format(result.status_code, result.json()))
            return False
