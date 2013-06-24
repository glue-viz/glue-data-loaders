# Hubble FITS files

`hubble_data` is a custom data loader for 'typical' FITS files
from the Hubble Space Telescope. It scans FITS files for
groups of SCI, ERR and DQ extensions, and constructs
a Glue data object from each.

Furthermore, it uses the STScI `wcsutil` library for
parsing Hubble's particular flavor of WCS metadata.

## Demo

```
curl -Lso o63401030_flt.fits https://www.dropbox.com/s/ke1y3huwq10m9rl/o63401030_flt.fits
glue o63401030_flt.fits
```
