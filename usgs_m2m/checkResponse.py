import requests
from .usgsErrors import *


def _check_response(response):
    _check_if_response_is_none(response)
    _check_http_response(response)
    _check_usgs_error(response)


def _check_if_response_is_none(response):
    if response is None:
        raise TypeError


def _check_http_response(response):
    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)
        print(response)
    except requests.exceptions.ConnectionError as error:
        print("Error Connecting:", error)
        print(response)
    except requests.exceptions.Timeout as error:
        print("Timeout Error:", error)
        print(response)
    except requests.exceptions.RequestException as error:
        print("Oops: Something Else", error)
        print(response)


def _check_usgs_error(response):
    json = response.json()
    errorCode = json['errorCode']
    errorMessage = json['errorMessage']

    if errorCode is None:
        return True

    elif errorCode == 'ENDPOINT_UNAVAILABLE':
        print(json)
        raise ENDPOINT_UNAVAILABLE(f'{errorCode}: {errorMessage}')

    elif errorCode == 'UNKNOWN':
        print(json)
        raise UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_FORMAT':
        print(json)
        raise INPUT_FORMAT(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_PARAMETER_INVALID':
        print(json)
        raise INPUT_PARAMETER_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_INVALID':
        print(json)
        raise INPUT_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'NOT_FOUND':
        print(json)
        raise NOT_FOUND(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SERVER_ERROR':
        print(json)
        raise SERVER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'VERSION_UNKNOWN':
        print(json)
        raise VERSION_UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_INVALID':
        print(json)
        raise AUTH_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_UNAUTHROIZED':
        print(json)
        raise AUTH_UNAUTHROIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_KEY_INVALID':
        print(json)
        raise AUTH_KEY_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'RATE_LIMIT':
        print(json)
        raise RATE_LIMIT(f'{errorCode}: {errorMessage}')

    elif errorCode == 'RATE_LIMIT_USER_DL':
        print(json)
        raise RATE_LIMIT_USER_DL(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DOWNLOAD_ERROR':
        print(json)
        raise DOWNLOAD_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'EXPORT_ERROR':
        print(json)
        raise EXPORT_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_ERROR':
        print(json)
        raise DATASET_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_UNAUTHORIZED':
        print(json)
        raise DATASET_UNAUTHORIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_AUTH':
        print(json)
        raise DATASET_AUTH(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_INVALID':
        print(json)
        raise DATASET_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_CUSTOM_CLEAR_ERROR':
        print(json)
        raise DATASET_CUSTOM_CLEAR_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_CUSTOM_GET_ERROR':
        print(json)
        raise DATASET_CUSTOM_GET_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_CUSTOMS_GET_ERROR':
        print(json)
        raise DATASET_CUSTOMS_GET_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_CUSTOM_SET_ERROR':
        print(json)
        raise DATASET_CUSTOM_SET_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_CUSTOMS_SET_ERROR':
        print(json)
        raise DATASET_CUSTOMS_SET_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_CREATE_ERROR':
        print(json)
        raise SEARCH_CREATE_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_ERROR':
        print(json)
        raise SEARCH_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_EXECUTE_ERROR':
        print(json)
        raise SEARCH_EXECUTE_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_FAILED':
        print(json)
        raise SEARCH_FAILED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_RESULT_ERROR':
        print(json)
        raise SEARCH_RESULT_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_UNAVAILABLE':
        print(json)
        raise SEARCH_UNAVAILABLE(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_UPDATE_ERROR':
        print(json)
        raise SEARCH_UPDATE_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_ERROR':
        print(json)
        raise ORDER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_AUTH':
        print(json)
        raise ORDER_AUTH(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_INVALID':
        print(json)
        raise ORDER_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'RESTORE_ORDER_ERROR':
        print(json)
        raise RESTORE_ORDER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SUBSCRIPTION_ERROR':
        print(json)
        raise SUBSCRIPTION_ERROR(f'{errorCode}: {errorMessage}')

    else:
        print(json)
        raise UNKNOWN(f'{errorCode}: {errorMessage}')
