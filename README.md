## Glue Data Loaders

This repository contains several examples of writing custom
data loaders in Glue.

The basic process for writing custom data loaders is described
in the [Glue documentation](http://www.glueviz.org/en/latest/customization.html#custom-data-loaders). The basic strategy is as follows:

 1. Write a function that takes a path as an input, and returns one or more Glue data objects as output
 1. Wrap this function in the `@data_factory` decorator, which adds the function to the Glue UI
 1. Put this code in a `config.py` file, which Glue runs on startup.
