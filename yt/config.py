from glue.core import Data, Component
from glue.config import data_factory
from glue.core.data_factories import data_label

from yt.mods import load


class YtComponent(Component):
    def __init__(self, ds, field, shape):
        self._ds = ds
        self._dd = ds.h.all_data()
        self._field = field
        self._shape = shape
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self._dd[self._field]
        return self._data

    @property
    def shape(self):
        return self._shape

    @property
    def __getitem__(self, key):
        return self.data[key]

    @property
    def numeric(self):
        return True


@data_factory('yt data', lambda x, **kwargs: False)
def yt_data(path):
    """Use yt to load a gridded dataset

    This function will extract all particle and field datasets
    (excluding derived datasets) from a file. Currently,
    you cannot make images from this data.

    The resulting Field dataset refers to the highest-resolution
    subgrids

    Paramters
    ---------
    path : str
           Path to file to load. This is what get's passed to yt.mods.load()

    Returns
    -------
    One or two Glue data objects
    """
    ds = load(path)
    dd = ds.h.all_data()

    particles = [f for f in ds.h.field_list if ds.field_info[f].particle_type]
    fields = [f for f in ds.h.field_list if not ds.field_info[f].particle_type]

    lbl = data_label(path)

    result = []
    if len(particles) > 0:
        d1 = Data(label=lbl + "_particle")
        shp = dd[particles[0]].shape
        for p in particles:
            d1.add_component(YtComponent(ds, p, shp), p)
        result.append(d1)

    if len(fields) > 0:
        d2 = Data(label=lbl + "_field")
        shp = dd[fields[0]].shape
        for f in fields:
            d2.add_component(YtComponent(ds, f, shp), f)
        result.append(d2)

    return result
