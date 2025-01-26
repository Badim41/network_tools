class NetworkToolsError(Exception):
    """base error"""


class NetworkToolsBadRequest(NetworkToolsError):
    """bad request"""


class NetworkToolsTimeout(NetworkToolsError):
    """timeout"""


class UnknownMimetype(NetworkToolsError):
    """no received mimetype"""
