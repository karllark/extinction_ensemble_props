################
1D Distributions
################

The datasets that can be plotted are given in :ref:`datasets`.

====
Code
====

A plot of the 1D distribution for a single parameter for single dataset can be done using the code below.
This shows an example for the VCG04 sample of Milky Way sightlines for the FM90 parameter B3.

.. plot::
   :include-source:

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
    fig, ax = plt.subplots(figsize=fsize)

    plot_1d_dist(ax, ["VCG04"], "B3")

    fig.tight_layout()
    plt.show()

This shows an example for the VCG04, FM07, and GCC09 samples of Milky Way sightlines for the FM90 parameter C2.

.. plot::
   :include-source:

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
    fig, ax = plt.subplots(figsize=fsize)

    plot_1d_dist(ax, ["VCG04", "FM07", "GCC09"], "C3")

    fig.tight_layout()
    plt.show()

===========
Commandline
===========

1D distributions can be plotted using `plot_1d_dist`.  This can be run from the command line with::

   python plot_1d_dist.py

Options can be determined by appending `--help` to the call.



