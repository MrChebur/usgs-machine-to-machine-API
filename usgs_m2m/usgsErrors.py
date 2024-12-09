"""
Implementation date: 30.07.2020
Revision date: 20.11.2024

Simple error wrappers.

According to document:
https://m2m.cr.usgs.gov/api/docs/exceptioncodes/
"""


#  ======================= Module `General` =======================

class ENDPOINT_UNAVAILABLE(Exception):
    pass


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


#  ======================= Module `Authentication` =======================
class AUTH_INVALID(Exception):
    pass


class AUTH_UNAUTHROIZED(Exception):
    pass


class AUTH_KEY_INVALID(Exception):
    pass


#  ======================= Module `Rate Limit` =======================

class RATE_LIMIT(Exception):
    pass


class RATE_LIMIT_USER_DL(Exception):
    pass


#  ======================= Module `Download` =======================


class DOWNLOAD_ERROR(Exception):
    pass


#  ======================= Module `Export` =======================

class EXPORT_ERROR(Exception):
    pass


#  ======================= Module `Inventory` =======================


class DATASET_ERROR(Exception):
    pass


class DATASET_UNAUTHORIZED(Exception):
    pass


class DATASET_AUTH(Exception):
    pass


class DATASET_INVALID(Exception):
    pass


class DATASET_CUSTOM_CLEAR_ERROR(Exception):
    pass


class DATASET_CUSTOM_GET_ERROR(Exception):
    pass


class DATASET_CUSTOMS_GET_ERROR(Exception):
    pass


class DATASET_CUSTOM_SET_ERROR(Exception):
    pass


class DATASET_CUSTOMS_SET_ERROR(Exception):
    pass


class SEARCH_CREATE_ERROR(Exception):
    pass


class SEARCH_ERROR(Exception):
    pass


class SEARCH_EXECUTE_ERROR(Exception):
    pass


class SEARCH_FAILED(Exception):
    pass


class SEARCH_RESULT_ERROR(Exception):
    pass


class SEARCH_UNAVAILABLE(Exception):
    pass


class SEARCH_UPDATE_ERROR(Exception):
    pass


#  ======================= Module `Orders` =======================

class ORDER_ERROR(Exception):
    pass


class ORDER_AUTH(Exception):
    pass


class ORDER_INVALID(Exception):
    pass


class RESTORE_ORDER_ERROR(Exception):
    pass


#  ======================= Module `Subscription` s=======================


class SUBSCRIPTION_ERROR(Exception):
    pass
