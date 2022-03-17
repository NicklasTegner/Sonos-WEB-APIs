class SonosException(ValueError):
    """A generic Sonos Exception"""
    pass
    

class SonosUnexpectedApiException(SonosException):
    """This exception is raised, if an unexpected return code are returned from the Sonos Cloud APIs"""
    pass

class SonosNotAUthorizedException(SonosException):
    """This exception is raised, if a method you are trying to call, needs authorization"""
    pass    

class SonosBadRequestException(SonosException): # for a 400 error
    """This exception is raised, if something is missing or invalid with the request you sent to the Sonos Cloud APIs"""
    pass

class SonosUnauthorizedRequestException(SonosException): #for 401
    pass
