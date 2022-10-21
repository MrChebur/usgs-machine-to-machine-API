import requests
from usgs_m2m.checkResponse import _check_response


class usgsMethods:
    """
    Implementation date: 12.03.2021

    Wrapper for Official USGS/EROS Inventory Service Documentation (Machine-to-Machine API):
    https://m2m.cr.usgs.gov/api/docs/json/

    According to document:
    https://m2m.cr.usgs.gov/api/docs/reference/
    """

    apiURL = r'https://m2m.cr.usgs.gov/api/api/json/stable/'  # must ends with slash: "/"
    apiKey = None
    loud_mode = False

    def dataOwner(self, dataOwner):
        """
        This method is used to provide the contact information of the data owner.
        :param dataOwner: (string) Used to identify the data owner - this value comes from the dataset-search response
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}data-owner'
        json_payload = {"dataOwner": dataOwner}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def dataset(self, datasetId=None, datasetName=None):
        """
        This method is used to retrieve the dataset by id or name.
        :param datasetId: (string) The dataset identifier - must use this or datasetName
        :param datasetName: (string) The system-friendly dataset name - must use this or datasetId
        :return: (dict) Response as a dictionary
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
        Lists all available bulk products for a dataset - this does not guarantee scene availability.
        :param datasetName: (str)  	Used to identify the which dataset to return results for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-bulk-products'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetCategories(self, catalog=None, includeMessages=False, publicOnly=False, useCustomization=False,
                          parentId=None, datasetFilter=None):
        """
        This method is used to search datasets under the categories.
        :param catalog: (string) Used to identify datasets that are associated with a given application
        :param includeMessages: (boolean) Optional parameter to include messages regarding specific dataset components
        :param publicOnly: (boolean) Used as a filter out datasets that are not accessible to unauthenticated general public users
        :param useCustomization (boolean) Used as a filter out datasets that are excluded by user customization
        :param parentId: (string) If provided, returned categories are limited to categories that are children of the provided ID
        :param datasetFilter: (string) If provided, filters the datasets - this automatically adds a wildcard before and after the input value
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-categories'
        json_payload = {"catalog": catalog,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "useCustomization": useCustomization,
                        "parentId": parentId,
                        "datasetFilter": datasetFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetClearCustomization(self, datasetName=None, metadataType=None):
        """
        This method is used the remove an entire customization or clear out a specific metadata type.
        :param datasetName: (string) Used to identify the dataset to clear. If null, all dataset customizations will be cleared.
        :param metadataType: (string[]) If populated, identifies which metadata to clear(export, full, res_sum, shp)
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}dataset-clear-customization'
        json_payload = {"datasetName": datasetName,
                        "metadataType": metadataType}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetCoverage(self, datasetName):
        """
        Returns coverage for a given dataset.
        :param datasetName: (string) Determines which dataset to return coverage for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-coverage'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetDownloadOptions(self, datasetName, sceneFilter=None):
        """
        This request lists all available products for a given dataset - this does not guarantee scene availability.
        :param datasetName: (string) Used to identify the which dataset to return results for
        :param sceneFilter: (SceneFilter) Used to filter data within the dataset
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-download-options'
        json_payload = {"datasetName": datasetName,
                        "sceneFilter": sceneFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetFilters(self, datasetName):
        """
        This request is used to return the metadata filter fields for the specified dataset. These values can be used as additional criteria when submitting search and hit queries.
        :param datasetName: (string) Determines which dataset to return filters for
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}dataset-filters'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetGetCustomization(self, datasetName):
        """
        This method is used to retrieve metadata customization for a specific dataset.
        :param datasetName: (string) Used to identify the dataset to search
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}dataset-get-customization'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetGetCustomizations(self, datasetNames, metadataType):
        """
        This method is used to retrieve metadata customizations for multiple datasets at once.
        :param datasetNames: (string[]) Used to identify the dataset(s) to return. If null it will return all the users customizations
        :param metadataType: (string[]) If populated, identifies which metadata to return(export, full, res_sum, shp)
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}dataset-get-customizations'
        json_payload = {"datasetNames": datasetNames,
                        "metadataType": metadataType, }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetMessages(self, catalog=None, datasetName=None, datasetNames=None):
        """
        Returns any notices regarding the given datasets features.
        :param catalog: (string) Used to identify datasets that are associated with a given application
        :param datasetName: (string) Used as a filter with wildcards inserted at the beginning and the end of the supplied value
        :param datasetNames: (string[]) Used as a filter with wildcards inserted at the beginning and the end of the supplied value
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-messages'
        json_payload = {"catalog": catalog,
                        "datasetName": datasetName,
                        "datasetNames": datasetNames,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetMetadata(self, datasetName):
        """
        This method is used to retrieve all metadata fields for a given dataset.
        :param datasetName: (string) The system-friendly dataset name
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}dataset-metadata'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetOrderProducts(self, datasetName):
        """
        Lists all available order products for a dataset - this does not guarantee scene availability.
        :param datasetName: (string) Used to identify the which dataset to return results for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-order-products'
        json_payload = {"datasetName": datasetName}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetSearch(self, catalog=None, categoryId=None, datasetName=None, includeMessages=None, publicOnly=None,
                      includeUnknownSpatial=None, temporalFilter=None, spatialFilter=None, useCustomization=None):
        """
        This method is used to find datasets available for searching. By passing only API Key, all available datasets
        are returned. Additional parameters such as temporal range and spatial bounding box can be used to find
        datasets that provide more specific data. The dataset name parameter can be used to limit the results based on
        matching the supplied value against the public dataset name with assumed wildcards at the beginning and end.
        :param catalog: (string) Used to identify datasets that are associated with a given application
        :param categoryId (string) Used to restrict results to a specific category (does not search sub-sategories)
        :param datasetName: (string) Used as a filter with wildcards inserted at the beginning and the end of the supplied value
        :param includeMessages: (boolean) Optional parameter to include messages regarding specific dataset components
        :param publicOnly: (boolean) Used as a filter out datasets that are not accessible to unauthenticated general public users
        :param includeUnknownSpatial (boolean) Optional parameter to include datasets that do not support geographic searching
        :param temporalFilter: (TemporalFilter) Used to filter data based on data acquisition
        :param spatialFilter: (SpatialFilter) Used to filter data based on data location
        :param useCustomization (boolean) Optional parameter to indicate whether to use customization
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-search'
        json_payload = {"catalog": catalog,
                        "datasetName": datasetName,
                        "categoryId": categoryId,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "includeUnknownSpatial": includeUnknownSpatial,
                        "temporalFilter": temporalFilter,
                        "spatialFilter": spatialFilter,
                        "useCustomization": useCustomization,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetSetCustomization(self, datasetName, excluded=None, metadata=None, searchSort=None):
        """
        This method is used to find datasets available for searching. By passing only API Key, all available datasets are returned. Additional parameters such as temporal range and spatial bounding box can be used to find datasets that provide more specific data. The dataset name parameter can be used to limit the results based on matching the supplied value against the public dataset name with assumed wildcards at the beginning and end.
        :param datasetName: (string)  Used to identify the dataset to search
        :param excluded: (boolean) 	Used to exclude the dataset
        :param metadata: (Metadata)	Used to customize the metadata layout.
        :param searchSort: (SearchSort) Used to sort the dataset results.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-set-customization'
        json_payload = {"datasetName": datasetName,
                        "excluded": excluded,
                        "metadata": metadata,
                        "searchSort": searchSort,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def datasetSetCustomizations(self, datasetCustomization):
        """
        This method is used to find datasets available for searching. By passing only API Key, all available datasets
        are returned. Additional parameters such as temporal range and spatial bounding box can be used to find datasets
        that provide more specific data. The dataset name parameter can be used to limit the results based on matching
        the supplied value against the public dataset name with assumed wildcards at the beginning and end.
        :param datasetCustomization: (DatasetCustomization) Used to create or update a dataset customization for
        multiple datasets.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-set-customizations'
        json_payload = {"datasetCustomization": datasetCustomization,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadEula(self, eulaCode, eulaCodes):
        """
        Gets the contents of a EULA from the eulaCodes.
        :param eulaCode: (string) Used to specify a single eula
        :param eulaCodes: (string[]) Used to specify multiple eulas
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-eula'
        json_payload = {"eulaCode": eulaCode,
                        "eulaCodes": eulaCodes}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadLabels(self, downloadApplication):
        """
        Gets a list of unique download labels associated with the orders.
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-labels'
        json_payload = {"downloadApplication": downloadApplication}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadOptions(self, datasetName, entityIds=None, listId=None):
        """
        The download options request is used to discover downloadable products for each dataset. If a download is marked
        as not available, an order must be placed to generate that product.
        :param datasetName: (str) Dataset alias
        :param entityIds: (str) List of scenes
        :param listId: (str) Used to identify the list of scenes to use
        :return: (dict) Response as a dictionary
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
        This method is used to prepare a download order for processing by moving the scenes into the queue for processing
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param label: (string) Determines which order to load
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-order-load'
        json_payload = {"downloadApplication": downloadApplication,
                        "label": label,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadOrderRemove(self, label, downloadApplication=None):
        """
        This method is used to remove an order from the download queue.
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param label: (string) Determines which order to remove
        :return: (dict) Response as a dictionary
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
        Removes an item from the download queue.
        :param downloadId: (int) Represents the ID of the download from within the queue
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-remove'
        json_payload = {"downloadId": downloadId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadRequest(self, configurationCode=None, downloadApplication=None,
                        downloads=None, dataPaths=None, label=None, systemId=False):
        """
        This method is used to insert the requested downloads into the download queue and returns the available download URLs.
        :param configurationCode: (DownloadConfigurationCode) Used to customize the the download routine, primarily for testing
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param downloads: (Download[]) Used to identify higher level products that this data may be used to create
        :param dataPaths: (FilepathDownload[]) Used to identify products by data path, specifically for internal automation and DDS functionality
        :param label: (string) If this value is passed it will overide all individual download label values
        :param systemId: (string) Identifies the system submitting the download/order
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-request'
        json_payload = {"configurationCode": configurationCode,
                        "downloadApplication": downloadApplication,
                        "downloads": downloads,
                        "dataPaths": dataPaths,
                        "label": label,
                        "systemId": systemId
                        # "returnAvailable": returnAvailable,  # this may be undocumented parameter
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def downloadRetrieve(self, downloadApplication=None, label=None):
        """
        Returns all available and previously requests but not completed downloads.
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param label: (string) Determines which downloads to return
        :return: (dict) Response as a dictionary
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
        This method is used to searche for downloads within the queue, regardless of status, that match the given label.
        :param activeOnly: (boolean) Determines if completed, failed, cleared and proxied downloads are returned
        :param label: (string) Used to filter downloads by label
        :param downloadApplication: (string) Used to filter downloads by the intended downloading application
        :return: (dict) Response as a dictionary
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
        Gets a summary of all downloads, by dataset, for any matching labels.
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param label: (string) Determines which downloads to return
        :param sendEmail: (boolean) If set to true, a summary email will also be sent
        :return: (dict) Response as a dictionary
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
        Used to translate between known grids and coordinates.
        :param gridType: (string) Which grid system is being used? (WRS1 or WRS2)
        :param responseShape: (string) What type of geometry should be returned - a bounding box polygon or a center point? (polygon or point)
        :param path: (string) The x coordinate in the grid system
        :param row: (string) The y coordinate in the grid system
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}grid2ll'
        json_payload = {"gridType": gridType,
                        "responseShape": responseShape,
                        "path": path,
                        "row": row,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def login(self, username, password, userContext=None):
        """
        Upon a successful login, an API key will be returned. This key will be active for two hours and should be destroyed upon final use of the service by calling the logout method.
        This request requires an HTTP POST request instead of a HTTP GET request as a security measure to prevent username and password information from being logged by firewalls, web servers, etc.
        :param username: (string) ERS Username
        :param password: (string) ERS Password
        :param userContext: (UserContext) Metadata describing the user the request is on behalf of
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}login'
        json_payload = {"username": username,
                        "password": password,
                        "userContext": userContext,
                        }
        response = requests.post(url, json=json_payload)
        _check_response(response)
        self.apiKey = response.json()['data']
        if self.loud_mode:
            print(f'Login successful. API key: {self.apiKey}')
        return response.json()

    def logout(self):
        """
        This method is used to remove the users API key from being used in the future.
        No Parameters for Endpoint
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}logout'
        response = requests.post(url, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        if self.loud_mode:
            print(f'Logout successful. API key destroyed: {self.apiKey}')
        return response.json()

    def notifications(self, systemId):
        """
        Gets a notification list.
        :param systemId: (string) Determines the system you wish to return notifications for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}notifications'
        json_payload = {"systemId": systemId}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def orderProducts(self, datasetName, entityIds=None, listId=None):
        """
        Gets a list of currently selected products - paginated.
        :param datasetName: (string) Dataset alias
        :param entityIds: (string) List of scenes
        :param listId: (string) Used to identify the list of scenes to use
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}order-products'
        json_payload = {"datasetName": datasetName,
                        "entityIds": entityIds,
                        "listId": listId,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def orderSubmit(self, products, autoBulkOrder=None, processingParameters=None,
                    priority=None, orderComment=None, systemId=None):
        """
        Submits the current product list as a TRAM order - internally calling tram-order-create.
        :param autoBulkOrder: (boolean) If any products can be bulk ordered as a resulk of completed processing this option allows users to have orders automatically submitted.
        :param products: (Product[]) Used to identify higher level products that this data may be used to create
        :param processingParameters: () Optional processing parameters to send to the processing system
        :param priority: (int) Processing Priority
        :param orderComment: (string)  	Optional textual identifier for the order
        :param systemId: (string) Identifies the system submitting the order
        :return: (dict) Response as a dictionary
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
        Returns a list of user permissions for the authenticated user. This method does not accept any input.
        No Parameters for Endpoint
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}permissions'
        response = requests.post(url, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListAdd(self, listId, datasetName, idField=None, entityId=None, entityIds=None, timeToLive=None):
        """
        Adds items in the given scene list.
        :param listId: (string) User defined name for the list
        :param datasetName: (string) Dataset alias
        :param idField: (string) Used to determine which ID is being used - entityId (default) or displayId
        :param entityId: (string) Scene Indentifier
        :param entityIds: (string[]) A list of Scene Indentifiers
        :param timeToLive: (string) User defined lifetime using ISO-8601 formatted duration (such as "P1M") for the list
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}scene-list-add'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        "idField": idField,
                        "entityId": entityId,
                        "entityIds": entityIds,
                        "timeToLive": timeToLive,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListGet(self, listId, datasetName=None, startingNumber=None, maxResults=None):
        """
        Returns items in the given scene list.
        :param listId: (string) User defined name for the list
        :param datasetName: (string) Dataset alias
        :param startingNumber: (int) Used to identify the start number to search from
        :param maxResults: (int) How many results should be returned?
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-list-get'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        "startingNumber": startingNumber,
                        "maxResults": maxResults,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneListRemove(self, listId, datasetName, entityId=None, entityIds=None):
        """
        Removes items from the given list.
        :param listId: (string) User defined name for the list
        :param datasetName: (string) Dataset alias
        :param entityId: (string) Scene Indentifier
        :param entityIds: (string[]) A list of Scene Indentifiers
        :return: (dict) Response as a dictionary
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
        Returns summary information for a given list.
        :param listId: (string) User defined name for the list
        :param datasetName: (string) Dataset alias
        :return: (dict) Response as a dictionary
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
        Returns scene list types (exclude, search, order, bulk, etc).
        :param listFilter: (string) If provided, only returns listIds that have the provided filter value within the ID
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-list-types'
        json_payload = {"listFilter": listFilter}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadata(self, datasetName, entityId, metadataType=None, includeNullMetadataValues=None,
                      useCustomization=None):
        """
        This request is used to return metadata for a given scene.
        :param datasetName: (string) Used to identify the dataset to search
        :param entityId: (string) Used to identify the scene to return results for
        :param metadataType: (string) If populated, identifies which metadata to return (summary, full, fgdc, iso)
        :param includeNullMetadataValues: (boolean) Optional parameter to include null metadata values
        :param useCustomization: (boolean) Optional parameter to display metadata view as per user customization
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-metadata'
        json_payload = {"datasetName": datasetName,
                        "entityId": entityId,
                        "metadataType": metadataType,
                        "includeNullMetadataValues": includeNullMetadataValues,
                        "useCustomization": useCustomization,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadataList(self, listId, datasetName=None, metadataType=None, includeNullMetadataValues=None,
                          useCustomization=None):
        """
        Scene Metadata where the input is a pre-set list.
        :param datasetName: (string) Used to identify the dataset to search
        :param listId: (string) Used to identify the list of scenes to use
        :param metadataType: (string) If populated, identifies which metadata to return (summary or full)
        :param includeNullMetadataValues: (boolean) Optional parameter to include null metadata values
        :param useCustomization: (boolean) Optional parameter to display metadata view as per user customization
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-metadata-list'
        json_payload = {"datasetName": datasetName,
                        "listId": listId,
                        "metadataType": metadataType,
                        "includeNullMetadataValues": includeNullMetadataValues,
                        "useCustomization": useCustomization,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneMetadataXML(self, datasetName, entityId, metadataType=None):
        """
        Returns metadata formatted in XML, ahering to FGDC, ISO and EE scene metadata formatting standards.
        :param datasetName: (string) Used to identify the dataset to search
        :param entityId: (string) Used to identify the scene to return results for
        :param metadataType: (string) If populated, identifies which metadata to return (full, fgdc, iso)
        :return: (dict) Response as a dictionary
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
                    sortDirection=None, sortCustomization=None, useCustomization=None, sceneFilter=None,
                    compareListName=None, bulkListName=None, orderListName=None, excludeListName=None,
                    includeNullMetadataValues=None):
        """
        Searching is done with limited search criteria. All coordinates are assumed decimal-degree format. If lowerLeft
        or upperRight are supplied, then both must exist in the request to complete the bounding box. Starting and
        ending dates, if supplied, are used as a range to search data based on acquisition dates. The current
        implementation will only search at the date level, discarding any time information. If data in a given dataset
        is composite data, or data acquired over multiple days, a search will be done to match any intersection of the
        acquisition range. There currently is a 50,000 scene limit for the number of results that are returned, however,
        some client applications may encounter timeouts for large result sets for some datasets. To use the sceneFilter
        field, pass one of the four search filter objects (SearchFilterAnd, SearchFilterBetween, SearchFilterOr,
        SearchFilterValue) in JSON format with sceneFilter being the root element of the object.

        :param datasetName: (string) Used to identify the dataset to search
        :param maxResults: (int)  How many results should be returned ? (default = 100)
        :param startingNumber: (int) Used to identify the dataset to search
        :param metadataType: (string) If populated, identifies which metadata to return (summary or full)
        :param sortField: (string) Determines which field to sort the results on
        :param sortDirection: (string) Determines how the results should be sorted - ASC or DESC
        :param sortCustomization: (SortCustomization) Used to pass in custom sorts
        :param useCustomization: (boolean) Optional parameter to indicate whether to use customization
        :param sceneFilter: (SceneFilter) Used to filter data within the dataset
        :param compareListName: (string) If provided, defined a scene-list listId to use to track scenes selected for comparison
        :param bulkListName: (string) If provided, defined a scene-list listId to use to track scenes selected for bulk ordering
        :param orderListName: (string) If provided, defined a scene-list listId to use to track scenes selected for on-demand ordering
        :param excludeListName: (string) If provided, defined a scene-list listId to use to exclude scenes from the results
        :param includeNullMetadataValues: (boolean) Optional parameter to include null metadata values
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}scene-search'
        json_payload = {"datasetName": datasetName,
                        "maxResults": maxResults,
                        "startingNumber": startingNumber,
                        "metadataType": metadataType,
                        "sortField": sortField,
                        "sortDirection": sortDirection,
                        "sortCustomization": sortCustomization,
                        "useCustomization": useCustomization,
                        "sceneFilter": sceneFilter,
                        "compareListName": compareListName,
                        "bulkListName": bulkListName,
                        "orderListName": orderListName,
                        "excludeListName": excludeListName,
                        "includeNullMetadataValues": includeNullMetadataValues,
                        }
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def sceneSearchDelete(self, datasetName, maxResults=None, startingNumber=None, sortField=None, sortDirection=None,
                          temporalFilter=None):
        """
        This method is used to detect deleted scenes from datasets that support it. Supported datasets are determined by the 'supportDeletionSearch' parameter in the 'datasets' response. There currently is a 50,000 scene limit for the number of results that are returned, however, some client applications may encounter timeouts for large result sets for some datasets.
        :param datasetName: (string) Used to identify the dataset to search
        :param maxResults: (int) Used to identify the dataset to search
        :param startingNumber: (int) Used to identify the dataset to search
        :param sortField: (string) Determines which field to sort the results on
        :param sortDirection: (string) Determines how the results should be sorted - ASC or DESC
        :param temporalFilter: (TemporalFilter) Used to filter data based on data acquisition
        :return: (dict) Response as a dictionary
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
        This method is used to find the related scenes for a given scene.
        :param entityId: (string) Used to identify the scene to find related scenes for
        :param datasetName: (string) Used to identify the dataset to search
        :param maxResults: (int) Used to identify the dataset to search
        :param startingNumber: (int) Used to identify the dataset to search
        :param metadataType: (string) If populated, identifies which metadata to return (summary or full)
        :param sortField: (string) Determines which field to sort the results on
        :param sortDirection: (string) Determines how the results should be sorted - ASC or DESC
        :param compareListName: (string) If provided, defined a scene-list listId to use to track scenes selected for comparison
        :param bulkListName: (string) If provided, defined a scene-list listId to use to track scenes selected for bulk ordering
        :param orderListName: (string) If provided, defined a scene-list listId to use to track scenes selected for on-demand ordering
        :param excludeListName: (string) If provided, defined a scene-list listId to use to exclude scenes from the results
        :return: (dict) Response as a dictionary
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
        Search TRAM orders.
        :param orderId: (string) 	The order ID to get status for (accepts '%' wildcard)
        :param maxResults: (int) 	How many results should be returned on each page? (default = 25)
        :param systemId: (string) 	Limit results based on the application that order was submitted from
        :param sortAsc: (boolean) 	True for ascending results, false for descending results
        :param sortField: (string) 	Which field should sorting be done on? (order_id, date_entered or date_updated)
        :param statusFilter: (string[]) 	An array of status codes to
        :return: (dict) Response as a dictionary
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
        Gets the status of a TRAM order.
        :param orderNumber: (string) The order ID to get status for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-status'
        json_payload = {"orderNumber": orderNumber}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def tramOrderUnits(self, orderNumber):
        """
        Lists units for a specified order.
        :param orderNumber: (string) The order ID to get units for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-units'
        json_payload = {"orderNumber": orderNumber}
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()
