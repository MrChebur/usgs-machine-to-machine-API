import requests
import usgsErrors


def _check_response(response):
    _check_http_response(response)
    _check_usgs_error(response)


def _check_http_response(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print("Http Error:", error)
    except requests.exceptions.ConnectionError as error:
        print("Error Connecting:", error)
    except requests.exceptions.Timeout as error:
        print("Timeout Error:", error)
    except requests.exceptions.RequestException as error:
        print("OOps: Something Else", error)


def _check_usgs_error(response):
    json = response.json()
    errorCode = json['errorCode']
    errorMessage = json['errorMessage']

    if errorCode is None:
        return

    elif errorCode == 'UNKNOWN':
        raise usgsErrors.UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_FORMAT':
        raise usgsErrors.INPUT_FORMAT(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_PARAMETER_INVALID/INPUT_INVALID ':
        raise usgsErrors.INPUT_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_PARAMETER_INVALID':
        raise usgsErrors.INPUT_PARAMETER_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'INPUT_INVALID ':
        raise usgsErrors.INPUT_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'NOT_FOUND':
        raise usgsErrors.NOT_FOUND(f'{errorCode}: {errorMessage}')

    elif errorCode == 'VERSION_UNKNOWN':
        raise usgsErrors.VERSION_UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SERVER_ERROR':
        raise usgsErrors.SERVER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'VERSION_UNKNOWN':
        raise usgsErrors.VERSION_UNKNOWN(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_INVALID':
        raise usgsErrors.AUTH_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_UNAUTHROIZED':
        raise usgsErrors.AUTH_UNAUTHROIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'AUTH_KEY_INVALID':
        raise usgsErrors.AUTH_KEY_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DOWNLOAD_ERROR':
        raise usgsErrors.DOWNLOAD_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_UNAUTHORIZED':
        raise usgsErrors.DATASET_UNAUTHORIZED(f'{errorCode}: {errorMessage}')

    elif errorCode == 'DATASET_INVALID':
        raise usgsErrors.DATASET_INVALID(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SEARCH_ERROR':
        raise usgsErrors.SEARCH_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_ERROR':
        raise usgsErrors.ORDER_ERROR(f'{errorCode}: {errorMessage}')

    elif errorCode == 'ORDER_AUTH':
        raise usgsErrors.ORDER_AUTH(f'{errorCode}: {errorMessage}')

    elif errorCode == 'SUBSCRIPTION_ERROR':
        raise usgsErrors.SUBSCRIPTION_ERROR(f'{errorCode}: {errorMessage}')

    else:
        raise usgsErrors.UNKNOWN(f'{errorCode}: {errorMessage}')
