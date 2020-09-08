'''
main file to execute the data extraction

'''
import InputDataExtraction
import ProjectLogger
import shapely.geometry
import os
# from osgeo import ogr
import fiona
import geopandas as gpd
from pprint import pprint as pp
import ee
import ee.mapclient
from datetime import datetime as dt
from IPython.display import Image, display
import requests

'''
Challenge is to convert from NAD83->EPSG:3310 coordinate system from arcgis 
to EPSG:4326 which is the standard GPS and geojson coordinate system

'''

if __name__ == "__main__":
    # Setup the logger for the file.
    # Check ProjectLogger.py for info on logger level number to use as parameter
    log = ProjectLogger.setup_logging(os.path.basename(__file__), 0)
    #test log message
    log.warning('Setup logger for the file is done!')
    ###############################
    # geopandas option
    #######################
    gdb_file = "Data/SNMMPC_v2.gdb/SNMMPC_v2.gdb"
    df = gpd.read_file(gdb_file)
    df = df.to_crs("EPSG:4326")
    pp(df.head)


    ######################################
    # Initialize the Earth Engine module.
    #####################################
    service_account = 'william-baron@cmpe-295-catching-meadows.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, 'keys/cmpe-295-catching-meadows-e4ec6e04fa8e.json')
    ee.Initialize(credentials)
    ###########################################################
    landsat = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
    test_image = ee.Geometry.MultiPolygon(list(df["geometry"][0][0].exterior.coords))
    lansat_test_image = landsat.filterBounds(test_image)
    landsat = landsat.filterDate('2019-07-01', '2019-12-01')
    lansat_test_image.getInfo()
    lansat_test_image.first().bandNames().getInfo()
    lansat_test_image.first().bandNames()
    first_image = ee.Image(lansat_test_image.sort('CLOUD_COVER').first())
    parameters = {'min': 0,
                  'max': 1000,
                  'dimensions': 512,
                  'bands': ['B4', 'B3', 'B2'],
                   'region': test_image}
    path = first_image.getThumbURL(parameters)
    print(path)
    img_data = requests.get(path).content
    with open('_image_overlays/test_image.jpg', 'wb') as handler:
        handler.write(img_data)
