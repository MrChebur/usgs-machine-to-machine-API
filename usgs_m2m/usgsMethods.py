import requests
from warnings import warn
from .checkResponse import _check_response


# noinspection PyPep8Naming
class API:
    """
    Implementation date: 30.07.2020
    Revision date: 09.12.2024

    Official USGS/EROS Inventory Service Documentation (Machine-to-Machine API):
    https://m2m.cr.usgs.gov

    This API complies with the methods given in:
    https://m2m.cr.usgs.gov/api/docs/reference/
    """

    apiURL = r'https://m2m.cr.usgs.gov/api/api/json/stable/'  # must ends with slash: "/"
    apiKey = None
    loud_mode = False

    def __send_request_and_check_it(self, url: str, json_payload: dict) -> dict:
        """Protected function to send request, check it and return response. Used in almost every method in this API.
        :param url: request URL
        :param json_payload: `requests` json payload.
        :return: response as dictionary
        """
        response = requests.post(url, json=json_payload, headers={'X-Auth-Token': self.apiKey})
        _check_response(response)
        return response.json()

    def dataOwner(self, dataOwner):
        """
        This method is used to provide the contact information of the data owner.
        :param dataOwner: (string) Used to identify the data owner - this value comes from the dataset-search response
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}data-owner'
        json_payload = {"dataOwner": dataOwner}
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def datasetBrowse(self, datasetId):
        """
        This request is used to return the browse configurations for the specified dataset.
        :param datasetId: (string) Determines which dataset to return browse configurations for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-browse'
        json_payload = {"datasetId": datasetId}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetBulkProducts(self, datasetName):
        """
        Lists all available bulk products for a dataset - this does not guarantee scene availability.
        :param datasetName: (str)  	Used to identify the which dataset to return results for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-bulk-products'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetCatalogs(self):
        """
        This method is used to retrieve the available dataset catalogs. The use of dataset catalogs are not required,
        but are used to group datasets by their use within our web applications.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-catalogs'
        json_payload = {}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetCategories(self, catalog, includeMessages=False, publicOnly=False, useCustomization=False, parentId=None,
                          datasetFilter=None):
        """
        This method is used to search datasets under the categories.
        :param catalog: (string) Used to identify datasets that are associated with a given application
        :param includeMessages: (boolean) Optional parameter to include messages regarding specific dataset components
        :param publicOnly: (boolean) Used as a filter out datasets that are not accessible to unauthenticated general
               public users
        :param useCustomization: (boolean) Used as a filter out datasets that are excluded by user customization
        :param parentId: (string) If provided, returned categories are limited to categories that are children of the
               provided ID
        :param datasetFilter: (string) If provided, filters the datasets - this automatically adds a wildcard before and
               after the input value
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-categories'
        json_payload = {"catalog": catalog,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "useCustomization": useCustomization,
                        "parentId": parentId,
                        "datasetFilter": datasetFilter}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetClearCustomization(self, datasetName=None, metadataType=None, fileGroupIds=None):
        """
        This method is used the remove an entire customization or clear out a specific metadata type.
        :param datasetName: (string) Used to identify the dataset to clear. If null, all dataset customizations will be cleared.
        :param metadataType: (string[]) If populated, identifies which metadata to clear(export, full, res_sum, shp)
        :param fileGroupIds: (string[]) If populated, identifies which file group to clear
        :return: (dict) Response as a dictionary
        """
        if fileGroupIds is None:
            fileGroupIds = []
        if metadataType is None:
            metadataType = []
        url = f'{self.apiURL}dataset-clear-customization'
        json_payload = {"datasetName": datasetName,
                        "metadataType": metadataType,
                        "fileGroupIds": fileGroupIds,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def datasetCoverage(self, datasetName):
        """
        Returns coverage for a given dataset.
        :param datasetName: (string) Determines which dataset to return coverage for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-coverage'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def datasetFileGroups(self, datasetName):
        """
        This method is used to list all configured file groups for a dataset.
        :param datasetName: (string) Dataset alias
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-file-groups'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetFilters(self, datasetName):
        """
        This request is used to return the metadata filter fields for the specified dataset. These values can be used
        as additional criteria when submitting search and hit queries.
        :param datasetName: (string) Determines which dataset to return filters for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-filters'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetGetCustomization(self, datasetName):
        """
        This method is used to retrieve metadata customization for a specific dataset.
        as additional criteria when submitting search and hit queries.
        :param datasetName: (string) Used to identify the dataset to search
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-get-customization'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetGetCustomizations(self, datasetNames=None, metadataType=None):
        """
        This method is used to retrieve metadata customizations for multiple datasets at once.
        :param datasetNames: (string[]) Used to identify the dataset(s) to return. If null it will return all the users
        customizations
        :param metadataType: (string[]) If populated, identifies which metadata to return(export, full, res_sum, shp)
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-get-customizations'
        json_payload = {"datasetName": datasetNames,
                        "metadataType": metadataType,
                        }
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def datasetMetadata(self, datasetName):
        """
        This method is used to retrieve all metadata fields for a given dataset.
        :param datasetName: (string) The system-friendly dataset name
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-metadata'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetOrderProducts(self, datasetName):
        """
        Lists all available order products for a dataset - this does not guarantee scene availability.
        :param datasetName: (string) Used to identify the which dataset to return results for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-order-products'
        json_payload = {"datasetName": datasetName}
        return self.__send_request_and_check_it(url, json_payload)

    def datasetSearch(self, catalog=None, categoryId=None, datasetName=None, includeMessages=None, publicOnly=None,
                      includeUnknownSpatial=None, temporalFilter=None, spatialFilter=None, sortDirection=None,
                      sortField=None, useCustomization=None):
        """
        This method is used to find datasets available for searching. By passing only API Key, all available datasets
        are returned. Additional parameters such as temporal range and spatial bounding box can be used to find datasets
        that provide more specific data. The dataset name parameter can be used to limit the results based on matching
        the supplied value against the public dataset name with assumed wildcards at the beginning and end.
        :param catalog: (string) Used to identify datasets that are associated with a given application
        :param categoryId: (string) Used to restrict results to a specific category (does not search sub-sategories)
        :param datasetName: (string) Used as a filter with wildcards inserted at the beginning and the end of the supplied value
        :param includeMessages: (boolean) Optional parameter to include messages regarding specific dataset components
        :param publicOnly: (boolean) Used as a filter out datasets that are not accessible to unauthenticated general public users
        :param includeUnknownSpatial: (string) Optional parameter to include datasets that do not support geographic searching
        :param temporalFilter: (TemporalFilter) Used to filter data based on data acquisition
        :param spatialFilter: (SpatialFilter) Used to filter data based on data location
        :param sortDirection: (string) Defined the sorting as Ascending (ASC) or Descending (DESC) - default is ASC
        :param sortField: (string) Identifies which field should be used to sort datasets (shortName - default, longName, dastasetName, GloVis)
        :param useCustomization: (string) Optional parameter to indicate whether to use customization

        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-search'
        json_payload = {"catalog": catalog,
                        "categoryId": categoryId,
                        "datasetName": datasetName,
                        "includeMessages": includeMessages,
                        "publicOnly": publicOnly,
                        "includeUnknownSpatial": includeUnknownSpatial,
                        "temporalFilter": temporalFilter,
                        "spatialFilter": spatialFilter,
                        "sortDirection": sortDirection,
                        "sortField": sortField,
                        "useCustomization": useCustomization,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def datasetSetCustomization(self, datasetName, excluded=None, metadata=None, searchSort=None, fileGroups=None):
        """
        This method is used to create or update dataset customizations for a given dataset.
        :param datasetName: (string) Used to identify the dataset to search
        :param excluded: (boolean) Used to exclude the dataset
        :param metadata: (Metadata) Used to customize the metadata layout.
        :param searchSort: (SearchSort) Used to sort the dataset results.
        :param fileGroups: (FileGroups) Used to customize downloads by file groups
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-set-customization'
        json_payload = {"datasetName": datasetName,
                        "excluded": excluded,
                        "metadata": metadata,
                        "searchSort": searchSort,
                        "fileGroups": fileGroups,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def datasetSetCustomizations(self, datasetCustomization):
        """
        This method is used to create or update dataset customizations for a given dataset.
        :param datasetCustomization: (DatasetCustomization) Used to create or update a dataset customization for
        multiple datasets.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}dataset-set-customizations'
        json_payload = {"datasetCustomization": datasetCustomization}
        return self.__send_request_and_check_it(url, json_payload)

    def downloadCompleteProxied(self, proxiedDownloads):
        """
        Updates status to 'C' with total downloaded file size for completed proxied downloads
        :param proxiedDownloads: (ProxiedDownload[]) Used to specify multiple proxied downloads
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-complete-proxied'
        json_payload = {"proxiedDownloads": proxiedDownloads}
        return self.__send_request_and_check_it(url, json_payload)

    def downloadEula(self, eulaCode=None, eulaCodes=None):
        """
        Gets the contents of a EULA from the eulaCodes.
        :param eulaCode: (string) Used to specify a single eula
        :param eulaCodes: (string[]) Used to specify multiple eulas
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-eula'
        json_payload = {"eulaCode": eulaCode,
                        "eulaCodes": eulaCodes,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def downloadLabels(self, downloadApplication=None):
        """
        Gets a list of unique download labels associated with the orders.
        :param downloadApplication: (string) Used to denote the application that will perform the download
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-labels'
        json_payload = {"downloadApplication": downloadApplication}
        return self.__send_request_and_check_it(url, json_payload)

    def downloadOptions(self, datasetName, entityIds=None, listId=None, includeSecondaryFileGroups=None):
        """
        The download options request is used to discover downloadable products for each dataset. If a download is marked
        as not available, an order must be placed to generate that product.
        :param datasetName: (str) Dataset alias
        :param entityIds: (str) List of scenes
        :param listId: (str) Used to identify the list of scenes to use
        :param includeSecondaryFileGroups: (boolean) Optional parameter to return file group IDs with secondary products
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-options'
        json_payload = {"datasetName": datasetName,
                        "entityIds": entityIds,
                        "listId": listId,
                        "includeSecondaryFileGroups": includeSecondaryFileGroups,
                        }
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def downloadRemove(self, downloadId):
        """
        Removes an item from the download queue.
        :param downloadId: (int) Represents the ID of the download from within the queue
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-remove'
        json_payload = {"downloadId": downloadId,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def downloadRequest(self, configurationCode=None, downloadApplication=None, downloads=None, dataPaths=None,
                        label=None, systemId=None, dataGroups=None, returnAvailable=False):
        """
        This method is used to insert the requested downloads into the download queue and returns the available download
        URLs.
        Each ID supplied in the downloads parameter you provide will be returned in one of three elements:
            availableDownloads - URLs provided in this list are immediately available; note that these URLs take you to
                                 other distribution systems that may require authentication
            preparingDownloads - IDs have been accepted but the URLs are NOT YET available for use
            failed - IDs were rejected; see the errorMessage field for an explanation

        Other information is also provided in the response:
            newRecords - Includes a downloadId for each element of the downloads parameter that was accepted and a label
                         that applies to the whole request
            duplicateProducts - Requests that duplicate previous requests by the same user; these are not re-added to
                                the queue and are not included in newRecords
            numInvalidScenes - The number of products that could not be found by ID or failed to be requested for any
                               reason
            remainingLimits - The number of remaining downloads to hit the rate limits by user and IP address
                limitType - The type of the limits are counted by, the value is either 'user' or 'ip'
                username - The user name associated with the request
                ipAddress - The IP address associated with the request
                recentDownloadCount - The number of downloads requested in the past 15 minutes
                pendingDownloadCount - The number of downloads in pending state before they are available for download
                unattemptedDownloadCount - The number of downloads in available status but the user has not downloaded
                                           yet

This API may be online while the distribution systems are unavailable. When this occurs, you will recieve the following
error when requesting products that belong to any of these systems: 'This download has been temporarily disabled.
Please try again at a later time. We apologize for the inconvenience.'. Once the distribution system is back online,
this error will stop occuring and download requests will succeed.

        :param configurationCode: (string) Used to customize the the download routine, primarily for testing.
        The valid values include no_data, test, order, order+email and null
        :param downloadApplication: (string) Used to denote the application that will perform the download
        (default = M2M). Internal use only.
        :param downloads: (DownloadInput[]) Used to identify higher level products that this data may be used to create
        :param dataPaths: (FilepathDownload[]) Used to identify products by data path, specifically for internal
        automation and DDS functionality
        :param label: (string) If this value is passed it will overide all individual download label values
        :param systemId: (string) Identifies the system submitting the download/order (default = M2M). Internal use only
        :param dataGroups: (FilegroupDownload[]) Identifies the products by file groups
        :param returnAvailable: THIS MAY BE UNDOCUMENTED PARAMETER
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-request'
        json_payload = {"configurationCode": configurationCode,
                        "downloadApplication": downloadApplication,
                        "downloads": downloads,
                        "dataPaths": dataPaths,
                        "label": label,
                        "systemId": systemId,
                        "dataGroups": dataGroups,
                        "returnAvailable": returnAvailable,  # this may be undocumented parameter
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def downloadRetrieve(self, downloadApplication=None, label=None):
        """
        Returns all available and previously requests but not completed downloads.

This API may be online while the distribution systems are unavailable. When this occurs, the downloads being fulfilled
by those systems will not appear as available nor are they counted in the 'queueSize' response field.

        :param downloadApplication: (string) Used to denote the application that will perform the download
        :param label: (string) Determines which downloads to return
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}download-retrieve'
        json_payload = {"label": label,
                        "downloadApplication": downloadApplication,
                        }
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def login(self, username, password, userContext=None):
        """
        Upon a successful login, an API key will be returned. This key will be active for two hours and should be
        destroyed upon final use of the service by calling the logout method. This request requires an HTTP POST
        request instead of a HTTP GET request as a security measure to prevent username and password information
        from being logged by firewalls, web servers, etc.
        :param username: (string) ERS Username
        :param password: (string) ERS Password
        :param userContext: (UserContext) Metadata describing the user the request is on behalf of
        :return: (dict) Response as a dictionary
        """
        warn("The `login` endpoint will be deprecated in February 2025. To continue using the API, use the "
             "`login-token` endpoint for authentication; additional details can be found here: "
             "https://www.usgs.gov/media/files/m2m-application-token-documentation",
             DeprecationWarning, stacklevel=2)

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

    def loginAppGuest(self, applicationToken, userToken):
        """
        This endpoint assumes that the calling application has generated a single-use token to complete the
        authentication and return an API Key specific to that guest user. All subsequent requests should use the API
        Key under the 'X-Auth-Token' HTTP header as the Single Sign-On cookie will not authenticate those requests.
        The API Key will be active for two hours, which is restarted after each subsequent request, and should be
        destroyed upon final use of the service by calling the logout method.

        The 'appToken' field will be used to verify the 'Referrer' HTTP Header to ensure the request was authentically
        sent from the assumed application.
        :param applicationToken: (string) The token for the calling application
        :param userToken: (string) The single-use token generated for this user
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}login-app-guest'
        json_payload = {"applicationToken": applicationToken,
                        "userToken": userToken,
                        }
        response = requests.post(url, json=json_payload)
        _check_response(response)
        self.apiKey = response.json()['data']
        if self.loud_mode:
            print(f'Login successful. API key: {self.apiKey}')
        return response.json()

    def loginSSO(self, userContext):
        """
        This endpoint assumes that a user has an active ERS Single Sign-On Cookie in their browser or attached to this
        request. Authentication will be performed from the Single Sign-On Cookie and return an API Key upon successful
        authentication. All subsequent requests should use the API Key under the 'X-Auth-Token' HTTP header as the
        Single Sign-On cookie will not authenticate those requests. The API Key will be active for two hours, which is
        restarted after each subsequent request, and should be destroyed upon final use of the service by calling the
        logout method.
        :param userContext: (UserContext) Metadata describing the user the request is on behalf of
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}login-sso'
        json_payload = {"userContext": userContext}
        response = requests.post(url, json=json_payload)
        _check_response(response)
        self.apiKey = response.json()['data']
        if self.loud_mode:
            print(f'Login successful. API key: {self.apiKey}')
        return response.json()

    def loginToken(self, username, token):
        """
        This login method uses ERS application tokens to allow for authentication that is not directly tied the users
        ERS password. Instructions for generating the application token can be found here:
        https://www.usgs.gov/media/files/m2m-application-token-documentation
        Upon a successful login, an API key will be returned. This key will be active for two hours and should be
        destroyed upon final use of the service by calling the logout method.

        This request requires an HTTP POST request instead of a HTTP GET request as a security measure to prevent
        username and password information from being logged by firewalls, web servers, etc.
        :param username: (string) ERS Username
        :param token: (string) Application Token
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}login-token'
        json_payload = {"username": username,
                        "token": token,
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
        Gets a notification list. Note: Few valid systems ids are BDA, DDS, EE, ERS, GVN, HDDS, M2M, etc.
        :param systemId: (string) Determines the system you wish to return notifications for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}notifications'
        json_payload = {"systemId": systemId}
        return self.__send_request_and_check_it(url, json_payload)

    def orderProducts(self, datasetName, entityIds=None, listId=None):
        """
        Gets a list of currently selected products - paginated.
        Note: "listId" is the id of the customized list which is built by scene-list-add:
                https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-add
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
        return self.__send_request_and_check_it(url, json_payload)

    def orderSubmit(self, products, autoBulkOrder=None, processingParameters=None, priority=None,
                    orderComment=None, systemId=None):
        """
        Submits the current product list as a TRAM order - internally calling tram-order-create.
        :param products: (Product[]) Used to identify higher level products that this data may be used to create
        :param autoBulkOrder: (boolean) If any products can be bulk ordered as a resulk of completed processing this
                                        option allows users to have orders automatically submitted.
        :param processingParameters: (string) 	Optional processing parameters to send to the processing system
        :param priority: (int) Processing Priority
        :param orderComment: (string) Optional textual identifier for the order
        :param systemId: (string) Identifies the system submitting the order
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}order-submit'
        json_payload = {"products": products,
                        "autoBulkOrder": autoBulkOrder,
                        "processingParameters": processingParameters,
                        "priority": priority,
                        "orderComment": orderComment,
                        "systemId": systemId,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def permissions(self):
        """
        Returns a list of user permissions for the authenticated user. This method does not accept any input.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}permissions'
        json_payload = {}
        return self.__send_request_and_check_it(url, json_payload)

    # Perhaps the feature description is not yet complete? https://m2m.cr.usgs.gov/api/docs/reference/#placename
    def placename(self, featureType=None, name=None):
        """
        (Description Unavailable)
        :param featureType: (string) Type or feature - either US or world
        :param name: (string) Name of the feature
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}placename'
        json_payload = {"featureType": featureType,
                        "name": name,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def rateLimitSummary(self, ipAddress=None):
        """
        Returns download rate limits and how many downloads are in each status as well as how close the user is to
        reaching the rate limits

Three elements are provided in the response:

    initialLimits - Includes the initial downloads rate limits
        recentDownloadCount - The maximum number of downloads requested in the past 15 minutes
        pendingDownloadCount - The maximum number of downloads in pending state before they are available for download
        unattemptedDownloadCount - The maximum number of downloads in available status but the user has not downloaded yet
    remainingLimits - - Includes downloads that are currently remaining and count towards the rate limits. Users should
    be watching out for any of those numbers approaching 0 which means it is close to hitting the rate limits
        limitType - The type of the limits are counted by, the value is either 'user' or 'ip'
        username - The user name associated with the request
        ipAddress - The IP address associated with the request
        recentDownloadCount - The number of downloads requested in the past 15 minutes
        pendingDownloadCount - The number of downloads in pending state before they are available for download
        unattemptedDownloadCount - The number of downloads in available status but the user has not downloaded yet
    recentDownloadCounts - Includes the downloads count in each status for the past 15 minutes
        countType - The type of the download counts are calculated by, the value is either 'user' or 'ip'
        username - The user name associated with the request
        ipAddress - The IP address associated with the request
        downloadCount - The number of downloads per status in the past 15 minutes

This API may be online while the distribution systems are unavailable. When this occurs, you will recieve the following
error when requesting products that belong to any of these systems: 'This download has been temporarily disabled.
Please try again at a later time. We apologize for the inconvenience.'. Once the distribution system is back online,
this error will stop occuring and download requests will succeed.
        :param ipAddress: (string[])  	Used to specify multiple IP address
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}rate-limit-summary'
        json_payload = {"ipAddress": ipAddress}
        return self.__send_request_and_check_it(url, json_payload)

    def sceneListAdd(self, listId, datasetName, idField=None, entityId=None, entityIds=None, timeToLive=None,
                     checkDownloadRestriction=None):
        """
        Adds items in the given scene list.
        :param listId: (string) User defined name for the list
        :param datasetName: (string) Dataset alias
        :param idField: (string) Used to determine which ID is being used - entityId (default) or displayId
        :param entityId: (string) Scene Indentifier
        :param entityIds: (string[]) A list of Scene Indentifiers
        :param timeToLive: (string) User defined lifetime using ISO-8601 formatted duration (such as "P1M") for the list
        :param checkDownloadRestriction: (boolean) Optional parameter to check download restricted access and availability
        :return: (dict) Response as a dictionary
        """

        url = f'{self.apiURL}scene-list-add'
        json_payload = {"listId": listId,
                        "datasetName": datasetName,
                        "idField": idField,
                        "entityId": entityId,
                        "entityIds": entityIds,
                        "timeToLive": timeToLive,
                        "checkDownloadRestriction": checkDownloadRestriction,
                        }
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def sceneListRemove(self, listId, datasetName=None, entityId=None, entityIds=None):
        """
        Removes items from the given list. If no datasetName is provided, the call removes the whole list. If a
        datasetName is provided but no entityId, this call removes that dataset with all its IDs. If a datasetName and
        entityId(s) are provided, the call removes the ID(s) from the dataset.
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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def sceneListTypes(self, listFilter=None):
        """
        Returns scene list types (exclude, search, order, bulk, etc).
        :param listFilter: (string) If provided, only returns listIds that have the provided filter value within the ID
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-list-types'
        json_payload = {"listFilter": listFilter}
        return self.__send_request_and_check_it(url, json_payload)

    def sceneMetadata(self, datasetName, entityId, idType=None, metadataType=None, includeNullMetadataValues=None,
                      useCustomization=None):
        """
        This request is used to return metadata for a given scene.
        :param datasetName: (string) Used to identify the dataset to search
        :param entityId: (string) Used to identify the scene to return results for
        :param idType: (string) If populated, identifies which ID field (entityId, displayId or orderingId) to use when
                                searching for the provided entityId (default = entityId)
        :param metadataType: (string) If populated, identifies which metadata to return (summary, full, fgdc, iso)
        :param includeNullMetadataValues: (boolean) Optional parameter to include null metadata values
        :param useCustomization: (boolean) Optional parameter to display metadata view as per user customization
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}scene-metadata'
        json_payload = {"datasetName": datasetName,
                        "entityId": entityId,
                        "idType": idType,
                        "metadataType": metadataType,
                        "includeNullMetadataValues": includeNullMetadataValues,
                        "useCustomization": useCustomization,
                        }
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

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

        The response of this request includes a 'totalHits' response parameter that indicates the total number of scenes
        that match the search query to allow for pagination. Due to this, searches without a 'sceneFilter' parameter can
        take much longer to execute. To minimize this impact we use a cached scene count for 'totalHits' instead of
        computing the actual row count. An additional field, 'totalHitsAccuracy', is also included in the response to
        indicate if the 'totalHits' value was computed based off the query or using an approximated value. This does not
        impact the users ability to access these results via pagination. This cached value is updated daily for all
        datasets with active data ingests. Ingest frequency for each dataset can be found using the 'ingestFrequency'
        field in the dataset, dataset-categories and dataset-search endpoint responses.
        :param datasetName: (string) Used to identify the dataset to search
        :param maxResults: (int) Used to identify the dataset to search
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
        return self.__send_request_and_check_it(url, json_payload)

    def sceneSearchDelete(self, datasetName, maxResults=None, startingNumber=None, sortField=None, sortDirection=None,
                          temporalFilter=None):
        """
        This method is used to detect deleted scenes from datasets that support it. Supported datasets are determined by
        the 'supportDeletionSearch' parameter in the 'datasets' response. There currently is a 50,000 scene limit for
        the number of results that are returned, however, some client applications may encounter timeouts for large
        result sets for some datasets.
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
        return self.__send_request_and_check_it(url, json_payload)

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
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderDetailUpdate(self, orderNumber, detailKey, detailValue):
        """
        This method is used to set metadata for an order.
        :param orderNumber: (string) The order ID for the order to update
        :param detailKey: (string) The system detail key
        :param detailValue: (string) The value to store under the detailKey
         :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-detail-update'
        json_payload = {"orderNumber": orderNumber,
                        "detailKey": detailKey,
                        "detailValue": detailValue,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderDetails(self, orderNumber):
        """
        This method is used to set metadata for an order.
        :param orderNumber: (string) The order ID to get details for
         :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-details'
        json_payload = {"orderNumber": orderNumber}
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderDetailsClear(self, orderNumber):
        """
        This method is used to clear all metadata within an order.
        :param orderNumber: (string) The order ID to clear details for
         :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-details-clear'
        json_payload = {"orderNumber": orderNumber}
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderDetailsRemove(self, orderNumber, detailKey):
        """
        This method is used to clear all metadata within an order.
        :param orderNumber: (string) The order ID to clear details for
        :param detailKey: (string) The system detail key
         :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-details-remove'
        json_payload = {"orderNumber": orderNumber,
                        "detailKey": detailKey,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderSearch(self, orderId=None, maxResults=None, systemId=None, sortAsc=None, sortField=None,
                        statusFilter=None):
        """
        Search TRAM orders.
        :param orderId: (string) The order ID to get status for (accepts '%' wildcard)
        :param maxResults: (int) How many results should be returned on each page? (default = 25)
        :param systemId: (string) Limit results based on the application that order was submitted from
        :param sortAsc: (boolean) True for ascending results, false for descending results
        :param sortField: (string) Which field should sorting be done on? (order_id, date_entered or date_updated)
        :param statusFilter: (string[]) An array of status codes to
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
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderStatus(self, orderNumber):
        """
        Gets the status of a TRAM order.
        :param orderNumber: (string) The order ID to get status for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-status'
        json_payload = {"orderNumber": orderNumber}
        return self.__send_request_and_check_it(url, json_payload)

    def tramOrderUnits(self, orderNumber):
        """
        Lists units for a specified order.
        :param orderNumber: (string) The order ID to get units for
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}tram-order-units'
        json_payload = {"orderNumber": orderNumber}
        return self.__send_request_and_check_it(url, json_payload)

    def userPreferenceGet(self, systemId=None, setting=None):
        """
        This method is used to retrieve user's preference settings.
        :param systemId: (string) Used to identify which system to return preferences for. If null it will return all
                                     the users preferences
        :param setting: (string[]) If populated, identifies which setting(s) to return
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}user-preference-get'
        json_payload = {"systemId": systemId,
                        "setting": setting,
                        }
        return self.__send_request_and_check_it(url, json_payload)

    def userPreferenceSet(self, systemId, userPreferences):
        """
        This method is used to create or update user's preferences.
        :param systemId: (string) Used to identify which system the preferences are for.
        :param userPreferences: (string[]) Used to set user preferences for various systems.
        :return: (dict) Response as a dictionary
        """
        url = f'{self.apiURL}user-preference-set'
        json_payload = {"systemId": systemId,
                        "userPreferences": userPreferences,
                        }
        return self.__send_request_and_check_it(url, json_payload)
