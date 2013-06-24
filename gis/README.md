# GIS files

This directory implements basic parsing of TIFF world files (.tfw) and
GIS SHP files. TIFF world files attach world coordinate metadata to
TIFF images, which Glue can use to convert between pixel and world
coordinates. SHP files are spatially-referenced catalogs.

## DEMO
Take a look at the data John Snow collected during the 1864 Cholera London epidemic (for more details, see [this blog post](http://blog.rtwilson.com/john-snows-famous-cholera-analysis-data-in-modern-gis-formats/)).

```
curl -sLo SnowGIS.zip http://www.rtwilson.com/downloads/SnowGIS_v2.zip
unzip SnowGIS.zip
glue SnowGIS/*shp SnowGIS/*tif
```