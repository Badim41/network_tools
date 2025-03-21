class NetworkToolsError(Exception):
    """base error"""


class NetworkToolsBadRequest(NetworkToolsError):
    """bad request"""


class RiffusionModerationError(NetworkToolsError):
    """moderation error"""


class RiffusionCriticalError(NetworkToolsError):
    """critical riffusion error"""


class RiffusionFileTooLong(NetworkToolsError):
    """File is too long"""


class NetworkToolsCriticalError(NetworkToolsError):
    """unknown error"""


class NetworkToolsTimeout(NetworkToolsError):
    """timeout"""


class UnknownMimetype(NetworkToolsError):
    """no received mimetype"""
