import json
from usgsDataTypes import usgsDataTypes
from usgsMethods import usgsMethods
from otherMethods import otherMethods
from pprint import pprint


def main():
    # In order not to store the login/password in the code - auth with json-formatted text file:
    # {"username": "username", "password": "password"}
    txt_path = r"G:\Scripts\py_test\USGS\m2mAPI\json_pass.txt"
    with open(txt_path, 'r') as file:
        json_data = json.load(file)
        usgs_username = json_data['username']
        usgs_password = json_data['password']

    api = usgsMethods()  # instance created
    api.login(usgs_username, usgs_password)
    api.loud_mode = True

    # show your permissions
    permissions = api.permissions()
    print(f"Your login permissions is {permissions['data']}", end='\n' * 2)

    datasetName = 'LANDSAT_8_C1'

    # Let's find some scenes by location!
    # Region of interest coordinates. Too long coordinates list may throw 404 HTTP errors!
    # Examples:
    # 'Point' [lat ,lon]
    # 'Polygon' [[ [lat ,lon], [lat ,lon], ... ]]
    ROI = [[
        [59.19852, 63.06039],
        [59.62473, 64.80140],
        [62.05751, 65.70580],
        [62.86149, 65.26510],
        [63.24590, 64.51990],
        [65.99469, 64.58008],
        [66.97107, 64.50871],
        [67.49873, 64.08241],
        [68.96698, 64.44441],
        [70.34046, 64.31480],
        [71.58613, 63.35573],
        [73.10955, 63.37922],
        [76.69435, 63.02787],
        [77.98457, 62.51861],
        [79.89941, 62.77741],
        [81.03670, 63.14609],
        [83.96038, 62.48975],
        [85.97549, 61.48612],
        [84.16387, 60.85305],
        [82.12599, 60.53366],
        [77.11535, 60.73926],
        [76.67393, 59.58814],
        [74.99998, 58.69959],
        [72.52650, 59.15018],
        [69.39066, 59.91733],
        [66.74067, 58.64882],
        [65.70599, 58.65047],
        [61.15117, 61.67129],
        [59.40793, 62.09941],
        [59.19852, 63.06039],
    ]]

    geoJson = usgsDataTypes.GeoJson(type='Polygon', coordinates=ROI)
    spatialFilter = usgsDataTypes.SpatialFilterGeoJson(filterType='geojson', geoJson=geoJson)
    acquisitionFilter = usgsDataTypes.AcquisitionFilter(start="2020-07-30", end="2020-07-31")
    sceneFilter = usgsDataTypes.SceneFilter(acquisitionFilter=acquisitionFilter,
                                            cloudCoverFilter=None,
                                            datasetName=datasetName,
                                            ingestFilter=None,
                                            metadataFilter=None,
                                            seasonalFilter=None,
                                            spatialFilter=spatialFilter)
    # print('sceneFilter=')
    # pprint(sceneFilter)

    sceneSearchResult = api.sceneSearch(datasetName=datasetName, maxResults=1, startingNumber=None,
                                        metadataType='full',
                                        sortField=None,
                                        sortDirection='ASC',
                                        sceneFilter=sceneFilter,
                                        compareListName=None,
                                        bulkListName=None,
                                        orderListName=None,
                                        excludeListName=None)
    # print('sceneSearchResult=')
    # pprint(sceneSearchResult)

    print(f"\nDownloading:")

    productName = 'LandsatLook Quality Image'
    for searchResult in sceneSearchResult['data']['results']:
        entityId = searchResult['entityId']
        filesize = otherMethods.request_filesize(api, datasetName=datasetName, productName=productName, entityId=entityId)

        print(f"The file size of {productName} with entityId={entityId} is {filesize} bytes", end='\n' * 2)

        results = otherMethods.download(api, datasetName=datasetName, entityIds=entityId, productName=productName,
                                        output_dir=r'G:\!Download')
        print(results)

    api.logout()
    print('Done!')


if __name__ == '__main__':
    main()
