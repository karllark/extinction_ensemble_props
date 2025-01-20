.. _datasets:

########
Datasets
########

========
Included
========

There are a number of datasets available in this package.  These are results from the literature
and can be combined together in any of the possible plots.  

Milky Way
---------

Large Magellanic Cloud
----------------------

Small Magellanic Cloud
----------------------

======
Custom
======

Custom datasets can be added by constructing and adding a compatible data file to the `data` subdirectory
and adding the sample name to the `ptypes` dictionary in `helpers.py`.  The `ptypes` dictionary is used
for the plot symbol, color, and legend label for each sample. 

Please consider opening a pull request to the repository with datasets that would be useful to others.