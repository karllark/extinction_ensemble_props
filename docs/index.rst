.. extinction_ensemble_props documentation master file, created by
   sphinx-quickstart on Mon Dec 23 14:13:44 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Extinction Ensemble Properties
==============================

``extinction_ensemble_props`` is a python package to make plots of the ensemble 
properties of extinction curves.  The goal of this package is to provide a
straightforward way to plot the properties of different samples of extinction curves 
either alone or one property versus another one.  This can be helpful for investigating
correlations and how difference samples vary (e.g., between different galaxies).

Extinction describes the effects of dust on observations of single star due to
the dust along the line-of-sight to a star removing flux by absorbing photons
and scattering photons out of the line-of-sight. The wavelength dependence of
dust extinction (also know as extinction curves) provides fundamental
information about the size, composition, and shape of interstellar dust grain.
In general, extinction models are used to model or correct the effects of dust
on observations.

The properties of dust extinction curves includes measurements of the dust (and gas)
columns (e.g., A(V), R(V), N(H)/A(V)) and parameters that describe the shape of the
extinction curve (.e.g, FM90 parameters [C1, C2, B3, ...]).

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Datasets <datasets.rst>
   Plotting 1D distributions <plot_1d.rst>
   Plotting parameter versus parameter <plot_param_vs_param.rst>

Installation
============

.. toctree::
  :maxdepth: 2

  How to install <install.rst>

Reporting Issues
================

If you have found a bug in ``extinction_ensemble_props`` please report it by creating a
new issue on the ``extinction_ensemble_props`` `GitHub issue tracker
<https://github.com/karllark/extinction_ensemble_props/issues>`_.

Please include an example that demonstrates the issue sufficiently so that the
developers can reproduce and fix the problem. You may also be asked to provide
information about your operating system and a full Python stack trace.  The
developers will walk you through obtaining a stack trace if it is necessary.

Contributing
============

Like the `Astropy`_ project, ``extinction_ensemble_props`` is made both by and for its
users.  We accept contributions at all levels, spanning the gamut from fixing a
typo in the documentation to developing a major new feature. We welcome
contributors who will abide by the `Python Software Foundation Code of Conduct
<https://www.python.org/psf/conduct/>`_.

``extinction_ensemble_props`` follows the same workflow and coding guidelines as
`Astropy`_.  Take a look at the astropy 
`developer <https://docs.astropy.org/en/latest/index_dev.html>`_ documentation for
guidelines.

For the complete list of contributors please see the `extinction_ensemble_props
contributors page on Github
<https://github.com/karllark/extinction_ensemble_props/graphs/contributors>`_.

Reference API
=============

.. toctree::
   :maxdepth: 2

   reference_api.rst