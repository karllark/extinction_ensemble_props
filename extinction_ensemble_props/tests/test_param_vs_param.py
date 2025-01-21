import matplotlib.pyplot as plt

from extinction_ensemble_props.plot_param_vs_param import plot_param_vs_param


def test_param_vs_param():
    """
    Simple test if a plot is generated.
    """

    fsize = (12, 8)
    fig, ax = plt.subplots(figsize=fsize)

    plot_param_vs_param(ax, ["GCC09"], "AV", "C2")
