import matplotlib.pyplot as plt

from extinction_ensemble_props.plot_1d_distributions import plot_1d_dist


def test_1d_dist():
    """
    Simple test if a plot is generated.
    """

    fsize = (12, 8)
    fig, ax = plt.subplots(figsize=fsize)

    plot_1d_dist(ax, ["gor09"], "C2")
