import json
import time
from pprint import pprint
from usgsDataTypes import usgsDataTypes
from usgsMethods import usgsMethods



def main():
    # In order not to store the login/password in the code - auth with json-formatted text file:
    # {"username": "username", "password": "password"}
    txt_path = r"G:\Scripts\py_test\USGS\m2mAPI\json_pass.txt"
    with open(txt_path, 'r') as f:
        json_data = json.load(f)
        usgs_username = json_data['username']
        usgs_password = json_data['password']

    api = usgsMethods()
    api.login(usgs_username, usgs_password)

    a = {
        "maxResults": 100,
        "datasetName": "gls_all",
        "sceneFilter": {
            "ingestFilter": None,
            "spatialFilter": None,
            "metadataFilter": None,
            "cloudCoverFilter": {
                "max": 100,
                "min": 0,
                "includeUnknown": True
            },
            "acquisitionFilter": None
        },
        "bulkListName": "my_bulk_list",
        "metadataType": "summary",
        "orderListName": "my_order_list",
        "startingNumber": 1,
        "compareListName": "my_comparison_list",
        "excludeListName": "my_exclusion_list"
    }

    # result = api.sceneSearch(datasetName='LANDSAT_8_C1', maxResults=10, startingNumber=None, metadataType=None,
    #                          sortField=None,
    #                          sortDirection=None, sceneFilter=None, compareListName=None, bulkListName=None,
    #                          orderListName=None,
    #                          excludeListName=None)

    result = usgsDataTypes.General.CloudCoverFilter(1, 2, 3)
    pprint(result)

    perm = api.permissions()
    print(f'perm={type(perm)} {perm}')

    log = api.logout()
    print(f'log={type(log)} {log}')
    print(f'api.apiKey={type(api.apiKey)} {api.apiKey}')
    time.sleep(5)



    perm = api.permissions()
    print(f'perm={type(perm)} {perm}')

    api.apiKey = None
    print(f'api.apiKey={type(api.apiKey)} {api.apiKey}')

    perm = api.permissions()
    print(f'perm={type(perm)} {perm}')

    pprint('Done!')


if __name__ == '__main__':
    main()
