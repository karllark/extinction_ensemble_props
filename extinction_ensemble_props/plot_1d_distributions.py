import importlib.resources as importlib_resources

import argparse
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import QTable
from astropy.modeling import models, fitting

from extinction_ensemble_props.helpers import ptypes

__all__ = ["plot_1d_dist"]


def plot_1d_dist(ax, datasets, param, fit=False):
    """
    Plot the 1D distribution of a a single dust property.
    Multiple datasets can be plotted together.
    Optionally, include a Gaussian fit to the distribution of each dataset.

    Parameters
    ----------
    ax : matplottlib.axes
        matplotlib axes object for the plot

    datasets : list
        list of the datasets to plot

    param : string
        name of the parameter to be plot

    fit : boolean
        set to fit a Gaussian to the distribution [default=False]
    """
    ref = importlib_resources.files("extinction_ensemble_props") / "data"

    for cset in datasets:
        ptype, palpha, clabel = ptypes[cset]

        with importlib_resources.as_file(ref) as data_path:
            tdata = QTable.read(
                f"{data_path}/{cset}_ensemble_params.dat", format="ascii.ipac"
            )

        # now add data if missing and derivable from expected columns
        if "B3" not in tdata.colnames:
            tdata["B3"] = tdata["C3"] / (tdata["gamma"].value ** 2)
            if "C3_unc" in tdata.colnames:
                tdata["B3_unc"] = np.absolute(tdata["B3"]) * np.sqrt(
                    tdata["C3_unc"] ** 2 + 2.0 * (tdata["gamma_unc"].value ** 2)
                )
            # temp fix until LMC and MW GCC09 can be refit with B3
            # C3 and gamma strongly correlated
            tdata["B3_unc"] *= 0.2

        medval = np.median(tdata[param])
        if hasattr(medval, "value"):
            medval = medval.value

        hinfo = ax.hist(
            tdata[param], bins=20, color=ptype[0], label=clabel, alpha=palpha
        )
        y = hinfo[0]
        x = hinfo[1]
        x = 0.5 * (x[0:-1] + x[1:])

        if fit:
            g_init = models.Gaussian1D(amplitude=50.0, mean=medval, stddev=1.0)
            fit_g = fitting.TRFLSQFitter()
            g = fit_g(g_init, x, y, maxiter=100000)
            ax.plot(
                x,
                g(x),
                label=rf"{clabel} model (m={g.mean.value:.3f}, $\sigma$={g.stddev.value:.3f})",
                color=ptype[0],
                alpha=palpha,
            )

    ax.set_xlabel(param)
    ax.set_ylabel("#")

    ax.legend()


if __name__ == "__main__":

    pdatasets = np.sort(list(ptypes.keys()))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasets",
        help="give the datasets to plot",
        nargs="+",
        default=["GCC09", "G03_lmc", "G24_smc"],
        choices=pdatasets,
    )
    parser.add_argument(
        "--param",
        help="Parameter to use",
        default="B3",
        choices=["C1", "C2", "C3", "B3", "C4", "x0", "gamma", "RV", "AV", "EBV"],
    )
    parser.add_argument(
        "--fit",
        help="include Gaussian fit to each dataset distribution",
        action="store_true",
    )
    parser.add_argument("--png", help="save figure as a png file", action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file", action="store_true")
    args = parser.parse_args()

    fontsize = 18
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fsize = (12, 8)
    fig, ax = plt.subplots(figsize=fsize)

    plot_1d_dist(ax, args.datasets, args.param, fit=args.fit)
    ax.legend(fontsize=0.7 * fontsize)

    fig.tight_layout()

    fname = f"distributions_1d_{args.param}"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
