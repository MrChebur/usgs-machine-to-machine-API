import json
from pprint import pprint
from pathlib import Path

from usgs_m2m import API as M2M
from usgs_m2m import otherMethods
from usgs_m2m.usgsDataTypes import (GeoJson,
                                    SpatialFilterGeoJson,
                                    AcquisitionFilter,
                                    SceneFilter,
                                    )


def example_search_scene_and_download_quicklook():
    print()
    # In order not to store the login/password in the code - auth with json-formatted text file:
    # {"username": "username", "password": "password"}
    txt_path = r"E:\kupriyanov\!auth\query_usgs_auth.json"

    with open(txt_path, 'r') as file:
        json_data = json.load(file)
        usgs_username = json_data['usgs_username1']
        usgs_token = json_data['usgs_token1']

    api = M2M()  # instance created
    api.loginToken(usgs_username, usgs_token)  # this is new login method
    api.loud_mode = True

    # Region of interest coordinate. Too long coordinates list may throw 404 HTTP errors!
    # Examples:
    # 'Point' [lat ,lon]
    # 'Polygon' [[ [lat ,lon], ... ]]
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

    datasetName = 'landsat_ot_c2_l1'

    geoJson = GeoJson(type='Polygon', coordinates=ROI).dict
    spatialFilter = SpatialFilterGeoJson(filterType='geojson', geoJson=geoJson).dict
    acquisitionFilter = AcquisitionFilter(start="2020-07-30", end="2020-07-31").dict
    sceneFilter = SceneFilter(acquisitionFilter=acquisitionFilter,
                              cloudCoverFilter=None,
                              datasetName=datasetName,
                              ingestFilter=None,
                              metadataFilter=None,
                              seasonalFilter=None,
                              spatialFilter=spatialFilter).dict
    # print('\nsceneFilter=')
    # pprint(sceneFilter)
    #
    # When using polygons in the sceneSearch method, images that do not lie within the boundaries of the polygon are returned.
    # This is due to the fact that the contours of the images lie at the border of 180/-180 degrees in the projection WGS 84 (EPSG: 4326).
    sceneSearchResult = api.sceneSearch(datasetName=datasetName,
                                        maxResults=1,
                                        startingNumber=None,
                                        metadataType='full',
                                        sortField=None,  # "Acquisition Date", '5e83d0b92ff6b5e8' - doesn't work
                                        sortDirection='ASC',
                                        sceneFilter=sceneFilter,
                                        compareListName=None,
                                        bulkListName=None,
                                        orderListName=None,
                                        excludeListName=None)
    # print('\nsceneSearchResult=')
    # pprint(sceneSearchResult)

    dataset_info = api.dataset(datasetName=datasetName)
    dataset_alias = dataset_info['data']['datasetAlias']
    print(f'dataset_alias={dataset_alias}')

    entityId = None
    for searchResult in sceneSearchResult['data']['results']:
        entityId = searchResult['entityId']
        print(f'Scene name (entityId): {entityId}')

    # pprint(dataset_info)

    print(f'\nSearching {dataset_alias} dataset products...')
    products = api.datasetBulkProducts(dataset_alias)
    # pprint(products)

    product_name_natural_colors = None
    for product in products['data']:
        product_name = product['productName']
        if 'geotiff' in product_name.lower() and 'natural' in product_name.lower():
            product_name_natural_colors = product_name

    print(f'Downloading product: {product_name_natural_colors}')
    results = otherMethods.download(api,
                                    datasetName=datasetName,
                                    entityId=entityId,
                                    output_dir=Path(r'.\\').resolve(),
                                    productName=product_name_natural_colors)
    print(results)
    api.logout()


def example_print_scene_size():
    # In order not to store the login/password in the code - auth with json-formatted text file:
    # {"username": "username", "password": "password"}
    txt_path = r"E:\kupriyanov\!auth\query_usgs_auth.json"
    with open(txt_path, 'r') as file:
        json_data = json.load(file)
        usgs_username = json_data['usgs_username1']
        usgs_password = json_data['usgs_password1']

    api = M2M()  # instance created
    api.login(usgs_username, usgs_password)  # login method will be deprecated in February 2025
    api.loud_mode = True

    datasetName = 'LANDSAT_OT_C2_L1'

    filesize_usgs = otherMethods.request_filesize(api,
                                                  datasetName,
                                                  productName='Landsat Collection 2 Level-1 Product Bundle',
                                                  entityId='LC81650162022019LGN00')
    print(f'filesize_usgs={filesize_usgs} bytes')
    api.logout()
    print('Done!')


if __name__ == '__main__':
    print('\nExecuting `example_print_scene_size()`')
    example_print_scene_size()

    print('\nExecuting `example_search_scene_and_download_quicklook()`')
    example_search_scene_and_download_quicklook()
