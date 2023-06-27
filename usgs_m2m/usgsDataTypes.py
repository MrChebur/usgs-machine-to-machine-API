class usgsDataTypes:
    """
    Implementation date: 11.03.2021

    These data types are just wrappers that return dictionaries.
    No special operators are implemented (like "+", ">=", "<" and etc.).

    According to document:
    https://m2m.cr.usgs.gov/api/docs/datatypes/
    """

    @classmethod
    def AcquisitionFilter(cls, start, end):
        """
        :param start: (string) The date the scene began acquisition - ISO 8601 Formatted Date
        :param end: (string) The date the scene ended acquisition - ISO 8601 Formatted Date
        """
        return {'start': start, 'end': end}

    @classmethod
    def CloudCoverFilter(cls, min, max, includeUnknown):
        """
        :param min: (int) Used to limit results by minimum cloud cover (for supported datasets)
        :param max: (int) Used to limit results by maximum cloud cover (for supported datasets)
        :param includeUnknown: (boolean) Used to determine if scenes with unknown cloud cover values should be included in the results
        """
        return {'min': min, 'max': max, 'includeUnknown': includeUnknown}

    @classmethod
    def Coordinate(cls, latitude, longitude):
        """
        :param latitude: (double) Decimal degree coordinate in EPSG:4326 projection
        :param longitude: (double) Decimal degree coordinate in EPSG:4326 projection
        """
        return {'latitude': latitude, 'longitude': longitude}

    @classmethod
    def DateRange(cls, startDate, endDate):
        """
        :param startDate: (string) Used to apply a temporal filter on the data - ISO 8601 Formatted Date
        :param endDate: (string) Used to apply a temporal filter on the data - ISO 8601 Formatted Date
        """
        return {'startDate': startDate, 'endDate': endDate}

    @classmethod
    def GeoJson(cls, type, coordinates):
        """
        :param type: (string) Geometry types supported by GeoJson, like polygon
        :param coordinates: (coordinate[]) Coordinate array
        """
        return {'type': type, 'coordinates': coordinates}

    @classmethod
    def IngestFilter(cls, start, end):
        """
        :param start: (string) The date the scene began ingestion - ISO 8601 Formatted Date
        :param end: (string) The date the scene ended ingestion - ISO 8601 Formatted Date
        """
        return {'start': start, 'end': end}

    @classmethod
    def MetadataFilter(cls, **kwargs):
        """
        This is an abstract data model, use MetadataAnd, MetadataBetween, MetadataOr, or MetadataValue
        """
        if 'filterType' not in kwargs:
            raise ValueError(f'filterType parameter is required')

        if kwargs['filterType'] == "and":
            return cls.MetadataAnd(**kwargs)

        elif kwargs['filterType'] == "between":
            return cls.MetadataBetween(**kwargs)

        elif kwargs['filterType'] == "or":
            return cls.MetadataOr(**kwargs)

        elif kwargs['filterType'] == "value":
            return cls.MetadataValue(**kwargs)

        else:
            raise ValueError(
                f'Invalid filterType value: {kwargs["filterType"]}. Check for SpatialFilterMbr or SpatialFilterGeoJson data types')

    @classmethod
    def MetadataAnd(cls, childFilters, filterType='and'):
        """
        :param filterType: (string) Value must be "and"
        :param childFilters: (string) Joins any filter parameters together with the "and" logical operator
        """
        return {'filterType': filterType, 'childFilters': childFilters}

    @classmethod
    def MetadataBetween(cls, filterId, firstValue, secondValue, filterType='between'):
        """
        :param filterType (string) Value must be "between"
        :param filterId (string) Unique Identifier for the dataset criteria field and it can be retrieved by dataset-filters
        :param firstValue (int) First value in between clause
        :param secondValue (int) Second value in between clause
        """
        return {'filterType': filterType, 'filterId': filterId, 'firstValue': firstValue, 'secondValue': secondValue}

    @classmethod
    def MetadataOr(cls, childFilters, filterType='or'):
        """
        :param filterType (string) Value must be "or"
        :param childFilters: (string) Joins any filter parameters together with the "or" logical operator
        """
        return {'filterType': filterType, 'childFilters': childFilters}

    @classmethod
    def MetadataValue(cls, filterId, value, operand, filterType='value'):
        """
        :param filterType (string) Value must be "value"
        :param filterId (string) Unique Identifier for the dataset criteria field and it can be retrieved by dataset-filters
        :param value (string) Value to use
        :param operand (string) Determines what operand to search with - accepted values are "=" and "like"
        """
        return {'filterType': filterType, 'filterId': filterId, 'value': value, 'operand': operand}

    @classmethod
    def SceneFilter(cls, acquisitionFilter, cloudCoverFilter, datasetName, ingestFilter, metadataFilter,
                    seasonalFilter, spatialFilter):
        """
        :param acquisitionFilter: (acquisitionFilter) Used to apply a acquisition filter on the data
        :param cloudCoverFilter: (cloudCoverFilter) Used to apply a cloud cover filter on the data
        :param datasetName: (string) Dataset name
        :param ingestFilter: (ingestFilter) Used to apply an ingest filter on the data
        :param metadataFilter: (metadataFilter) Used to apply a metadata filter on the data
        :param seasonalFilter: (int[]) Used to apply month numbers from 1 to 12 on the data
        :param spatialFilter: (spatialFilter) Used to apply a spatial filter on the data
        """
        return {'acquisitionFilter': acquisitionFilter, 'cloudCoverFilter': cloudCoverFilter,
                'datasetName': datasetName, 'ingestFilter': ingestFilter, 'metadataFilter': metadataFilter,
                'seasonalFilter': seasonalFilter, 'spatialFilter': spatialFilter}

    @classmethod
    def SpatialBounds(cls, **kwargs):
        """
        This is an abstract data model, use spatialBoundsMbr or geoJson
        """
        if 'north' in kwargs:
            return cls.spatialBoundsMbr(**kwargs)
        elif 'type' in kwargs:
            return cls.geoJson(**kwargs)
        raise ValueError(f"'north' or 'type' parameter is required. Check for spatialBoundsMbr or geoJson data types")

    @classmethod
    def SpatialBoundsMbr(cls, north, east, south, west):
        """
        :param north: (string) Decimal degree coordinate value in EPSG:4326 projection representing the northern most point of the MBR
        :param east: (string) Decimal degree coordinate value in EPSG:4326 projection representing the eastern most point of the MBR
        :param south: (string) Decimal degree coordinate value in EPSG:4326 projection representing the southern most point of the MBR
        :param west: (string) Decimal degree coordinate value in EPSG:4326 projection representing the western most point of the MBR
        """
        return {'north': north, 'east': east, 'south': south, 'west': west}

    @classmethod
    def SpatialFilter(cls, **kwargs):
        """
        This is an abstract data model, use SpatialFilterMbr or SpatialFilterGeoJson
        """
        if 'filterType' not in kwargs:
            raise ValueError(f'filterType parameter is required')

        if kwargs['filterType'] == "mbr":
            return cls.SpatialFilterMbr(**kwargs)
        elif kwargs['filterType'] == "geojson":
            return cls.SpatialFilterGeoJson(**kwargs)
        else:
            raise ValueError(
                f'Invalid filterType value: {kwargs["filterType"]}. Check for SpatialFilterMbr or SpatialFilterGeoJson data types')

    @classmethod
    def SpatialFilterMbr(cls, lowerLeft, upperRight, filterType="mbr"):
        """
        :param filterType: (string) value must be "mbr"
        :param lowerLeft: (coordinate) The southwest point of the minimum bounding rectangle
        :param upperRight: (coordinate) The northeast point of the minimum bounding rectangle
        """
        return {'filterType': filterType, 'lowerLeft': lowerLeft, 'upperRight': upperRight}

    @classmethod
    def SpatialFilterGeoJson(cls, geoJson, filterType="geojson"):
        """
        :param filterType: (string) value must be "geojson"
        :param geoJson: (geoJson) A GeoJson object representing a region of space
        """
        return {'filterType': filterType, 'geoJson': geoJson}

    @classmethod
    def UserContext(cls, contactId, ipAddress):
        """
        :param contactId: (string) Internal user Identifier
        :param ipAddress: (string) Ip address used to send the request
        """
        return {'contactId': contactId, 'ipAddress': ipAddress}

    @classmethod
    def TemporalCoverage(cls, StartDate, endDate):
        """
        :param StartDate: (string) Starting temporal extent of coverage - ISO 8601 Formatted Date
        :param endDate: (string) Ending temporal extent of the coverage - ISO 8601 Formatted Date
        """
        return {'StartDate': StartDate, 'endDate': endDate}

    @classmethod
    def DownloadResponse(cls, id=None, displayId=None, entityId=None, datasetId=None, available=None, filesize=None,
                         productName=None, productCode=None, bulkAvailable=None, downloadSystem=None,
                         secondaryDownloads=None):
        """
        :param id: (int) Scene Identifier
        :param displayId: (string) Scene Identifier used for display
        :param entityId: (string) Entity Identifier
        :param datasetId: (string) Dataset Identifier
        :param available: (string) Value is "Y" or "N". Denotes if the download option is available
        :param filesize: (long) The size of the download in bytes
        :param productName: (string) The user friendly name for this download option
        :param productCode: (string) Internal product code to represent the download option
        :param bulkAvailable: (string) Value is "Y" or "N". Denotes if the download option is available for bulk
        :param downloadSystem: (string) The system that is running the download
        :param secondaryDownloads: (download) An array of related downloads
        """
        return {'id': id, 'displayId': displayId, 'entityId': entityId, 'datasetId': datasetId,
                'available': available, 'filesize': filesize, 'productName': productName,
                'productCode': productCode, 'bulkAvailable': bulkAvailable, 'downloadSystem': downloadSystem,
                'secondaryDownloads': secondaryDownloads}

    @classmethod
    def DownloadInput(cls, entityId, productId, dataUse, label):
        """
        :param entityId: (string) Entity Identifier
        :param productId: (string) Product identifiers
        :param dataUse: (string) The type of use of this data
        :param label: (string) The label name used when requesting the download
        """
        return {'entityId': entityId,
                'productId': productId,
                'dataUse': dataUse,
                'label': label}

    @classmethod
    def DownloadQueueDownload(cls, downloadId, collectionName, datasetId, displayId, entityId, eulaCode, filesize,
                              label, productCode, productName, statusCode, statusText):
        """
        :param downloadId: (int) Download Identifier
        :param collectionName: (string) User friendly name of the collection
        :param datasetId: (string) Dataset Identifier
        :param displayId: (string) Scene Identifier used for display
        :param entityId: (string) Entity Identifier
        :param eulaCode: (string) A EULA Code to use for EULA retrieval - only populated when loading download orders
        :param filesize: (long) The size of the download in bytes
        :param label: (string) The label name used when requesting the download
        :param productCode: (string) Internal product code to represent the download option
        :param productName: (string) The user friendly name for this product
        :param statusCode: (string) Internal status code
        :param statusText: (string) User friendly status
        """
        return {'downloadId': downloadId, 'collectionName': collectionName, 'datasetId': datasetId,
                'displayId': displayId, 'entityId': entityId, 'eulaCode': eulaCode, 'filesize': filesize,
                'label': label, 'productCode': productCode, 'productName': productName, 'statusCode': statusCode,
                'statusText': statusText}

    @classmethod
    def Eula(cls, eulaCode, agreementContent):
        """
        :param eulaCode: (string) A EULA Code to use for EULA retrieval - only populated when loading download orders
        :param agreementContent: (string) Agreement clauses to use the data - only populated when loading download orders
        """
        return {'eulaCode': eulaCode, 'agreementContent': agreementContent}

    @classmethod
    def FilepathDownload(cls, datasetName, productCode, dataPath, dataUse, label):
        """
        :param datasetName: (string) Dataset name
        :param productCode: (string) Internal code used to represent this product during ordering
        :param dataPath: (string) The data location to stream the download from
        :param dataUse: (string) The type of use of this data
        :param label: (string) The label name used when requesting the download
        """
        return {'datasetName': datasetName, 'productCode': productCode, 'dataPath': dataPath, 'dataUse': dataUse,
                'label': label}

    @classmethod
    def Options(cls, bulk, order, download, secondary):
        """
        :param bulk: (boolean) Denotes if the scene is available for bulk
        :param order: (boolean) Denotes if the scene is available for order
        :param download: (boolean) Denotes if the scene is available for download
        :param secondary: (boolean) Denotes if the scene is available for secondary download
        """
        return {'bulk': bulk, 'order': order, 'download': download, 'secondary': secondary}

    @classmethod
    def ProductDownload(cls, datasetName, productIds, sceneFilter):
        """
        :param datasetName: (string) Dataset name
        :param productIds: (string[]) Product identifiers
        :param sceneFilter: (sceneFilter) Used to apply a scene filter on the data
        """
        return {'datasetName': datasetName, 'productIds': productIds, 'sceneFilter': sceneFilter}

    @classmethod
    def Selected(cls, bulk, order, compare):
        """
        :param bulk: (boolean) Denotes if the scene is selected for bulk
        :param order: (boolean) Denotes if the scene is selected for order
        :param compare: (boolean) Denotes if the scene is selected for compare
        """
        return {'bulk': bulk, 'order': order, 'compare': compare}

    @classmethod
    def MetadataExport(cls, exportId, exportName, datasetId, datasetName, sceneFilter, customMessage, exportType,
                       status, statusName, dateEntered, dateUpdated):
        """
        :param exportId: (string) Identifier of this export
        :param exportName: (string) Name of this export
        :param datasetId: (string) Dataset Identifier
        :param datasetName: (string) Dataset name
        :param sceneFilter: (sceneFilter) Used to apply a scene filter on the data
        :param customMessage: (string) The content of the custom message
        :param exportType: (string) Type of this export
        :param status: (string) Internal Status Code
        :param statusName: (string) User Friendly Status
        :param dateEntered: (string) The date this export was entered
        :param dateUpdated: (string) Date the export was last updated
        """
        return {'exportId': exportId, 'exportName': exportName, 'datasetId': datasetId, 'datasetName': datasetName,
                'sceneFilter': sceneFilter, 'customMessage': customMessage, 'exportType': exportType,
                'status': status, 'statusName': statusName, 'dateEntered': dateEntered, 'dateUpdated': dateUpdated}

    @classmethod
    def MetadataField(cls, id, fieldName, dictionaryLink, value):
        """
        :param id: (int) Metadata Identifier
        :param fieldName: (string) The name of the metadata field
        :param dictionaryLink: (string) A link to the data dictionary entry for this field
        :param value: (string) The value for this metadata field
        """
        return {'id': id, 'fieldName': fieldName, 'dictionaryLink': dictionaryLink, 'value': value}

    @classmethod
    def Browse(cls, browseRotationEnabled, browseName, browsePath, overlayPath, overlayType, thumbnailPath):
        """
        :param browseRotationEnabled: (boolean) Denotes if the rotation is enabled for browse
        :param browseName: (string) Name for browse
        :param browsePath: (string) Path for browse
        :param overlayPath: (string) Path of overlay
        :param overlayType: (string) Type of overlay
        :param thumbnailPath: (string) Path of thumbnail
        """
        return {'browseRotationEnabled': browseRotationEnabled, 'browseName': browseName, 'browsePath': browsePath,
                'overlayPath': overlayPath, 'overlayType': overlayType, 'thumbnailPath': thumbnailPath}

    @classmethod
    def Dataset(cls, abstractText, acquisitionStart, acquisitionEnd, catalogs, collectionName, collectionLongName,
                datasetId, datasetAlias, datasetCategoryName, dataOwner, dateUpdated, doiNumber, ingestFrequency,
                keywords, sceneCount, spatialBounds, temporalCoverage, supportCloudCover, supportDeletionSearch):
        """
        :param abstractText: (string) Abstract of the dataset
        :param acquisitionStart: (date) Start date the scene was acquired, ISO 8601 Formatted Date
        :param acquisitionEnd: (date) End date the scene was acquired, ISO 8601 Formatted Date
        :param catalogs: (string[]) The Machine-to-Machine dataset catalogs including "EE", "GV", "HDDS", "LPCS"
        :param collectionName: (string) User friendly name of the collection
        :param collectionLongName: (string) Full User friendly dataset name
        :param datasetId: (string) Dataset Identifier
        :param datasetAlias: (string) Short User friendly dataset name
        :param datasetCategoryName: (string) Category this dataset belongs to
        :param dataOwner: (string) Owner of the data
        :param dateUpdated: (date) Date the dataset was last updated, ISO 8601 Formatted Date
        :param doiNumber: (string) DOI name of the dataset
        :param ingestFrequency: (string) Interval to ingest this dataset (ISO-8601 formatted string)
        :param keywords: (string) Keywords of the dataset
        :param sceneCount: (int) The number of scenes under the dataset
        :param spatialBounds: (spatialBounds) Dataset Spatial Extent
        :param temporalCoverage: (temporalCoverage) Temporal extent of the dataset (ISO 8601 Formatted Date)
        :param supportCloudCover: (boolean) Denotes if the dataset supports cloud cover searching (via cloudCover filter in the scene search parameters)
        :param supportDeletionSearch: (boolean) Denotes if the dataset supports deletion searching
        """
        return {'abstractText': abstractText, 'acquisitionStart': acquisitionStart,
                'acquisitionEnd': acquisitionEnd, 'catalogs': catalogs, 'collectionName': collectionName,
                'collectionLongName': collectionLongName, 'datasetId': datasetId, 'datasetAlias': datasetAlias,
                'datasetCategoryName': datasetCategoryName, 'dataOwner': dataOwner, 'dateUpdated': dateUpdated,
                'doiNumber': doiNumber, 'ingestFrequency': ingestFrequency, 'keywords': keywords,
                'sceneCount': sceneCount, 'spatialBounds': spatialBounds, 'temporalCoverage': temporalCoverage,
                'supportCloudCover': supportCloudCover, 'supportDeletionSearch': supportDeletionSearch}

    @classmethod
    def DatasetCategory(cls, id, categoryName, categoryDescription, parentCategoryId, parentCategoryName,
                        referenceLink):
        """
        :param id: (int) Dataset category Identifier
        :param categoryName: (string) Name of the category
        :param categoryDescription: (string) Description of the category
        :param parentCategoryId: (int) Parent category Identifier
        :param parentCategoryName: (string) Name of the parent category
        :param referenceLink: (string) Information for the category
        """
        return {'id': id, 'categoryName': categoryName, 'categoryDescription': categoryDescription,
                'parentCategoryId': parentCategoryId, 'parentCategoryName': parentCategoryName,
                'referenceLink': referenceLink}

    @classmethod
    def DatasetCustomization(cls, datasetName, excluded, metadata, searchSort):
        """
        :param datasetName: (string) Alias of the dataset
        :param excluded: (boolean) Used to include or exclude a dataset
        :param metadata: (Metadata) Used to customize the layout of a datasets metadata
        :param searchSort: (SearchSort) Used to sort the datasets results
        """
        return {'datasetName': datasetName, 'excluded': excluded, 'metadata': metadata, 'searchSort': searchSort}

    @classmethod
    def Metadata(cls, metadataType, id, sortOrder):
        """
        :param metadataType: (string)Value can be 'export', 'res_sum', 'shp', or 'full'
        :param id: (string) Used to identify which field your referencing.
        :param sortOrder: (integer) Used to change the order in which the fields are sorted.
        """
        return {'metadataType': metadataType, 'id': id, 'sortOrder': sortOrder}

    @classmethod
    def SearchSort(cls, id, direction):
        """
        :param id: (string) Used to identify which field you want to sort by.
        :param direction: (string) Used to determine which directions to sort (ASC, DESC).
        """
        return {'id': id, 'direction': direction}

    @classmethod
    def SortCustomization(cls, field_name, direction):
        """
        :param field_name: (string) Used to identify which field you want to sort by.
        :param direction: (string) Used to determine which directions to sort (ASC, DESC).
        """
        return {'field_name': field_name, 'direction': direction}

    @classmethod
    def DatasetFilter(cls, id, legacyFieldId, dictionaryLink, fieldConfig, fieldLabel, searchSql):
        """
        :param id: (int) Dataset Identifier
        :param legacyFieldId: (int) Legacy field Identifier
        :param dictionaryLink: (string) A link to the data dictionary entry for this field
        :param fieldConfig: (fieldConfig) Configuration of the field
        :param fieldLabel: (string) The label name used when requesting the field
        :param searchSql: (string) WHERE clause when searching in the database
        """
        return {'id': id, 'legacyFieldId': legacyFieldId, 'dictionaryLink': dictionaryLink,
                'fieldConfig': fieldConfig, 'fieldLabel': fieldLabel, 'searchSql': searchSql}

    @classmethod
    def FieldConfig(cls, type, filters, validators, displayListId):
        """
        :param type: (string) Value can be 'Select", 'Text', 'Range'
        :param filters: (filter[]) Reference only. Describes the input for a query
        :param validators: ([]) Reference only. Describes various validation the input data is put through prior to being used in the query
        :param displayListId: (string) Internal reference. Used to reference where provided value lists are sourced from
        """
        return {'type': type, 'filters': filters, 'validators': validators, 'displayListId': displayListId}

    @classmethod
    def Notification(cls, id, subject, messageContent, severityCode, severityCssClass, severityText, dateUpdated):
        """
        :param id: (int) Notification Identifier
        :param subject: (string) The subject of the notification
        :param messageContent: (string) The content of the notification message
        :param severityCode: (string) Internal severity code
        :param severityCssClass: (string) Class of the severity
        :param severityText: (string) The user friendly name for this severity
        :param dateUpdated: (string) Date the notification was last updated
        """
        return {'id': id, 'subject': subject, 'messageContent': messageContent, 'severityCode': severityCode,
                'severityCssClass': severityCssClass, 'severityText': severityText, 'dateUpdated': dateUpdated}

    @classmethod
    def ProductResponse(cls, id, entityId, datasetId, available, price, productName, productCode):
        """
        :param id: (int) Product Identifier
        :param entityId: (string) Entity Identifier
        :param datasetId: (string) Dataset Identifier
        :param available: (string) Denotes if the download option is available
        :param price: (double) The price for ordering this product, less the $5.00 handling fee per order(Handling Fee - Applies to Orders that require payment)
        :param productName: (string) User friendly name for this product
        :param productCode: (string) Internal code used to represent this product during ordering
        """
        return {'id': id, 'entityId': entityId, 'datasetId': datasetId, 'available': available, 'price': price,
                'productName': productName, 'productCode': productCode}

    @classmethod
    def ProductInput(cls, datasetName, entityId, productId, productCode):
        """
        :param datasetName: (string) Dataset name
        :param entityId: (string) Entity Identifier
        :param productId: (string) Product identifiers
        :param productCode: (string) Internal product code to represent the download option
        """
        return {'datasetName': datasetName, 'entityId': entityId, 'productId': productId, 'productCode': productCode}

    @classmethod
    def RunOptions(cls, resultFormats):
        """
        :param resultFormats: (string[]) The valid values are 'metadata', 'email', 'kml', 'shapefile', 'geojson'
        """
        return {'resultFormats': resultFormats}

    @classmethod
    def Scene(cls, browse, cloudCover, entityId, displayId, metadata, options, selected, spatialBounds,
              spatialCoverage, temporalCoverage, publishDate):
        """
        :param browse: (browse) An array of browse options
        :param cloudCover: (string) The cloud cover score for this scene (-1 if score does not exist)
        :param entityId: (string) Entity Identifier
        :param displayId: (string) Scene Identifier used for display
        :param metadata: (metadata) An array of metadata for this scene
        :param options: (options) An array of available download options for this scene
        :param selected: (selected) Denotes if the scene is selected for various systems
        :param spatialBounds: (spatialBounds) Dataset Spatial Extent
        :param spatialCoverage: (spatialBounds) Dataset spatial coverage
        :param temporalCoverage: (temporalCoverage) Dataset temporal coverage
        :param publishDate: (string) The date the scene was published
        """
        return {'browse': browse, 'cloudCover': cloudCover, 'entityId': entityId, 'displayId': displayId,
                'metadata': metadata, 'options': options, 'selected': selected, 'spatialBounds': spatialBounds,
                'spatialCoverage': spatialCoverage, 'temporalCoverage': temporalCoverage,
                'publishDate': publishDate}

    @classmethod
    def IngestSubscription(cls, subscriptionId, subscriptionName, username, catalogId, datasets, runOptions,
                           runStartDate, runEndDate, requestApp, requestAppReferenceId, runFrequency, status,
                           dateEntered, lastRunDate, lastAttemptDate):
        """
        :param subscriptionId: (int) The unique Identifier for the subscription
        :param subscriptionName: (string) Used for user reference to name a request
        :param username: (string) The user who created this subscription
        :param catalogId: (string) The Machine-to-Machine dataset catalog being used
        :param datasets: (string) Used to identify datasets to search and the parameters specific to each dataset
        :param runOptions: (runOptions) Used to set subscription runtime configurations
        :param runStartDate: (string) Used to apply a temporal filter on the data based on ingest date
        :param runEndDate: (string) Used to apply a temporal filter on the data based on ingest date
        :param requestApp: (string)
        :param requestAppReferenceId: (string) The application that is creating the subscription
        :param runFrequency: (string) Run this subscription at this interval
        :param status: (string) The status of the subscription
        :param dateEntered: (string) The date this subscription was entered
        :param lastRunDate: (string) The date of the last run for this subscription
        :param lastAttemptDate: (string) The date of the last attempt for this subscription
        """
        return {'subscriptionId': subscriptionId, 'subscriptionName': subscriptionName, 'username': username,
                'catalogId': catalogId, 'datasets': datasets, 'runOptions': runOptions,
                'runStartDate': runStartDate, 'runEndDate': runEndDate, 'requestApp': requestApp,
                'requestAppReferenceId': requestAppReferenceId, 'runFrequency': runFrequency, 'status': status,
                'dateEntered': dateEntered, 'lastRunDate': lastRunDate, 'lastAttemptDate': lastAttemptDate}

    @classmethod
    def IngestSubscriptionLog(cls, runId, subscriptionId, runDate, executionTime, numScenesMatched, resultCode,
                              runScriptOutput, runSummary, runOptions, datasets, catalogId, lastRunDate, orderIds,
                              bulkIds):
        """
        :param runId: (int) The unique Identifier for this subscription run
        :param subscriptionId: (int) The unique Identifier for the subscription
        :param runDate: (string) The date of this subscription run
        :param executionTime: (string) The number of seconds this subscription took to run
        :param numScenesMatched: (string) The number of scenes this subscription run matched
        :param resultCode: (string) The result of this subscription run
        :param runScriptOutput: (string) The output of this subscription run
        :param runSummary: (string) Any summary text associated with this subscription run
        :param runOptions: (runOptions) Runtime configurations of this subscription run
        :param datasets: (string) Datasets of this subscription run
        :param catalogId: (string) The Machine-to-Machine dataset catalog being used
        :param lastRunDate: (string) The date of the last run for this subscription
        :param orderIds: (string) Tram order Identifier
        :param bulkIds: (string) Bulk order Identifier
        """
        return {'runId': runId, 'subscriptionId': subscriptionId, 'runDate': runDate,
                'executionTime': executionTime, 'numScenesMatched': numScenesMatched, 'resultCode': resultCode,
                'runScriptOutput': runScriptOutput, 'runSummary': runSummary, 'runOptions': runOptions,
                'datasets': datasets, 'catalogId': catalogId, 'lastRunDate': lastRunDate, 'orderIds': orderIds,
                'bulkIds': bulkIds}

    @classmethod
    def SubscriptionDataset(cls, datasetName):
        """
        :param datasetName: (string) Dataset name
        """
        return {'datasetName': datasetName}

    @classmethod
    def TramOrder(cls, orderId, username, processingPriority, orderComment, statusCode, statusCodeText, dateEntered,
                  lastUpdatedDate):
        """
        :param orderId: (int) Order Identifier
        :param username: (string) The user who created this order
        :param processingPriority: (int) Processing priority for the order
        :param orderComment: (string) Comment contents of the order
        :param statusCode: (string) Internal status code
        :param statusCodeText: (string) User friendly status
        :param dateEntered: (string) The date this order was entered
        :param lastUpdatedDate: (string) Date the order was last updated
        """
        return {'orderId': orderId, 'username': username, 'processingPriority': processingPriority,
                'orderComment': orderComment, 'statusCode': statusCode, 'statusCodeText': statusCodeText,
                'dateEntered': dateEntered, 'lastUpdatedDate': lastUpdatedDate}

    @classmethod
    def TramUnit(cls, unitNumber, productCode, productName, datasetId, datasetName, collectionName, orderingId,
                 unitPrice, unitComment, statusCode, statusCodeText, lastUpdatedDate):
        """
        :param unitNumber: (int) The unit Identifier
        :param productCode: (string) Internal product code
        :param productName: (string) The user friendly name for the product
        :param datasetId: (string) Dataset identifier
        :param datasetName: (string) Dataset name
        :param collectionName: (string) User friendly name of the collection
        :param orderingId: (string) Scene Identifier used within the ordering system
        :param unitPrice: (string) The price for ordering this unit
        :param unitComment: (string) Any comments that should be retained with this product
        :param statusCode: (string) Internal status code
        :param statusCodeText: (string) User friendly status
        :param lastUpdatedDate: (string) Date the unit was last updated
        """
        return {'unitNumber': unitNumber, 'productCode': productCode, 'productName': productName,
                'datasetId': datasetId, 'datasetName': datasetName, 'collectionName': collectionName,
                'orderingId': orderingId, 'unitPrice': unitPrice, 'unitComment': unitComment,
                'statusCode': statusCode, 'statusCodeText': statusCodeText, 'lastUpdatedDate': lastUpdatedDate}
