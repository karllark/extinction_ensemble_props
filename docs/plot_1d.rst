#####################
Plot 1D Distributions
#####################

.. plot::
   :include-source:

    import matplotlib.pyplot as plt
    from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist

    fsize = (12, 8)
    fig, ax = plt.subplots(figsize=fsize)
    fontsize = 14
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    plot_1d_dist(ax, ["gor09"], "B3")

    fig.tight_layout()
    plt.show()