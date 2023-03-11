import os
import requests
import logging
from datetime import datetime
from tqdm import tqdm
from usgsDataTypes import usgsDataTypes
from usgsMethods import usgsMethods


class otherMethods:
    """
    Implementation date: 18.03.2021

    Other methods not related to Official USGS/EROS Inventory Service Documentation (Machine-to-Machine API).
    Other methods is purposed to handle stuff like data download.
    """

    @classmethod
    def download(cls, api, datasetName, entityIds, productName, output_dir):
        """
         Perform scene search and download.

        :param api: Instance of usgsMethods()
        :param datasetName:
        :param entityIds:
        :param productName:
        :param output_dir:
        :return:
        """
        downloadOptions = api.downloadOptions(datasetName=datasetName, entityIds=entityIds)
        datasetId, productId = None, None

        for downloadOption in downloadOptions['data']:
            if downloadOption['productName'] == productName:
                datasetId = downloadOption['datasetId']
                productId = downloadOption['id']
                break
        if (datasetId, productId) == (None, None):
            logging.error(f"{datetime.now()} Can't find productName={productName} in datasetName={datasetName}")

        download = usgsDataTypes.DownloadInput(entityId=entityIds, productId=productId, dataUse=None, label=None)
        downloadRequest = api.downloadRequest(downloads=[download])

        if downloadRequest['data']['failed'] != []:
            logging.warning(f'{datetime.now()} downloadRequest failed see respond:\n{downloadRequest}')

        availableDownloads = downloadRequest['data']['availableDownloads'] + \
                             downloadRequest['data']['preparingDownloads']
        results_list = []
        for availableDownload in availableDownloads:
            url = availableDownload['url']
            if (productName.find('Bundle') == -1):
                path = cls._download(url, output_dir)
            else: 
                path = cls._download(url, output_dir, bundle_dict={'name': url[url.find("product_id=") + len("product_id="):url.find("product_id=") + len("product_id=") + 38]})
            results_list.append(path)
        return results_list

    @classmethod
    def _download(cls, url, output_dir, chunk_size=1024, timeout=60, bundle_dict=None):
        """
        :param url:
        :param output_dir:
        :param chunk_size:
        :return: file_path: (str) - if successful, None - if interrupted, 'Skip' - if landsat file is offline,
        """
        headers = requests.head(url, allow_redirects=True).headers
        if cls.is_downloadable(headers):
            expected_file_size = int(headers['content-length']) 
            file_name = "" 
            if bundle_dict: 
                file_name = bundle_dict['name'] + ".tar"
            else: 
                file_name = headers['content-disposition'].split('"')[1]
            file_path = os.path.join(output_dir, file_name)

            with requests.get(url, stream=True, allow_redirects=True, timeout=timeout) as r:
                with tqdm(desc="Downloading", total=expected_file_size, unit_scale=True, unit='B') as progressbar:
                    print(file_path)
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                progressbar.update(len(chunk))
                                f.write(chunk)
                
                if not bundle_dict: 
                    if cls.is_download_complete(expected_file_size, file_path):
                        return file_path
                    else:
                        # Check if the interrupted download can be continued.
                        if cls.is_accept_ranges(headers):
                            print('Hey, they added support for the `Accept-Ranges` header! ',
                                'Implement a method to recover interrupted downloads!', sep='\n')
                            # TODO If it is possible to continue downloading, do not delete the file, but try to continue the interrupted download.
                            os.remove(file_path)
                        else:
                            os.remove(file_path)
                else: 
                    return file_path


        return None

    @classmethod
    def is_download_complete(cls, expected_file_size, file_path):
        """Compares the size of the downloaded file on your hard drive with the expected file size.
        :param expected_file_size: (int) Expected file size
        :param file_path: (str) File path
        :return: (boolean)
        """
        if os.path.isfile(file_path):
            actual_file_size = os.path.getsize(file_path)
            print(actual_file_size)
            if expected_file_size == actual_file_size:
                return True
        return False

    @classmethod
    def is_downloadable(cls, headers):
        """
        Checks if content-type header is a downloadable resource
        :param headers: (dict) Headers returned from requests.head()
        :return: (boolean)
        """
        content_type = headers['content-type']
        if 'text' in content_type.lower():
            return False

        elif 'html' in content_type.lower():
            return False

        return True

    @classmethod
    def is_accept_ranges(cls, headers):
        """
        Checks if `Accept-Ranges` header is supported
        :param headers: (dict) Headers returned from requests.head()
        :return: (boolean)
        """
        content_type = headers['Accept-Ranges']
        if 'bytes' in content_type.lower():
            return True

        return False

    @classmethod
    def request_filesize(cls, api, datasetName, productName, entityId):
        """
        Checks file size of the scene.
        :param api: (usgsMethods)  Instance of usgsMethods()
        :param datasetName: (str) In example: 'LANDSAT_8_C1'
        :param productName: (str) In example: 'Level-1 GeoTIFF Data Product'
        :param entityId: (str) entityId
        :return: (int) Product file size
        """
        downloadOptions = api.downloadOptions(datasetName=datasetName, entityIds=entityId)
        if downloadOptions['data'] is None:
            print(f"Error: Can't request file size. downloadOptions['data'] is {downloadOptions['data']}")
            return None
        for downloadOption in downloadOptions['data']:
            if productName == downloadOption['productName']:
                file_size = int(downloadOption['filesize'])
                return file_size
