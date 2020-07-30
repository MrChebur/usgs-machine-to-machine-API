import requests
from checkResponse import _check_response


class usgsMethods:
    """
    Official USGS/EROS Inventory Service Documentation (Machine-to-Machine API):
    https://m2m.cr.usgs.gov/api/docs/json/
    """

    apiURL = r'https://m2m.cr.usgs.gov/api/api/json/stable/'  # must ends with slash - "/"
    apiKey = None
    loud_mode = True

    def dataOwner(self, dataOwner):
        """
        :param dataOwner:
        :return:
        """

        url = f'{self.apiURL}data-owner'
        json_payload = {"dataOwner": dataOwner}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def dataset(self, datasetId=None, datasetName=None):
        """

        :param datasetId:
        :param datasetName:
        :return:
        """

        if all(v is None for v in {datasetId, datasetName}):
            raise ValueError('datasetId or datasetName must be used.')

        elif all(v is not None for v in {datasetId, datasetName}):
            raise ValueError('datasetId or datasetName must be used, not both!')

        url = f'{self.apiURL}dataset'
        json_payload = {"datasetId": datasetId,
                        "datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetBulkProducts(self, datasetName):
        """

        :param datasetName:
        :return:
        """
        url = f'{self.apiURL}dataset-bulk-products'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetCategories(self, catalog, includeMessages=False, publicOnly=False, parentId=None, datasetFilter=None):
        """

        :param catalog:
        :param includeMessages:
        :param publicOnly:
        :param parentId:
        :param datasetFilter:
        :return:
        """
        url = f'{self.apiURL}dataset-categories'
        json_payload = {"catalog": catalog,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "parentId": parentId,
                        "datasetFilter": datasetFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetCoverage(self, datasetName):
        """

        :param datasetName:
        :return:
        """
        url = f'{self.apiURL}dataset-coverage'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetDownloadOptions(self, datasetName, sceneFilter=None):
        """

        :param datasetName:
        :param sceneFilter:
        :return:
        """
        url = f'{self.apiURL}dataset-download-options'
        json_payload = {"datasetName": datasetName,
                        "sceneFilter": sceneFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetFilters(self, datasetName):
        """

        :param datasetName:
        :return:
        """

        url = f'{self.apiURL}dataset-filters'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetMessages(self, catalog=None, datasetName=None, datasetNames=None):
        """

        :param catalog:
        :param datasetName:
        :param datasetNames:
        :return:
        """
        url = f'{self.apiURL}dataset-messages'
        json_payload = {"catalog": catalog,
                        "datasetName": datasetName,
                        "datasetNames": datasetNames,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetOrderProducts(self, datasetName):
        """

        :param datasetName:
        :return:
        """
        url = f'{self.apiURL}dataset-order-products'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetSearch(self, catalog=None, datasetName=None, includeMessages=None, publicOnly=None, temporalFilter=None,
                      spatialFilter=None):
        """

        :param catalog:
        :param datasetName:
        :param includeMessages:
        :param publicOnly:
        :param temporalFilter:
        :param spatialFilter:
        :return:
        """
        url = f'{self.apiURL}dataset-search'
        json_payload = {"catalog": catalog,
                        "datasetName": datasetName,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "temporalFilter": temporalFilter,
                        "spatialFilter": spatialFilter,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadEula(self, eulaCode, eulaCodes):
        """

        :param eulaCode:
        :param eulaCodes:
        :return:
        """
        url = f'{self.apiURL}download-eula'
        json_payload = {"eulaCode": eulaCode,
                        "eulaCodes": eulaCodes}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadLabels(self, downloadApplication):
        """

        :param downloadApplication:
        :return:
        """
        url = f'{self.apiURL}download-labels'
        json_payload = {"downloadApplication": downloadApplication}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadOptions(self, datasetName, entityIds=None, listId=None):
        """

        :param datasetName:
        :param entityIds:
        :param listId:
        :return:
        """
        url = f'{self.apiURL}download-options'
        json_payload = {"datasetName": datasetName,
                        "entityIds": entityIds,
                        "listId": listId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadOrderLoad(self, downloadApplication=None, label=None):
        """

        :param downloadApplication:
        :param label:
        :return:
        """
        url = f'{self.apiURL}download-options'
        json_payload = {"downloadApplication": downloadApplication,
                        "label": label,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadOrderRemove(self, label, downloadApplication=None):
        """

        :param label:
        :param downloadApplication:
        :return:
        """
        url = f'{self.apiURL}download-order-remove'
        json_payload = {"downloadApplication": downloadApplication,
                        "label": label,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadRemove(self, downloadId):
        """

        :param downloadId:
        :return:
        """
        url = f'{self.apiURL}download-order-remove'
        json_payload = {"downloadId": downloadId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadRequest(self, configurationCode=None, downloadApplication=None,
                        downloads=None, dataPaths=None, label=None, returnAvailable=False):
        """

        :param configurationCode:
        :param downloadApplication:
        :param downloads:
        :param dataPaths:
        :param label:
        :param returnAvailable:
        :return:
        """
        url = f'{self.apiURL}dataset-search'
        json_payload = {"configurationCode": configurationCode,
                        "downloadApplication": downloadApplication,
                        "downloads": downloads,
                        "dataPaths": dataPaths,
                        "label": label,
                        "returnAvailable": returnAvailable,  # this may be undocumented parameter
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadRetrieve(self, downloadApplication=None, label=None):
        """

        :param downloadApplication:
        :param label:
        :return:
        """
        url = f'{self.apiURL}download-retrieve'
        json_payload = {"label": label,
                        "downloadApplication": downloadApplication,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadSearch(self, activeOnly=None, label=None, downloadApplication=None):
        """

        :param activeOnly:
        :param label:
        :param downloadApplication:
        :return:
        """
        url = f'{self.apiURL}download-search'
        json_payload = {"activeOnly": activeOnly,
                        "label": label,
                        "downloadApplication": downloadApplication,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadSummary(self, downloadApplication, label, sendEmail=None):
        """

        :param downloadApplication:
        :param label:
        :param sendEmail:
        :return:
        """
        url = f'{self.apiURL}download-summary'
        json_payload = {"downloadApplication": downloadApplication,
                        "label": label,
                        "sendEmail": sendEmail,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def grid2ll(self, gridType, responseShape=None, path=None, row=None):
        """

        :param gridType:
        :param responseShape:
        :param path:
        :param row:
        :return:
        """
        url = f'{self.apiURL}download-summary'
        json_payload = {"gridType": gridType,
                        "responseShape": responseShape,
                        "path": path,
                        "row": row,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        url = f'{self.apiURL}login'
        json_payload = {"username": username,
                        "password": password}
        response = requests.post(url, json=json_payload)
        _check_response(response)
        self.apiKey = response.json()['data']
        if self.loud_mode:
            print(f'Login successful. API key: {self.apiKey}')
        return response.json()

    def logout(self):
        """

        :return:
        """
        url = f'{self.apiURL}logout'
        response = requests.post(url, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        if self.loud_mode:
            print(f'Logout successful. API key destroyed: {self.apiKey}')
        return response.json()

    def notifications(self, systemId):
        """

        :param systemId:
        :return:
        """
        url = f'{self.apiURL}notifications'
        json_payload = {"systemId": systemId}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def orderProducts(self, datasetName, entityIds=None, listId=None):
        """

        :param datasetName:
        :param entityIds:
        :param listId:
        :return:
        """
        url = f'{self.apiURL}order-products'
        json_payload = {"datasetName": datasetName,
                        "entityIds": entityIds,
                        "listId": listId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def orderSubmit(self, products, autoBulkOrder=None, processingParameters=None, priority=None,
                    orderComment=None, systemId=None):
        """

        :param products:
        :param autoBulkOrder:
        :param processingParameters:
        :param priority:
        :param orderComment:
        :param systemId:
        :return:
        """
        url = f'{self.apiURL}order-submit'
        json_payload = {"autoBulkOrder": autoBulkOrder,
                        "products": products,
                        "processingParameters": processingParameters,
                        "priority": priority,
                        "orderComment": orderComment,
                        "systemId": systemId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def permissions(self):
        """

        :return:
        """
        url = f'{self.apiURL}permissions'
        response = requests.post(url, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListAdd(self, listId, datasetName, idField=None, entityId=None, entityIds=None):
        """

        :param listId:
        :param datasetName:
        :param idField:
        :param entityId:
        :param entityIds:
        :return:
        """

        url = f'{self.apiURL}scene-list-add'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        "idField": idField,
                        "entityId": entityId,
                        "entityIds": entityIds,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListGet(self, listId, datasetName=None):
        """

        :param listId:
        :param datasetName:
        :return:
        """
        url = f'{self.apiURL}scene-list-get'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListRemove(self, listId, datasetName, entityId=None, entityIds=None):
        """

        :param listId:
        :param datasetName:
        :param entityId:
        :param entityIds:
        :return:
        """
        url = f'{self.apiURL}scene-list-remove'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        "entityId": entityId,
                        "entityIds": entityIds,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListSummary(self, listId, datasetName=None):
        """

        :param listId:
        :param datasetName:
        :return:
        """
        url = f'{self.apiURL}scene-list-summary'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListTypes(self, listFilter=None):
        """

        :param listFilter:
        :return:
        """
        url = f'{self.apiURL}scene-list-types'
        json_payload = {"listFilter": listFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadata(self, datasetName, entityId, metadataType=None):
        """

        :param datasetName:
        :param entityId:
        :param metadataType:
        :return:
        """
        url = f'{self.apiURL}scene-metadata'
        json_payload = {"datasetName": datasetName,
                        "entityId": entityId,
                        "metadataType": metadataType,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadataList(self, listId, datasetName=None, metadataType=None):
        """

        :param listId:
        :param datasetName:
        :param metadataType:
        :return:
        """
        url = f'{self.apiURL}scene-metadata-list'
        json_payload = {"datasetName": datasetName,
                        "listId": listId,
                        "metadataType": metadataType,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadataXML(self, datasetName, entityId, metadataType=None):
        """

        :param datasetName:
        :param entityId:
        :param metadataType:
        :return:
        """
        url = f'{self.apiURL}scene-metadata-xml'
        json_payload = {"datasetName": datasetName,
                        "entityId": entityId,
                        "metadataType": metadataType,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneSearch(self, datasetName, maxResults=None, startingNumber=None, metadataType=None, sortField=None,
                    sortDirection=None, sceneFilter=None, compareListName=None, bulkListName=None, orderListName=None,
                    excludeListName=None):
        """

        :param datasetName:
        :param maxResults:
        :param startingNumber:
        :param metadataType:
        :param sortField:
        :param sortDirection:
        :param sceneFilter:
        :param compareListName:
        :param bulkListName:
        :param orderListName:
        :param excludeListName:
        :return:
        """
        url = f'{self.apiURL}scene-search'
        json_payload = {"datasetName": datasetName,
                        "maxResults": maxResults,
                        "startingNumber": startingNumber,
                        "metadataType": metadataType,
                        "sortField": sortField,
                        "sortDirection": sortDirection,
                        "sceneFilter": sceneFilter,
                        "compareListName": compareListName,
                        "bulkListName": bulkListName,
                        "orderListName": orderListName,
                        "excludeListName": excludeListName,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneSearchDelete(self, datasetName, maxResults=None, startingNumber=None, sortField=None, sortDirection=None,
                          temporalFilter=None):
        """

        :param datasetName:
        :param maxResults:
        :param startingNumber:
        :param sortField:
        :param sortDirection:
        :param temporalFilter:
        :return:
        """
        url = f'{self.apiURL}scene-search-delete'
        json_payload = {"datasetName": datasetName,
                        "maxResults": maxResults,
                        "startingNumber": startingNumber,
                        "sortField": sortField,
                        "sortDirection": sortDirection,
                        "temporalFilter": temporalFilter
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneSearchSecondary(self, entityId, datasetName, maxResults=None, startingNumber=None, metadataType=None,
                             sortField=None, sortDirection=None, compareListName=None, bulkListName=None,
                             orderListName=None, excludeListName=None):
        """

        :param entityId:
        :param datasetName:
        :param maxResults:
        :param startingNumber:
        :param metadataType:
        :param sortField:
        :param sortDirection:
        :param compareListName:
        :param bulkListName:
        :param orderListName:
        :param excludeListName:
        :return:
        """
        url = f'{self.apiURL}scene-search-secondary'
        json_payload = {"entityId": entityId,
                        "datasetName": datasetName,
                        "maxResults": maxResults,
                        "startingNumber": startingNumber,
                        "metadataType": metadataType,
                        "sortField": sortField,
                        "sortDirection": sortDirection,
                        "compareListName": compareListName,
                        "bulkListName": bulkListName,
                        "orderListName": orderListName,
                        "excludeListName": excludeListName,

                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def tramOrderSearch(self, orderId=None, maxResults=None, systemId=None, sortAsc=None, sortField=None,
                        statusFilter=None):
        """

        :param orderId:
        :param maxResults:
        :param systemId:
        :param sortAsc:
        :param sortField:
        :param statusFilter:
        :return:
        """
        url = f'{self.apiURL}tram-order-search'
        json_payload = {"orderId": orderId,
                        "maxResults": maxResults,
                        "systemId": systemId,
                        "sortAsc": sortAsc,
                        "sortField": sortField,
                        "statusFilter": statusFilter,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def tramOrderStatus(self, orderNumber):
        """

        :param orderNumber:
        :return:
        """
        url = f'{self.apiURL}tram-order-status'
        json_payload = {"orderNumber": orderNumber}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def tramOrderUnits(self, orderNumber):
        """

        :param orderNumber:
        :return:
        """

        url = f'{self.apiURL}tram-order-units'
        json_payload = {"orderNumber": orderNumber}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()
