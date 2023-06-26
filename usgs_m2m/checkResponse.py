import requests
import usgs_m2m.usgsErrors


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

    elif errorCode == 'UNKNOWN':
        print(json)
        raise usgsErrors.UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_FORMAT':
        print(json)
        raise usgsErrors.INPUT_FORMAT(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_PARAMETER_INVALID/INPUT_INVALID ':
        print(json)
        raise usgsErrors.INPUT_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_PARAMETER_INVALID':
        print(json)
        raise usgsErrors.INPUT_PARAMETER_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_INVALID ':
        print(json)
        raise usgsErrors.INPUT_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'NOT_FOUND':
        print(json)
        raise usgsErrors.NOT_FOUND(f'{errorCode}: {errorMessage}')

    elif errorCode == 'VERSION_UNKNOWN':
        print(json)
        raise usgsErrors.VERSION_UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SERVER_ERROR':
        print(json)
        raise usgsErrors.SERVER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'VERSION_UNKNOWN':
        print(json)
        raise usgsErrors.VERSION_UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_INVALID':
        print(json)
        raise usgsErrors.AUTH_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_UNAUTHROIZED':
        print(json)
        raise usgsErrors.AUTH_UNAUTHROIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_KEY_INVALID':
        print(json)
        raise usgsErrors.AUTH_KEY_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DOWNLOAD_ERROR':
        print(json)
        raise usgsErrors.DOWNLOAD_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_UNAUTHORIZED':
        print(json)
        raise usgsErrors.DATASET_UNAUTHORIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_INVALID':
        print(json)
        raise usgsErrors.DATASET_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_ERROR':
        print(json)
        raise usgsErrors.SEARCH_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_ERROR':
        print(json)
        raise usgsErrors.ORDER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_AUTH':
        print(json)
        raise usgsErrors.ORDER_AUTH(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SUBSCRIPTION_ERROR':
        print(json)
        raise usgsErrors.SUBSCRIPTION_ERROR(f'{errorCode}: {errorMessage}')

    else:
        print(json)
        raise usgsErrors.UNKNOWN(f'{errorCode}: {errorMessage}')
