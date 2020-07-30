"""
Implementation date: 30.07.2020

Simple error wrappers.

According to document:
https://m2m.cr.usgs.gov/api/docs/exceptioncodes/
"""


class UNKNOWN(Exception):
    pass


class INPUT_FORMAT(Exception):
    pass


class INPUT_PARAMETER_INVALID(Exception):
    pass


class INPUT_INVALID(Exception):
    pass


class NOT_FOUND(Exception):
    pass


class SERVER_ERROR(Exception):
    pass


class VERSION_UNKNOWN(Exception):
    pass


class AUTH_INVALID(Exception):
    pass


class AUTH_UNAUTHROIZED(Exception):
    pass


class AUTH_KEY_INVALID(Exception):
    pass


class DOWNLOAD_ERROR(Exception):
    pass


class DATASET_UNAUTHORIZED(Exception):
    pass


class DATASET_INVALID(Exception):
    pass


class SEARCH_ERROR(Exception):
    pass


class ORDER_ERROR(Exception):
    pass


class ORDER_AUTH(Exception):
    pass


class SUBSCRIPTION_ERROR(Exception):
    pass
