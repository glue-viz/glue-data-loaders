import os
from collections import defaultdict

from PIL import Image
from astropy.wcs import WCS
import numpy as np
import shapefile

from glue.core.coordinates import coordinates_from_wcs
from glue.config import data_factory
from glue.core import Data
from glue.core.data_factories import has_extension

def tfw_to_coords(filename, shp):
    """ Use a TIFF world file to build Glue Coordinates """
    with open(filename) as hfile:
        hdr = hfile.read().splitlines()
    hdr = map(float, hdr)
    hdr = dict(CD1_1=hdr[0],
               CD1_2=hdr[1] * (-1),
               CD2_1=hdr[2],
               CD2_2=hdr[3] * (-1),
               CRVAL1=hdr[4],
               CRVAL2=hdr[5],
               CRPIX1=0,
               CRPIX2=shp[0])
    wcs = WCS(hdr)
    return coordinates_from_wcs(wcs)


@data_factory('GIS TIFF', has_extension('tiff tif'), default='tif')
def read_tiff_metadata(filename):
    """ Read a TIFF image, looking for .tfw metadata """
    base, ext = os.path.splitext(filename)
    data = np.flipud(np.array(Image.open(filename).convert('L')))

    result = Data()

    if os.path.exists(base + '.tfw'):
        result.coords = tfw_to_coords(base + '.tfw', data.shape)

    result.add_component(data, 'map')
    return result


@data_factory('GIS Shapefile', has_extension('shx shp dbf'),
              default='shx shp dbf')
def read_shp(filename):
    """ Read a GIS set of .shx, .shp, .dbf files """
    rec = shapefile.Reader(filename)
    result = Data()
    fields = defaultdict(list)

    for sr in rec.shapeRecords():
        #reduce each shapefile to the mean position
        x, y = zip(*sr.shape.points)
        fields['x'].append(sum(x) / len(x))
        fields['y'].append(sum(y) / len(y))

        for key, val in zip(rec.fields[1:], sr.record):
            fields[key[0]].append(val)

    result = Data(**fields)
    return result
