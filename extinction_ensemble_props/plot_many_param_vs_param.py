import argparse
import numpy as np
import matplotlib.pyplot as plt

from extinction_ensemble_props.plot_param_vs_param import plot_param_vs_param
from extinction_ensemble_props.helpers import ptypes

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
    parser.add_argument("--sprops", help="sample properties", action="store_true")
    parser.add_argument(
        "--spropsebv", help="sample properties versus ebv", action="store_true"
    )
    parser.add_argument(
        "--spropsav", help="sample properties versus av", action="store_true"
    )
    parser.add_argument(
        "--gdprops", help="N(HI)/E(B-V) properties", action="store_true"
    )
    parser.add_argument(
        "--fm90main", help="only plot the main FM90 parameters", action="store_true"
    )
    parser.add_argument(
        "--fm90main_noc1", help="only plot the main FM90 parameters (Av vs Rv instead of C1 vs C2)",
        action="store_true"
    )
    parser.add_argument(
        "--fm90_noc1", help="plot FM90 parameters (Av vs Rv instead of C1 vs C2)",
        action="store_true"
    )
    parser.add_argument("--ebv", help="plot FM90 versus E(B-V)", action="store_true")
    parser.add_argument("--av", help="plot FM90 versus A(V)", action="store_true")
    parser.add_argument("--nhi", help="plot FM90 versus N(HI)", action="store_true")
    parser.add_argument("--rv", help="plot FM90 versus R(V)", action="store_true")
    parser.add_argument("--irv", help="plot FM90 versus 1/R(V)", action="store_true")
    parser.add_argument("--nouncs", help="do not plot uncs", action="store_true")
    parser.add_argument("--fit", help="Fit lines for some plots", action="store_true")
    parser.add_argument("--paper", help="portrait format", action="store_true")
    parser.add_argument("--png", help="save figure as a png file", action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file", action="store_true")
    args = parser.parse_args()

    if args.paper:
        fsize = (12, 14)
        nrows = 3
        ncols = 2
        pi = [0, 1, 2, 3, 4, 5]
    else:
        fsize = (18, 10)
        nrows = 2
        ncols = 3
        pi = [0, 1, 3, 4, 2, 5]

    # default values
    yptags = ["C1", "C2", "B3", "C4", "x0", "gamma"]
    fitlines = [False] * (nrows * ncols)
    show_gd = None
    if args.sprops:
        ostr = "sprops"
        fsize = (12, 10)
        nrows = 2
        ncols = 2
        pi = [0, 1, 2, 3]
        xptags = ["EBV", "AV", "EBV", "AV"]
        yptags = ["RV", "RV", "NHI_EBV", "NHI_AV"]
    elif args.spropsebv:
        ostr = "sprops_ebv"
        fsize = (14, 6)
        nrows = 1
        ncols = 2
        pi = [0, 1]
        xptags = ["EBV", "EBV"]
        yptags = ["RV", "NHI"]
        show_gd = [False, True]
    elif args.spropsav:
        ostr = "sprops_av"
        fsize = (14, 6)
        nrows = 1
        ncols = 2
        pi = [0, 1]
        xptags = ["AV", "AV"]
        yptags = ["RV", "NHI"]
        show_gd = [False, True]
    elif args.gdprops:
        ostr = "gdprops"
        nrows = 2
        ncols = 3
        xptags = ["AV", "C2", "B3", "C4", "gamma", "x0"]
        yptags = ["NHI_AV", "NHI_AV", "NHI_AV", "NHI_AV", "NHI_AV", "NHI_AV"]
        fitlines = [False, True, True, True, True, True]
    elif args.ebv:
        ostr = "ebv"
        npts = len(yptags)
        xptags = ["EBV"] * npts
    elif args.av:
        ostr = "av"
        npts = len(yptags)
        xptags = ["AV"] * npts
    elif args.nhi:
        ostr = "nhi"
        npts = len(yptags)
        xptags = ["NHI"] * npts
    elif args.rv:
        ostr = "rv"
        npts = len(yptags)
        xptags = ["RV"] * npts
    elif args.irv:
        ostr = "irv"
        npts = len(yptags)
        xptags = ["IRV"] * npts
    elif args.fm90main:
        ostr = "fm90main"
        fsize = (12, 10)
        nrows = 2
        ncols = 2
        pi = [0, 1, 2, 3]
        fitlines = [True] * nrows * ncols
        xptags = ["C2", "C2", "C2", "C4"]
        yptags = ["C1", "B3", "C4", "B3"]
    elif args.fm90main_noc1:
        ostr = "fm90main_noc1"
        fsize = (12, 10)
        nrows = 2
        ncols = 2
        pi = [0, 1, 2, 3]
        fitlines = [True] * nrows * ncols
        xptags = ["AV", "C2", "C2", "C4"]
        yptags = ["RV", "B3", "C4", "B3"]
    elif args.fm90_noc1:
        ostr = "fm90_noc1"
        xptags = ["AV", "C2", "C2", "C4", "gamma", "gamma"]
        yptags = ["RV", "B3", "C4", "B3", "B3", "x0"]
    else:  # plot fm90 vs fm90
        ostr = "fm90"
        xptags = ["C2", "C2", "C2", "C2", "gamma", "gamma"]
        yptags = ["C1", "B3", "C4", "x0", "B3", "x0"]

    # make the plots
    fontsize = 14
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=fsize)

    for i in range(nrows * ncols):
        if (nrows == 1) | (ncols == 1):
            tax = ax[i]
        else:
            px, py = divmod(pi[i], ncols)
            tax = ax[px, py]

        plot_param_vs_param(
            tax,
            args.datasets,
            xptags[i],
            yptags[i],
            fit=fitlines[i] & args.fit,
            nouncs=args.nouncs,
        )

        if i != 0:
            tax.get_legend().remove()

    fig.tight_layout()

    fname = f"ensemble_{ostr}_vs_fm90_params"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
