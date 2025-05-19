import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
from astropy.modeling import models, fitting

from extinction_ensemble_props.utils.fit_full2dcor import lnlike_correlated
from extinction_ensemble_props.helpers import (
    poss_params,
    param_labels,
    ptypes,
    get_dataset,
)

__all__ = ["plot_param_vs_param"]


def plot_param_vs_param(
    ax,
    datasets,
    xparam,
    yparam,
    fit=False,
    nouncs=False,
    showstats=False,
    show_gd=False,
    fontsize=16,
):
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

    nouncs : boolean
        set to not show error bars if sample size is >50 [default=False]

    fit : boolean
        set to fit a line [default=False]

    showstats : boolean
        print the statistics for each dataset [default=False]

    show_gd : boolean
        set to show the gas-to-dust ratio if xparam/yparam are appropriate [default=False]
    """

    # for fitting
    xvals = []
    xvals_unc = []
    yvals = []
    yvals_unc = []
    # ebv = []
    # ebv_unc = []

    for cname in datasets:
        cdata = get_dataset(cname)

        if xparam not in list(cdata.colnames):
            raise ValueError(f"xparam {xparam} not present in {cname} dataset.")
        if yparam not in list(cdata.colnames):
            raise ValueError(f"yparam {yparam} not present in {cname} dataset.")

        # for fitting with covariances
        # ebv = np.concatenate((ebv, cdata["EBV"].data))
        # ebv_unc = np.concatenate((ebv_unc, cdata["EBV_unc"].data))

        ptype, palpha, plabel = ptypes[cname]

        xdata = np.array(cdata[xparam].data)
        ydata = np.array(cdata[yparam].data)

        # for fitting
        xvals = np.concatenate((xvals, xdata))
        yvals = np.concatenate((yvals, ydata))

        # if both zero, then not good data
        gvals = (xdata != 0.0) & (ydata != 0.0)

        # check if uncertainties are included
        if f"{xparam}_unc" in cdata.colnames:
            xdata_unc = np.array(cdata[f"{xparam}_unc"].data)[gvals]
            # for fitting
            xvals_unc = np.concatenate((xvals_unc, xdata_unc))
        else:
            xdata_unc = None
        if f"{yparam}_unc" in cdata.colnames:
            ydata_unc = np.array(cdata[f"{yparam}_unc"].data)[gvals]
            # for fitting
            yvals_unc = np.concatenate((yvals_unc, ydata_unc))
        else:
            ydata_unc = None

        if nouncs & (len(cdata[xparam]) > 50):
            xdata_unc = None
            ydata_unc = None

        colstr = ptype[0]
        symstr = ptype[1]

        ax.errorbar(
            xdata[gvals],
            ydata[gvals],
            xerr=xdata_unc,
            yerr=ydata_unc,
            color=colstr,
            marker=symstr,
            linestyle="",
            label=plabel,
            alpha=palpha,
        )

        summarystats = {}
        if showstats:
            print(f"Summary statistics for {cname}")
        for ccol in cdata.colnames:
            if ("name" not in ccol.lower()) & ("unc" not in ccol.lower()):
                ave = np.average(cdata[ccol].data)
                std = np.std(cdata[ccol].data)
                summarystats[ccol] = (
                    ave,
                    std,
                    std / np.sqrt(len(cdata[ccol].data)),
                )
                if showstats:
                    print(f"{ccol}: ave = {ave} +/- {std}")

        # special code to fit for the gas-to-dust ratio
        if (xparam in ["EBV", "AV"]) & (yparam == "NHI") & (show_gd is not None):

            if show_gd & (len(xdata) > 10):
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                x = np.arange(0.0, xlim[1], 0.01)
                gdratio = summarystats[f"NHI_{xparam}"][0]
                gdratio_unc = summarystats[f"NHI_{xparam}"][2]
                line_orig = models.Linear1D(slope=gdratio, intercept=0.0)
                tlabel = (
                    rf"$N(HI)/{param_labels[xparam]} = {gdratio:.2f} \pm {gdratio_unc:.2f}$"
                    + ": {clabel}"
                )
                ax.plot(
                    x,
                    line_orig(x),
                    linestyle=":",
                    label=tlabel,
                    color=colstr,
                )
                ax.legend(fontsize=0.7 * fontsize, loc="upper right")

    if fit:
        # fit a line using standard minimizer to get good initial fit
        line_orig = models.Linear1D(slope=-10.0, intercept=20.0)
        fit = fitting.LinearLSQFitter()
        fitted_line = fit(line_orig, xvals, yvals, weights=1.0 / yvals_unc)
        nparams = fitted_line.parameters

        # now take into account x *and* y uncertainties (and covariance [to be added])
        # uses a numerical integration technique (see Gordon et al. 2023)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x = np.arange(xlim[0], xlim[1], 0.01)
        dxlim = xlim[1] - xlim[0]
        intinfo = [xlim[0] - dxlim, xlim[1] + dxlim, dxlim / 20]

        def nll(*args):
            return -lnlike_correlated(*args)

        npts = len(xvals)
        covs = np.zeros((npts, 2, 2))

        # needed for fitting
        # covtags = ["C1", "C2", "B3", "C4"]
        for k in range(npts):
            # if (xptags[i] in covtags) & (yptags[i] in covtags):
            #    # approximation following Gordon et al. (2023)
            #    cov_xy = xvals[k] * yvals[k] * ((ebv_unc[k] / ebv[k]) ** 2)
            #    corr_xy = np.min([cov_xy / (xvals_unc[k] * yvals_unc[k]), 0.99])
            #    cov_xy *= xvals_unc[k] * yvals_unc[k]
            # else:
            #    cov_xy = 0.0
            cov_xy = 0.0
            covs[k, 0, 0] = xvals_unc[k] ** 2
            covs[k, 0, 1] = cov_xy
            covs[k, 1, 0] = cov_xy
            covs[k, 1, 1] = yvals_unc[k] ** 2

        result = op.minimize(
            nll,
            fitted_line.parameters,
            args=(yvals, fitted_line, covs, intinfo, xvals),
        )
        nparams = result["x"]
        fitted_line = models.Linear1D(slope=nparams[0], intercept=nparams[1])
        ax.plot(
            x,
            fitted_line(x),
            "k--",
            label=f"Fit: {nparams[1]:.2f} + {nparams[0]:.2f}x",
        )

        ax.set_ylim(ylim)

    if xparam in ["NHI_EBV", "NHI_AV"]:
        ax.set_xscale("log")
    if yparam in ["NHI_EBV", "NHI_AV"]:
        ax.set_yscale("log")

    ax.set_xlabel(param_labels[xparam])
    ax.set_ylabel(param_labels[yparam])

    ax.legend(fontsize=0.7 * fontsize)


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
    parser.add_argument(
        "--showstats",
        help="Print the summary statistics for each dataset",
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

    plot_param_vs_param(
        ax,
        args.datasets,
        args.xparam,
        args.yparam,
        fit=args.fit,
        nouncs=args.nouncs,
        showstats=args.showstats,
    )

    fig.tight_layout()

    fname = f"ensemble_{args.xparam}_vs_{args.yparam}_params"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
