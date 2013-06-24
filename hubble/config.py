from glue.core import Data
from glue.core.coordinates import coordinates_from_wcs
from glue.config import data_factory

import pyfits as fits
from stwcs.wcsutil import HSTWCS


@data_factory('Hubble Image', '*.fits *.fit', default='fits fit')
def hubble_data(filename):
    """
    Data loader customized for 'typical' hubble fits files

    This function extracts groups of (SCI, ERR, and DQ) extensions
    from a file. Each is retuned as a glue Data object

    HSTWCS objects are used to parse wcs.

    Any other extensions are ignored
    """
    #assumption: relevant SCI/ERR/DQ arrays are
    #grouped together, with SCI component first

    result = []

    hdulist = fits.open(filename, memmap=True)

    label = filename.split('.')[0]
    label = label.split('/')[-1].split('\\')[-1]
    index = 0

    def _get_sci_group(i, index):
        d = Data("%s_%i" % (label, index))
        d.coords = coordinates_from_wcs(HSTWCS(hdulist, i))

        index = index + 1
        d.add_component(hdulist[i].data, hdulist[i].name)
        for h in hdulist[i:]:
            if h.name  == 'SCI':
                break  # new science grp
            if h.name not in ['ERR', 'DQ']:
                continue
            d.add_component(h.data, h.name)
        return d

    for i, h in enumerate(hdulist):
        if h.name != 'SCI':
            continue
        result.append(_get_sci_group(i, index))
        index += 1

    return result
