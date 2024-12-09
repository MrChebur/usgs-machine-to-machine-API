"""
Implementation date: 22.11.2024

This API complies with the data types given in:
https://m2m.cr.usgs.gov/api/docs/datatypes/
"""
from typing import Literal


class AbstractDataType:
    """
    Use `self.dict` to return the class attributes as a dictionary.
    """

    def __init__(self):
        self.dict = self._as_dict()

    def _as_dict(self) -> dict:
        attributes = self.__dict__.items()
        attributes_filtered = dict((key, value) for key, value in attributes if not key.startswith('_'))
        object.__setattr__(self, '_dict', attributes_filtered)  # avoid recursion self._dict = attributes_filtered
        return attributes_filtered

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)  # avoid recursion self.name = value
        object.__setattr__(self, '_dict', self._as_dict())  # avoid recursion self._dict = self._as_dict()


# ===================== USGS data types are below this line =====================

# To make it easier to check for updates and new data types, all classes are listed in order of appearance on the
# source page: https://m2m.cr.usgs.gov/api/docs/datatypes/, but this is against the python rule: "classes must be
# defined before they can be used".  So some classes are moved and comments are left where they were originally.


class AcquisitionFilter(AbstractDataType):
    """
    :param start: (string) The date the scene began acquisition - ISO 8601 Formatted Date
    :param end: (string) The date the scene ended acquisition - ISO 8601 Formatted Date
    """

    def __init__(self,
                 start: str | None = None,
                 end: str | None = None):
        self.start = start
        self.end = end

        self.dict = self._as_dict()


class CloudCoverFilter(AbstractDataType):
    """
    :param min: (int) Used to limit results by minimum cloud cover (for supported datasets)
    :param max: (int) Used to limit results by maximum cloud cover (for supported datasets)
    :param includeUnknown: (boolean) Used to determine if scenes with unknown cloud cover values should be included in
                           the results
    """

    def __init__(self,
                 min: int | None = None,
                 max: int | None = None,
                 includeUnknown: bool | None = None):
        self.min = min
        self.max = max
        self.includeUnknown = includeUnknown

        self.dict = self._as_dict()


class Coordinate(AbstractDataType):
    """
    :param latitude: (double) Decimal degree coordinate in EPSG:4326 projection
    :param longitude: (double) Decimal degree coordinate in EPSG:4326 projection
    """

    def __init__(self,
                 latitude: float,
                 longitude: float):
        self.latitude = latitude
        self.longitude = longitude

        self.dict = self._as_dict()


class DateRange(AbstractDataType):
    """
    :param startDate: (string) Used to apply a temporal filter on the data - ISO 8601 Formatted Date
    :param endDate: (string) Used to apply a temporal filter on the data - ISO 8601 Formatted Date
    """

    def __init__(self,
                 startDate: str | None = None,
                 endDate: str | None = None):
        self.startDate = startDate
        self.endDate = endDate

        self.dict = self._as_dict()


# replaced
class IngestUpdateTemplate(AbstractDataType):
    """
    :param templateId: (string) value must be 'ingestUpdate'
    :param darId: (string) The number of data acquisition request
    :param sceneIds: (string[]) An array of Scene IDs
    :param viewName: (string) The view name of the dataset
    :param idField: (string) Used to determine the ID being used in EE (EE_DISPLAY_ID by default)
    """

    def __init__(self,
                 templateId: Literal['ingestUpdate'] = 'ingestUpdate',
                 darId: str | None = None,
                 sceneIds: list[str] | None = None,
                 viewName: str | None = None,
                 idField: str | None = None):
        self.templateId = templateId
        self.darId = darId
        self.sceneIds = sceneIds
        self.viewName = viewName
        self.idField = idField

        self.dict = self._as_dict()


class TemplateConfiguration(IngestUpdateTemplate):
    """
    This is an abstract data model, use ingestUpdateTemplate
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GeoJson(AbstractDataType):
    """
   :param type: (string) Geometry types supported by GeoJson, like polygon
   :param coordinates: (coordinate[]) Coordinate array
   """

    def __init__(self,
                 type: str,
                 coordinates: list | list[Coordinate]):
        self.type = type
        self.coordinates = coordinates

        self.dict = self._as_dict()


# IngestUpdateTemplate original place

class IngestFilter(AbstractDataType):
    """
    :param start: (string) Used to filter scenes by last metadata ingest
    :param end: (string) Used to filter scenes by last metadata ingest
    """

    def __init__(self,
                 start: str | None = None,
                 end: str | None = None):
        self.start = start
        self.end = end

        self.dict = self._as_dict()


class MetadataFilter(AbstractDataType):  # MetadataFilter/Metadata
    """
    This is an abstract data model, use MetadataAnd, MetadataBetween, MetadataOr, or MetadataValue
    """

    def __init__(self, **kwargs):
        if 'filterType' not in kwargs:
            raise ValueError(f'filterType parameter is required')

        if kwargs['filterType'] == "and":
            # noinspection PyTypeChecker
            MetadataAnd.__init__(self, **kwargs)

        elif kwargs['filterType'] == "between":
            # noinspection PyTypeChecker
            MetadataBetween.__init__(self, **kwargs)

        elif kwargs['filterType'] == "or":
            # noinspection PyTypeChecker
            MetadataOr.__init__(self, **kwargs)

        elif kwargs['filterType'] == "value":
            # noinspection PyTypeChecker
            MetadataValue.__init__(self, **kwargs)

        else:
            raise ValueError(
                f'Invalid filterType value: {kwargs["filterType"]}. Check for SpatialFilterMbr or SpatialFilterGeoJson data types')  #


class MetadataAnd(AbstractDataType):
    """
    :param filterType: (string) Value must be "and"
    :param childFilters: (metadataFilter[]) Joins any filter parameters together with the "and" logical operator
    """

    def __init__(self,
                 childFilters: list[MetadataFilter],
                 filterType: Literal['and'] = 'and'):
        self.childFilters = childFilters
        self.filterType = filterType

        self.dict = self._as_dict()


class MetadataBetween(AbstractDataType):
    """
    :param filterType (string) Value must be "between"
    :param filterId (string) Unique Identifier for the dataset criteria field and it can be retrieved by dataset-filters
                             https://m2m.cr.usgs.gov/api/docs/reference/#dataset-filters
    :param firstValue (int) First value in between clause
    :param secondValue (int) Second value in between clause
    """

    def __init__(self,
                 filterType: Literal['between'],
                 filterId: str | None = None,
                 firstValue: int | None = None,
                 secondValue: int | None = None):
        self.filterType = filterType
        self.filterId = filterId
        self.firstValue = firstValue
        self.secondValue = secondValue

        self.dict = self._as_dict()


class MetadataOr(AbstractDataType):
    """
    :param filterType (string) Value must be "or"
    :param childFilters: (metadataFilter[]) Joins any filter parameters together with the "or" logical operator
    """

    def __init__(self,
                 childFilters: list[MetadataFilter],
                 filterType: Literal['or'] = 'or'):
        self.filterType = filterType
        self.childFilters = childFilters

        self.dict = self._as_dict()


class MetadataValue(AbstractDataType):
    """
    :param filterType (string) Value must be "value"
    :param filterId (string) Unique Identifier for the dataset criteria field and it can be retrieved by dataset-filters
    :param value (string) Value to use
    :param operand (string) Determines what operand to search with - accepted values are "=" and "like"
    """

    def __init__(self,
                 filterType: Literal['value'] = 'value',
                 filterId: str | None = None,
                 value: str | None = None,
                 operand: str | None = None):
        self.filterType = filterType
        self.filterId = filterId
        self.value = value
        self.operand = operand

        self.dict = self._as_dict()


# replaced
class SpatialFilter(AbstractDataType):
    """
    This is an abstract data model, use SpatialFilterMbr or SpatialFilterGeoJson
    """

    def __init__(self, **kwargs):
        if 'filterType' not in kwargs:
            raise ValueError(f'filterType parameter is required')

        if kwargs['filterType'] == "mbr":
            # noinspection PyTypeChecker
            SpatialFilterMbr.__init__(self, **kwargs)

        elif kwargs['filterType'] == "geojson":
            # noinspection PyTypeChecker
            SpatialFilterGeoJson.__init__(self, **kwargs)

        else:
            raise ValueError(
                f'Invalid filterType value: {kwargs["filterType"]}. Check for SpatialFilterMbr or SpatialFilterGeoJson data types')


# replaced
class SceneFilter(AbstractDataType):
    """
    :param acquisitionFilter: (AcquisitionFilter) Used to apply a acquisition filter on the data
    :param cloudCoverFilter: (CloudCoverFilter) Used to apply a cloud cover filter on the data
    :param datasetName: (string) Dataset name
    :param ingestFilter: (IngestFilter) Used to apply an ingest filter on the data
    :param metadataFilter: (MetadataFilter) Used to apply a metadata filter on the data
    :param seasonalFilter: (int[]) Used to apply month numbers from 1 to 12 on the data
    :param spatialFilter: (SpatialFilter) Used to apply a spatial filter on the data
    """

    def __init__(self,
                 acquisitionFilter: AcquisitionFilter | None = None,
                 cloudCoverFilter: CloudCoverFilter | None = None,
                 datasetName: str | None = None,
                 ingestFilter: IngestFilter | None = None,
                 metadataFilter: MetadataFilter | None = None,
                 seasonalFilter: list[int] | None = None,
                 spatialFilter: SpatialFilter | None = None):
        self.acquisitionFilter = acquisitionFilter
        self.cloudCoverFilter = cloudCoverFilter
        self.datasetName = datasetName
        self.ingestFilter = ingestFilter
        self.metadataFilter = metadataFilter
        self.seasonalFilter = seasonalFilter
        self.spatialFilter = spatialFilter

        self.dict = self._as_dict()


class SceneDatasetFilter(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    :param sceneFilter: (sceneFilter) Used to apply a scene filter on the data
    """

    def __init__(self,
                 datasetName: str | None = None,
                 sceneFilter: SceneFilter | None = None):
        self.datasetName = datasetName
        self.sceneFilter = sceneFilter

        self.dict = self._as_dict()


# SceneFilter original place


class SceneMetadataConfig(AbstractDataType):
    """
    :param includeNulls: (boolean) Used to include or exclude null values
    :param type: (string) Value can be 'full', 'summary' or null
    :param template: (string) Metadata template
    """

    # todo: check if parameter `type` allows None or only 'null' values (as string)?
    def __init__(self,
                 includeNulls: bool | None = None,
                 type: Literal['full', 'summary'] | None = None,
                 template: str | None = None):
        self.includeNulls = includeNulls
        self.type = type
        self.template = template

        self.dict = self._as_dict()


class SpatialBounds(AbstractDataType):
    """
    This is an abstract data model, use spatialBoundsMbr or geoJson
    """

    def __init__(self, **kwargs):
        if 'north' in kwargs:
            # noinspection PyTypeChecker
            SpatialBoundsMbr.__init__(self, **kwargs)
        elif 'coordinates' in kwargs:
            # noinspection PyTypeChecker
            GeoJson.__init__(self, **kwargs)
        raise ValueError(
            f"'north' or 'coordinates' parameter is required. Check for SpatialBoundsMbr or GeoJson data types")


class SpatialBoundsMbr(AbstractDataType):
    """
    :param north: (string) Decimal degree coordinate value in EPSG:4326 projection representing the northern most point of the MBR
    :param east: (string) Decimal degree coordinate value in EPSG:4326 projection representing the eastern most point of the MBR
    :param south: (string) Decimal degree coordinate value in EPSG:4326 projection representing the southern most point of the MBR
    :param west: (string) Decimal degree coordinate value in EPSG:4326 projection representing the western most point of the MBR
    """

    def __init__(self,
                 north: str | None = None,
                 east: str | None = None,
                 south: str | None = None,
                 west: str | None = None):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.dict = self._as_dict()


# SpatialFilter original place


class SpatialFilterMbr(AbstractDataType):
    """
    :param filterType: (string) value must be "mbr"
    :param lowerLeft: (Coordinate) The southwest point of the minimum bounding rectangle
    :param upperRight: (Coordinate) The northeast point of the minimum bounding rectangle
    """

    def __init__(self,
                 lowerLeft: Coordinate,
                 upperRight: Coordinate,
                 filterType: Literal['mbr'] = 'mbr'):
        self.lowerLeft = lowerLeft
        self.upperRight = upperRight
        self.filterType = filterType

        self.dict = self._as_dict()


class SpatialFilterGeoJson(AbstractDataType):
    """
    :param filterType: (string) value must be "geojson"
    :param geoJson: (geoJson) A GeoJson object representing a region of space
    """

    def __init__(self,
                 geoJson: GeoJson,
                 filterType: Literal['geojson'] = 'geojson'):
        self.filterType = filterType
        self.geoJson = geoJson

        self.dict = self._as_dict()


class UserContext(AbstractDataType):
    """
    :param contactId: (string) Internal user Identifier
    :param ipAddress: (string) Ip address used to send the request
    """

    def __init__(self,
                 contactId: str | None,
                 ipAddress: str | None):
        self.contactId = contactId
        self.ipAddress = ipAddress

        self.dict = self._as_dict()


class TemporalCoverage(AbstractDataType):
    """
    :param StartDate: (date) Starting temporal extent of coverage - ISO 8601 Formatted Date
    :param endDate: (date) Ending temporal extent of the coverage - ISO 8601 Formatted Date
    Even though this specifies the `date` data type, it is most likely `str` (not tested)
    """

    def __init__(self,
                 StartDate: str | None = None,
                 endDate: str | None = None):
        self.StartDate = StartDate
        self.endDate = endDate

        self.dict = self._as_dict()


class TemporalFilter(AbstractDataType):
    """
    :param start: (date) ISO 8601 Formatted Date
    :param end: (date) ISO 8601 Formatted Date
    Even though this specifies the `date` data type, it is most likely `str` (not tested)
    """

    def __init__(self,
                 start: str | None = None,
                 end: str | None = None):
        self.start = start
        self.end = end

        self.dict = self._as_dict()


class DownloadResponse(AbstractDataType):
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
    :param secondaryDownloads: (DownloadResponse) An array of related downloads
    """

    def __init__(self,
                 id: int | None = None,
                 displayId: str | None = None,
                 entityId: str | None = None,
                 datasetId: str | None = None,
                 available: Literal['Y', 'N'] | None = None,
                 filesize: int | None = None,
                 productName: str | None = None,
                 productCode: str | None = None,
                 bulkAvailable: Literal['Y', 'N'] | None = None,
                 downloadSystem: str | None = None,
                 secondaryDownloads: list | None = None):
        self.id = id
        self.displayId = displayId
        self.entityId = entityId
        self.datasetId = datasetId
        self.available = available
        self.filesize = filesize
        self.productName = productName
        self.productCode = productCode
        self.bulkAvailable = bulkAvailable
        self.downloadSystem = downloadSystem
        self.secondaryDownloads = secondaryDownloads

        self.dict = self._as_dict()


class DownloadInput(AbstractDataType):
    """
    :param entityId: (string) Entity Identifier
    :param productId: (string) Product identifiers
    :param dataUse: (string) The type of use of this data
    :param label: (string) The label name used when requesting the download
    """

    def __init__(self,
                 entityId: str | None = None,
                 productId: str | None = None,
                 dataUse: str | None = None,
                 label: str | None = None):
        self.entityId = entityId
        self.productId = productId
        self.dataUse = dataUse
        self.label = label

        self.dict = self._as_dict()


class DownloadQueueDownload(AbstractDataType):
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

    def __init__(self,
                 downloadId: int | None = None,
                 collectionName: str | None = None,
                 datasetId: str | None = None,
                 displayId: str | None = None,
                 entityId: str | None = None,
                 eulaCode: str | None = None,
                 filesize: int | None = None,
                 label: str | None = None,
                 productCode: str | None = None,
                 productName: str | None = None,
                 statusCode: str | None = None,
                 statusText: str | None = None):
        self.downloadId = downloadId
        self.collectionName = collectionName
        self.datasetId = datasetId
        self.displayId = displayId
        self.entityId = entityId
        self.eulaCode = eulaCode
        self.filesize = filesize
        self.label = label
        self.productCode = productCode
        self.productName = productName
        self.statusCode = statusCode
        self.statusText = statusText

        self.dict = self._as_dict()


class Eula(AbstractDataType):
    """
    :param eulaCode: (string) A EULA Code to use for EULA retrieval - only populated when loading download orders
    :param agreementContent: (string) Agreement clauses to use the data - only populated when loading download orders
    """

    def __init__(self,
                 eulaCode: str | None = None,
                 agreementContent: str | None = None):
        self.eulaCode = eulaCode
        self.agreementContent = agreementContent

        self.dict = self._as_dict()


class FilegroupDownload(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    :param fileGroups: (string[]) Internal codes used to represent the file groups
    :param listId: (string) The name of scene list to request from
    :param dataUse: (string) The type of use of this data
    :param label: (string) The label name used when requesting the download
    """

    def __init__(self,
                 datasetName: str | None = None,
                 fileGroups: list[str] | None = None,
                 listId: str | None = None,
                 dataUse: str | None = None,
                 label: str | None = None):
        self.datasetName = datasetName
        self.fileGroups = fileGroups
        self.listId = listId
        self.dataUse = dataUse
        self.label = label

        self.dict = self._as_dict()


class FilepathDownload(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    :param productCode: (string) Internal code used to represent this product during ordering
    :param dataPath: (string) The data location to stream the download from
    :param dataUse: (string) The type of use of this data
    :param label: (string) The label name used when requesting the download
    """

    def __init__(self,
                 datasetName: str | None = None,
                 productCode: str | None = None,
                 dataPath: str | None = None,
                 dataUse: str | None = None,
                 label: str | None = None):
        self.datasetName = datasetName
        self.productCode = productCode
        self.dataPath = dataPath
        self.dataUse = dataUse
        self.label = label

        self.dict = self._as_dict()


class Options(AbstractDataType):
    """
    :param bulk: (boolean) Denotes if the scene is available for bulk
    :param order: (boolean) Denotes if the scene is available for order
    :param download: (boolean) Denotes if the scene is available for download
    :param secondary: (boolean) Denotes if the scene is available for secondary download
    """

    def __init__(self,
                 bulk: bool | None = None,
                 order: bool | None = None,
                 download: bool | None = None,
                 secondary: bool | None = None):
        self.bulk = bulk
        self.order = order
        self.download = download
        self.secondary = secondary

        self.dict = self._as_dict()


class ProductDownload(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    :param productIds: (string[]) Product identifiers
    :param sceneFilter: (SceneFilter) Used to apply a scene filter on the data
    """

    def __init__(self,
                 datasetName: str | None = None,
                 productIds: list[str] | None = None,
                 sceneFilter: SceneFilter | None = None):
        self.datasetName = datasetName
        self.productIds = productIds
        self.sceneFilter = sceneFilter

        self.dict = self._as_dict()


class ProxiedDownload(AbstractDataType):
    """
    :param downloadId: (int) Download Identifier
    :param downloadedSize: (bigint) Total downloaded size of the file
    """

    def __init__(self,
                 downloadId: int | None = None,
                 downloadedSize: int | None = None):
        self.downloadId = downloadId
        self.downloadedSize = downloadedSize

        self.dict = self._as_dict()


class Selected(AbstractDataType):
    """
    :param bulk: (boolean) Denotes if the scene is selected for bulk
    :param order: (boolean) Denotes if the scene is selected for order
    :param compare: (boolean) Denotes if the scene is selected for compare
    """

    def __init__(self,
                 bulk: bool | None = None,
                 order: bool | None = None,
                 compare: bool | None = None):
        self.bulk = bulk
        self.order = order
        self.compare = compare

        self.dict = self._as_dict()


class MetadataExport(AbstractDataType):
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

    def __init__(self,
                 exportId: str | None = None,
                 exportName: str | None = None,
                 datasetId: str | None = None,
                 datasetName: str | None = None,
                 sceneFilter: SceneFilter | None = None,
                 customMessage: str | None = None,
                 exportType: str | None = None,
                 status: str | None = None,
                 statusName: str | None = None,
                 dateEntered: str | None = None,
                 dateUpdated: str | None = None):
        self.exportId = exportId
        self.exportName = exportName
        self.datasetId = datasetId
        self.datasetName = datasetName
        self.sceneFilter = sceneFilter
        self.customMessage = customMessage
        self.exportType = exportType
        self.status = status
        self.statusName = statusName
        self.dateEntered = dateEntered
        self.dateUpdated = dateUpdated

        self.dict = self._as_dict()


class MetadataField(AbstractDataType):
    """
    :param id: (int) Metadata Identifier
    :param fieldName: (string) The name of the metadata field
    :param dictionaryLink: (string) A link to the data dictionary entry for this field
    :param value: (string) The value for this metadata field
    """

    def __init__(self,
                 id: int | None = None,
                 fieldName: str | None = None,
                 dictionaryLink: str | None = None,
                 value: str | None = None):
        self.id = id
        self.fieldName = fieldName
        self.dictionaryLink = dictionaryLink
        self.value = value

        self.dict = self._as_dict()


class Browse(AbstractDataType):
    """
    :param browseRotationEnabled: (boolean) Denotes if the rotation is enabled for browse
    :param browseName: (string) Name for browse
    :param browsePath: (string) Path for browse
    :param overlayPath: (string) Path of overlay
    :param overlayType: (string) Type of overlay
    :param thumbnailPath: (string) Path of thumbnail
    """

    def __init__(self,
                 browseRotationEnabled: bool | None = None,
                 browseName: str | None = None,
                 browsePath: str | None = None,
                 overlayPath: str | None = None,
                 overlayType: str | None = None,
                 thumbnailPath: str | None = None):
        self.browseRotationEnabled = browseRotationEnabled
        self.browseName = browseName
        self.browsePath = browsePath
        self.overlayPath = overlayPath
        self.overlayType = overlayType
        self.thumbnailPath = thumbnailPath

        self.dict = self._as_dict()


class Dataset(AbstractDataType):
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
    :param supportCloudCover: (boolean) Denotes if the dataset supports cloud cover searching (via cloudCover filter in
    the scene search parameters)
    :param supportDeletionSearch: (boolean) Denotes if the dataset supports deletion searching
    """

    def __init__(self, abstractText: str | None = None,
                 acquisitionStart: str | None = None,
                 acquisitionEnd: str | None = None,
                 catalogs: list[str] | None = None,
                 collectionName: str | None = None,
                 collectionLongName: str | None = None,
                 datasetId: str | None = None,
                 datasetAlias: str | None = None,
                 datasetCategoryName: str | None = None,
                 dataOwner: str | None = None,
                 dateUpdated: str | None = None,
                 doiNumber: str | None = None,
                 ingestFrequency: str | None = None,
                 keywords: str | None = None,
                 sceneCount: int | None = None,
                 spatialBounds: SpatialBounds | None = None,
                 temporalCoverage: TemporalCoverage | None = None,
                 supportCloudCover: bool | None = None,
                 supportDeletionSearch: bool | None = None):
        self.abstractText = abstractText
        self.acquisitionStart = acquisitionStart
        self.acquisitionEnd = acquisitionEnd
        self.catalogs = catalogs
        self.collectionName = collectionName
        self.collectionLongName = collectionLongName
        self.datasetId = datasetId
        self.datasetAlias = datasetAlias
        self.datasetCategoryName = datasetCategoryName
        self.dataOwner = dataOwner
        self.dateUpdated = dateUpdated
        self.doiNumber = doiNumber
        self.ingestFrequency = ingestFrequency
        self.keywords = keywords
        self.sceneCount = sceneCount
        self.spatialBounds = spatialBounds
        self.temporalCoverage = temporalCoverage
        self.supportCloudCover = supportCloudCover
        self.supportDeletionSearch = supportDeletionSearch

        self.dict = self._as_dict()


class DatasetCategory(AbstractDataType):
    """
    :param id: (int) Dataset category Identifier
    :param categoryName: (string) Name of the category
    :param categoryDescription: (string) Description of the category
    :param parentCategoryId: (int) Parent category Identifier
    :param parentCategoryName: (string) Name of the parent category
    :param referenceLink: (string) Information for the category
    """

    def __init__(self,
                 id: int | None = None,
                 categoryName: str | None = None,
                 categoryDescription: str | None = None,
                 parentCategoryId: int | None = None,
                 parentCategoryName: str | None = None,
                 referenceLink: str | None = None):
        self.id = id
        self.categoryName = categoryName
        self.categoryDescription = categoryDescription
        self.parentCategoryId = parentCategoryId
        self.parentCategoryName = parentCategoryName
        self.referenceLink = referenceLink

        self.dict = self._as_dict()


# replaced
class Metadata(AbstractDataType):
    """
    :param metadataType: (string) Value can be 'export', 'res_sum', 'shp', or 'full'
    :param id: (string) Used to identify which field your referencing.
    :param sortOrder: (integer) Used to change the order in which the fields are sorted.
    """

    def __init__(self,
                 metadataType: Literal['export', 'res_sum', 'shp', 'full'] | None = None,
                 id: str | None = None,
                 sortOrder: int | None = None):
        self.metadataType = metadataType
        self.id = id
        self.sortOrder = sortOrder

        self.dict = self._as_dict()


# replaced
class SearchSort(AbstractDataType):
    """
    :param id: (string) Used to identify which field you want to sort by.
    :param direction: (string) Used to determine which directions to sort (ASC, DESC).
    """

    def __init__(self,
                 id: str | None = None,
                 direction: Literal['ASC', 'DESC'] | None = None):
        self.id = id
        self.direction = direction

        self.dict = self._as_dict()


# replaced
class FileGroups(AbstractDataType):
    """
    :param fileGroupId: (string) Values are the internal file group IDs.
    :param productIds: (string[]) An array of product IDs within the file group.
    """

    def __init__(self,
                 fileGroupId: str | None = None,
                 productIds: list[str] | None = None):
        self.fileGroupId = fileGroupId
        self.productIds = productIds

        self.dict = self._as_dict()


class DatasetCustomization(AbstractDataType):
    """
    :param datasetName: (string) Alias of the dataset
    :param excluded: (boolean) Used to include or exclude a dataset
    :param metadata: (Metadata) Used to customize the layout of a datasets metadata
    :param searchSort: (SearchSort) Used to sort the datasets results
    :param fileGroups: (FileGroups) Used to customize the downloads by file groups
    """

    def __init__(self,
                 datasetName: str | None = None,
                 excluded: str | None = None,
                 metadata: Metadata | None = None,
                 searchSort: SearchSort | None = None,
                 fileGroups: FileGroups | None = None
                 ):
        self.datasetName = datasetName
        self.excluded = excluded
        self.metadata = metadata
        self.searchSort = searchSort
        self.fileGroups = fileGroups

        self.dict = self._as_dict()


# Metadata original place


# SearchSort original place


# FileGroups original place


class SortCustomization(AbstractDataType):
    """
    :param field_name: (string) Used to identify which field you want to sort by.
    :param direction: (string) Used to determine which directions to sort (ASC, DESC).
    """

    def __init__(self,
                 field_name: str | None = None,
                 direction: Literal['ASC', 'DESC'] | None = None):
        self.field_name = field_name
        self.direction = direction

        self.dict = self._as_dict()


# replaced
class FieldConfig(AbstractDataType):
    """
    :param type: (string) Value can be 'Select", 'Text', 'Range'
    :param filters: (filter[]) Reference only. Describes the input for a query
    :param validators: ([]) Reference only. Describes various validation the input data is put through prior to being
    used in the query
    :param displayListId: (string) Internal reference. Used to reference where provided value lists are sourced from
    """

    # todo: It's not clear to me what these data types are: `filter[]` and `[]`.
    def __init__(self,
                 type: Literal['Select', 'Text', 'Range'],
                 filters: list | None = None,
                 validators: list | None = None,
                 displayListId: str | None = None):
        self.type = type
        self.filters = filters
        self.validators = validators
        self.displayListId = displayListId

        self.dict = self._as_dict()


class DatasetFilter(AbstractDataType):
    """
    :param id: (int) Dataset Identifier
    :param legacyFieldId: (int) Legacy field Identifier
    :param dictionaryLink: (string) A link to the data dictionary entry for this field
    :param fieldConfig: (FieldConfig) Configuration of the field
    :param fieldLabel: (string) The label name used when requesting the field
    :param searchSql: (string) WHERE clause when searching in the database
    """

    def __init__(self,
                 id: int | None = None,
                 legacyFieldId: int | None = None,
                 dictionaryLink: str | None = None,
                 fieldConfig: FieldConfig | None = None,
                 fieldLabel: str | None = None,
                 searchSql: str | None = None):
        self.id = id
        self.legacyFieldId = legacyFieldId
        self.dictionaryLink = dictionaryLink
        self.fieldConfig = fieldConfig
        self.fieldLabel = fieldLabel
        self.searchSql = searchSql

        self.dict = self._as_dict()


# FieldConfig original place


class Notification(AbstractDataType):
    """
    :param id: (int) Notification Identifier
    :param subject: (string) The subject of the notification
    :param messageContent: (string) The content of the notification message
    :param severityCode: (string) Internal severity code
    :param severityCssClass: (string) Class of the severity
    :param severityText: (string) The user friendly name for this severity
    :param dateUpdated: (string) Date the notification was last updated
    """

    def __init__(self,
                 id: int | None = None,
                 subject: str | None = None,
                 messageContent: str | None = None,
                 severityCode: str | None = None,
                 severityCssClass: str | None = None,
                 severityText: str | None = None,
                 dateUpdated: str | None = None):
        self.id = id
        self.subject = subject
        self.messageContent = messageContent
        self.severityCode = severityCode
        self.severityCssClass = severityCssClass
        self.severityText = severityText
        self.dateUpdated = dateUpdated

        self.dict = self._as_dict()


class ProductResponse(AbstractDataType):
    """
    :param id: (int) Product Identifier
    :param entityId: (string) Entity Identifier
    :param datasetId: (string) Dataset Identifier
    :param available: (string) Denotes if the download option is available
    :param price: (double) The price for ordering this product, less the $5.00 handling fee per order(Handling Fee -
     Applies to Orders that require payment)
    :param productName: (string) User friendly name for this product
    :param productCode: (string) Internal code used to represent this product during ordering
    """

    def __init__(self,
                 id: int | None = None,
                 entityId: str | None = None,
                 datasetId: str | None = None,
                 available: str | None = None,
                 price: float | None = None,
                 productName: str | None = None,
                 productCode: str | None = None):
        self.id = id
        self.entityId = entityId
        self.datasetId = datasetId
        self.available = available
        self.price = price
        self.productName = productName
        self.productCode = productCode

        self.dict = self._as_dict()


class ProductInput(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    :param entityId: (string) Entity Identifier
    :param productId: (string) Product identifiers
    :param productCode: (string) Internal product code to represent the download option
    """

    def __init__(self,
                 datasetName: str | None = None,
                 entityId: str | None = None,
                 productId: str | None = None,
                 productCode: str | None = None):
        self.datasetName = datasetName
        self.entityId = entityId
        self.productId = productId
        self.productCode = productCode

        self.dict = self._as_dict()


class RunOptions(AbstractDataType):
    """
    :param resultFormats: (string[]) The valid values are 'metadata', 'email', 'kml', 'shapefile', 'geojson'
    """

    def __init__(self, resultFormats: Literal['metadata', 'email', 'kml', 'shapefile', 'geojson']):
        self.resultFormats = resultFormats

        self.dict = self._as_dict()


class Scene(AbstractDataType):
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

    def __init__(self,
                 browse: Browse | None = None,
                 cloudCover: str | None = None,
                 entityId: str | None = None,
                 displayId: str | None = None,
                 metadata: list[MetadataField] | None = None,
                 options: Options | None = None,
                 selected: Selected | None = None,
                 spatialBounds: SpatialBounds | None = None,
                 spatialCoverage: SpatialBounds | None = None,
                 temporalCoverage: TemporalCoverage | None = None,
                 publishDate: str | None = None):
        self.browse = browse
        self.cloudCover = cloudCover
        self.entityId = entityId
        self.displayId = displayId
        self.metadata = metadata
        self.options = options
        self.selected = selected
        self.spatialBounds = spatialBounds
        self.spatialCoverage = spatialCoverage
        self.temporalCoverage = temporalCoverage
        self.publishDate = publishDate

        self.dict = self._as_dict()


class IngestSubscription(AbstractDataType):
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

    def __init__(self,
                 subscriptionId: int | None = None,
                 subscriptionName: str | None = None,
                 username: str | None = None,
                 catalogId: str | None = None,
                 datasets: str | None = None,
                 runOptions: RunOptions | None = None,
                 runStartDate: str | None = None,
                 runEndDate: str | None = None,
                 requestApp: str | None = None,
                 requestAppReferenceId: str | None = None,
                 runFrequency: str | None = None,
                 status: str | None = None,
                 dateEntered: str | None = None,
                 lastRunDate: str | None = None,
                 lastAttemptDate: str | None = None):
        self.subscriptionId = subscriptionId
        self.subscriptionName = subscriptionName
        self.username = username
        self.catalogId = catalogId
        self.datasets = datasets
        self.runOptions = runOptions
        self.runStartDate = runStartDate
        self.runEndDate = runEndDate
        self.requestApp = requestApp
        self.requestAppReferenceId = requestAppReferenceId
        self.runFrequency = runFrequency
        self.status = status
        self.dateEntered = dateEntered
        self.lastRunDate = lastRunDate
        self.lastAttemptDate = lastAttemptDate

        self.dict = self._as_dict()


class IngestSubscriptionLog(AbstractDataType):
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

    def __init__(self,
                 runId: int | None = None,
                 subscriptionId: int | None = None,
                 runDate: str | None = None,
                 executionTime: str | None = None,
                 numScenesMatched: str | None = None,
                 resultCode: str | None = None,
                 runScriptOutput: str | None = None,
                 runSummary: str | None = None,
                 runOptions: RunOptions | None = None,
                 datasets: str | None = None,
                 catalogId: str | None = None,
                 lastRunDate: str | None = None,
                 orderIds: str | None = None,
                 bulkIds: str | None = None):
        self.runId = runId
        self.subscriptionId = subscriptionId
        self.runDate = runDate
        self.executionTime = executionTime
        self.numScenesMatched = numScenesMatched
        self.resultCode = resultCode
        self.runScriptOutput = runScriptOutput
        self.runSummary = runSummary
        self.runOptions = runOptions
        self.datasets = datasets
        self.catalogId = catalogId
        self.lastRunDate = lastRunDate
        self.orderIds = orderIds
        self.bulkIds = bulkIds

        self.dict = self._as_dict()


class SubscriptionDataset(AbstractDataType):
    """
    :param datasetName: (string) Dataset name
    """

    def __init__(self, datasetName: str | None = None):
        self.datasetName = datasetName

        self.dict = self._as_dict()


class TramOrder(AbstractDataType):
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

    def __init__(self,
                 orderId: int | None = None,
                 username: str | None = None,
                 processingPriority: int | None = None,
                 orderComment: str | None = None,
                 statusCode: str | None = None,
                 statusCodeText: str | None = None,
                 dateEntered: str | None = None,
                 lastUpdatedDate: str | None = None):
        self.orderId = orderId
        self.username = username
        self.processingPriority = processingPriority
        self.orderComment = orderComment
        self.statusCode = statusCode
        self.statusCodeText = statusCodeText
        self.dateEntered = dateEntered
        self.lastUpdatedDate = lastUpdatedDate

        self.dict = self._as_dict()


class TramUnit(AbstractDataType):
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

    def __init__(self,
                 unitNumber: int | None = None,
                 productCode: str | None = None,
                 productName: str | None = None,
                 datasetId: str | None = None,
                 datasetName: str | None = None,
                 collectionName: str | None = None,
                 orderingId: str | None = None,
                 unitPrice: str | None = None,
                 unitComment: str | None = None,
                 statusCode: str | None = None,
                 statusCodeText: str | None = None,
                 lastUpdatedDate: str | None = None):
        self.unitNumber = unitNumber
        self.productCode = productCode
        self.productName = productName
        self.datasetId = datasetId
        self.datasetName = datasetName
        self.collectionName = collectionName
        self.orderingId = orderingId
        self.unitPrice = unitPrice
        self.unitComment = unitComment
        self.statusCode = statusCode
        self.statusCodeText = statusCodeText
        self.lastUpdatedDate = lastUpdatedDate

        self.dict = self._as_dict()
