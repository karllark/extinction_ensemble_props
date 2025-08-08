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

VCG04: `Valencic, Clayton, & Gordon 2014, 616, 912
<https://ui.adsabs.harvard.edu/abs/2004ApJ...616..912V>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["VCG04"], "AV", fit=True)
    plot_1d_dist(ax[1], ["VCG04"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

FM07: `Fitzpatrick & Massa 2007, ApJ, 663, 320
<https://ui.adsabs.harvard.edu/abs/2007ApJ...663..320F>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["FM07"], "AV", fit=True)
    plot_1d_dist(ax[1], ["FM07"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

GCC09: `Gordon, Cartledge, & Clayton 2009, ApJ, 705, 1320
<https://ui.adsabs.harvard.edu/abs/2009ApJ...705.1320G>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["GCC09"], "AV", fit=True)
    plot_1d_dist(ax[1], ["GCC09"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

Large Magellanic Cloud
----------------------

G03_lmc: `Gordon et al. 2003, ApJ, 594, 279
<https://ui.adsabs.harvard.edu/abs/2003ApJ...594..279G>`_G03: `Gordon et al. 2003, ApJ, 594, 279
<https://ui.adsabs.harvard.edu/abs/2003ApJ...594..279G>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["G03_lmc"], "AV", fit=True)
    plot_1d_dist(ax[1], ["G03_lmc"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

Small Magellanic Cloud
----------------------

G03_smc: `Gordon et al. 2003, ApJ, 594, 279
<https://ui.adsabs.harvard.edu/abs/2003ApJ...594..279G>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["G03_smc"], "AV", fit=True)
    plot_1d_dist(ax[1], ["G03_smc"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

G24_smc: `Gordon et al. 2024, ApJ, 970, 51
<https://ui.adsabs.harvard.edu/abs/2024ApJ...970...51G>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["G24_smc"], "AV", fit=True)
    plot_1d_dist(ax[1], ["G24_smc"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

M31
---

C15_m31: `Clayton et al. 2015, ApJ, 815, 14
<https://scixplorer.org/abs/2015ApJ...815...14C/abstract>`_

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["C15_m31"], "AV", fit=True)
    plot_1d_dist(ax[1], ["C15_m31"], "RV", fit=True)

    fig.tight_layout()
    plt.show()


C25_m31: Clayton et al. 2025, ApJ, in press

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["C25_m31"], "AV", fit=True)
    plot_1d_dist(ax[1], ["C25_m31"], "RV", fit=True)

    fig.tight_layout()
    plt.show()


G25_m33: Gordon et al. 2025, ApJ, submitted

.. plot::

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fontsize = 20
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(nrows=2, figsize=fsize)

    plot_1d_dist(ax[0], ["G25_m33"], "AV", fit=True)
    plot_1d_dist(ax[1], ["G25_m33"], "RV", fit=True)

    fig.tight_layout()
    plt.show()

======
Custom
======

Custom datasets can be added by constructing and adding a compatible data file to the `data` subdirectory
and adding the sample name to the `ptypes` dictionary in `helpers.py`.  The `ptypes` dictionary is used
for the plot symbol, color, and legend label for each sample. 

Please consider opening a pull request to the repository with datasets that would be useful to others.