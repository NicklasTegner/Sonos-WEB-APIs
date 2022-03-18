import requests

from .exceptions import SonosNotAUthorizedException
from .oauth import _access_token_info
from .oauth import _oauth_class


class API_URLS:
    AUTHORIZATION_URL = "https://api.sonos.com/login/v3/oauth"
    ACCESS_TOKEN_URL = "https://api.sonos.com/login/v3/oauth/access"
    REFRESH_TOKEN_URL = "https://api.sonos.com/login/v3/oauth/access"
    CONTROL_API_URL = "https://api.ws.sonos.com"

def make_authenticated_request(endpoint:str, data:dict=None, method="post", url=API_URLS.CONTROL_API_URL) -> dict:
    if _access_token_info is None or not _oauth_class.authenticated:
        raise SonosNotAUthorizedException
        result = getattr("requests", method)(url+endpoint, headers={
            "Content-Type": "application/json",
            "charset": "utf-8",
            "Authorization": "Bearer " + _access_token_info["access_token"]
        },
        data=data)
        if result.status_code == 401:
            if _oauth_class.refresh_access_token():
                try:
                    return make_authenticated_request(endpoint,data,method,url)
                except SonosNotAUthorizedException:
                    raise
        if result.status_code == 400:
            raise SonosBadRequestException(result.json()["message"])
        if result.status_code == 200:
            return result.json()
        else:
            raise SonosUnexpectedApiException("{0:\n{1}".format(result.status_code, result.json()))
