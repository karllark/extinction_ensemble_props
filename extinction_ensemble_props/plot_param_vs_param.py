import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
from astropy.modeling import models, fitting
from astropy.stats import sigma_clip

from extinction_ensemble_props.utils.fit_full2dcor import lnlike_correlated
from extinction_ensemble_props.helpers import (
    poss_params,
    param_labels,
    ptypes,
    get_dataset,
)

__all__ = ["plot_param_vs_param"]


def plot_param_vs_param(ax, datasets, xparam, yparam, fit=False, nouncs=False):
    """
    Plot xparam versus yparam for the specific datasets.

    Parameters
    ----------
    ax : matplottlib.axes
        matplotlib axes object for the plot

    datasets : list
        list of the datasets to plot

    xparam : string
        name of the parameter to be plot on the x-axis

    yparam : string
        name of the parameter to be plot on the y-axis

    fit : boolean
        set to fit a lines [default=False]
    """

    for cname in datasets:
        cdata = get_dataset(cname)

        ptype, palpha, plabel = ptypes[cname]

        xdata = cdata[xparam].data
        ydata = cdata[yparam].data

        # check if uncertainties are included
        if f"{xparam}_unc" in cdata.colnames:
            xdata_unc = cdata[f"{xparam}_unc"].data
        else:
            xdata_unc = None
        if f"{yparam}_unc" in cdata.colnames:
            ydata_unc = cdata[f"{yparam}_unc"].data
        else:
            ydata_unc = None

        if nouncs & (len(cdata[xparam]) > 50):
            xdata_unc = None
            ydata_unc = None

        colstr = ptype[0]
        symstr = ptype[1]

        ax.errorbar(
            xdata,
            ydata,
            xerr=xdata_unc,
            yerr=ydata_unc,
            color=colstr,
            marker=symstr,
            linestyle="",
            label=plabel,
            alpha=palpha,
        )

    if xparam in ["NHI_EBV", "NHI_AV"]:
        ax.set_xscale("log")
    if yparam in ["NHI_EBV", "NHI_AV"]:
        ax.set_yscale("log")

    ax.set_xlabel(param_labels[xparam])
    ax.set_ylabel(param_labels[yparam])

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
        "--xparam",
        help="Parameter for x-axis",
        default="B3",
        choices=poss_params,
    )
    parser.add_argument(
        "--yparam",
        help="Parameter for y-axis",
        default="C2",
        choices=poss_params,
    )
    parser.add_argument(
        "--nouncs",
        help="do not plot uncs for datasets with >50 samples",
        action="store_true",
    )
    parser.add_argument("--fit", help="Fit lines for some plots", action="store_true")
    parser.add_argument("--png", help="save figure as a png file", action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file", action="store_true")
    args = parser.parse_args()

    # make the plots
    fontsize = 14
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fig, ax = plt.subplots(figsize=(12, 8))

    plot_param_vs_param(ax, args.datasets, args.xparam, args.yparam, fit=args.fit, nouncs=args.nouncs)

    fig.tight_layout()

    fname = f"ensemble_{args.xparam}_vs_{args.yparam}_params"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
