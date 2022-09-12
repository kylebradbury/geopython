#!/usr/bin/env python
# coding: utf-8

# # Earth Engine for gathering data
# 
# Google Earth Engine is a powerful tool for geospatial data analysis. Here, we will discuss how to use its Python API for gathering data from Landsat, Sentinel, and NAIP imagery.
# 
# To start off with, request access to Google Earth Engine at: [](https://earthengine.google.com/). This may take some time. Once approved, install the Python API and get credentials for using the API following [these instructions](https://developers.google.com/earth-engine/guides/python_install-conda#mac_6). Be sure to try out the test code they suggest to make sure Earth Engine is running successfully):

# In[1]:


import ee

# Initialize the Earth Engine module.
ee.Initialize()

# Print metadata for a DEM dataset.
print(ee.Image('USGS/SRTMGL1_003').getInfo())


# In[22]:


import json
print(json.dumps(ee.Image('USGS/SRTMGL1_003').getInfo(), indent=3, sort_keys=True))


# If the above code yields output, you'll know you're ready for to go!
# 
# ## Selecting imagery
# 
# 

# In[2]:


from geetools import batch

def download_NAIP_toLocal(bbox, name, scale=1):
    """
    downloads NAIP imagery from the specified bounding box and saves it as `name`
    """
    AOI = ee.Geometry.Rectangle(list(bbox), "EPSG:4326", False)

    collection = (
        ee.ImageCollection("USDA/NAIP/DOQQ")
        .filterDate("2010-01-01", "2019-01-01")
        .filterBounds(AOI)
        .select(['R', 'G', 'B'])
    )

    image = ee.Image(collection.mosaic()).clip(AOI)
    batch.image.toLocal(image, name, scale=scale, region=AOI)

lat = [35.998708946524324, 36.003257110633896]
lon = [-78.94764325291365, -78.9412917819664]
bbox = [lon[0], lat[0], lon[1], lat[1]]
name = 'naipsample'
download_NAIP_toLocal(bbox, name, scale=1)


# In[3]:


# Unzip the files
import zipfile
path_to_zip_file = 'naipsample.zip'
directory_to_extract_to = 'naipsample'
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)


# In[4]:


# Combine the files:
import rasterio

def stack_bands(name, outname):
    file_list = [name + '.R.tif', name + '.G.tif', name + '.B.tif']

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count = len(file_list))

    # Read each layer and write it to stack
    with rasterio.open(outname, 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))

outname = "stacked_sample.tif"
stack_bands('naipsample/download',outname)


# In[5]:


# Plot the example
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import matplotlib.pyplot as plt
from rasterio.plot import show

fig, ax = plt.subplots(num='main', figsize=(6,6))

from rasterio.plot import show
data = rasterio.open(outname)
show(data.read([1,2,3]).astype('float')/255, transform=data.transform, ax=ax)


# In[6]:


from geetools import batch

def download_S2_toLocal(bbox, name, scale=1):
    """
    downloads Sentinel 2 imagery from the specified bounding box and saves it as `name`
    """
    AOI = ee.Geometry.Rectangle(list(bbox), "EPSG:4326", False)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterDate('2020-01-01', '2020-01-30')
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
        .filterBounds(AOI)
        .select(['B4', 'B3', 'B2'])
    )

    image = ee.Image(collection.mosaic()).clip(AOI)
    batch.image.toLocal(image, name, scale=scale, region=AOI)

lat = [35.998708946524324, 36.003257110633896]
lon = [-78.94764325291365, -78.9412917819664]
bbox = [lon[0], lat[0], lon[1], lat[1]]
name = 's2sample'
download_S2_toLocal(bbox, name, scale=1)


# In[7]:


import zipfile
path_to_zip_file = 's2sample.zip'
directory_to_extract_to = 's2sample'
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)


# In[8]:


import rasterio

def stack_bands_s2(name, outname):
    file_list = [name + '.B4.tif', name + '.B3.tif', name + '.B2.tif']

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count = len(file_list))

    # Read each layer and write it to stack
    with rasterio.open(outname, 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))

outname = "stacked_s2_sample.tif"
stack_bands_s2('s2sample/download',outname)


# In[9]:


# Plot the example
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import matplotlib.pyplot as plt
from rasterio.plot import show

fig, ax = plt.subplots(num='main', figsize=(6,6))

from rasterio.plot import show
data = rasterio.open(outname)
show(data.read([1,2,3]).astype('float')/4096, transform=data.transform, ax=ax)
# show(data.read([1,2,3]).astype('float')/255, transform=data.transform, ax=ax)


# In[10]:


from geetools import batch

lat = [35.998708946524324, 36.003257110633896]
lon = [-78.94764325291365, -78.9412917819664]
bbox = [lon[0], lat[0], lon[1], lat[1]]
name = 's2sample'


# In[11]:



AOI = ee.Geometry.Rectangle(list(bbox), "EPSG:4326", False)


# In[12]:



collection = ee.ImageCollection("COPERNICUS/S2_SR").filterDate("2010-01-01", "2019-01-01").filterBounds(AOI).select(['B4', 'B3', 'B2'])


# In[14]:


collection


# In[15]:


image = ee.Image(collection.mosaic()).clip(AOI)
# batch.image.toLocal(image, name, scale=scale, region=AOI)

