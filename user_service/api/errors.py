__all__ = ("ServiceError",
           "BadLogout",
           "BadLoginData",
           "BadAuthData",
           "BadRegData")


class ServiceError(Exception):
    status = -1
    message = ""

    def __init__(self):
        Exception.__init__(self, self.status, self.message)


class BadLogout(ServiceError):
    """ Exception raised for error in logout endpoint.
        raised if refresh token doesnt exist in redis """

    status = 411
    message = "Invalid refresh token"


class BadLoginData(ServiceError):
    """ Exception raised for error in login endpoint.
        raised if user with such log/pass combo doesnt exist """

    status = 412
    message = "User with this username and password was not found"


class BadAuthData(ServiceError):
    """ Exception raised for error in all endpoints.
        raised if user's access token incorrect/expired """

    status = 413
    message = "Bad Authentication data"


class BadRegData(ServiceError):
    """ Exception raised for error in registration endpoint.
        raised if user with such log/pass combo doesnt exist """

    status = 414
    message = "User with this username and password already exist"
