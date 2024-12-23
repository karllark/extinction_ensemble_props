import argparse
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import QTable
from astropy.modeling import models, fitting


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasets",
        help="give the datasets to plot",
        nargs="+",
        default=["gor09", "gor03_lmc", "gor24_smc"],
        choices=["val04", "gor03_smc", "gor03_lmc", "fit07", "gor09", "gor24_smc"],
    )
    parser.add_argument(
        "--param",
        help="Parameter to use",
        default="B3",
        choices=["C1", "C2", "C3", "B3", "C4", "x0", "gamma", "RV"],
    )
    parser.add_argument("--png", help="save figure as a png file", action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file", action="store_true")
    args = parser.parse_args()

    # plot types, colors and alphas
    ptypes = {
        "val04": ("k.", 0.25, "MW: VCG04"),
        "gor03_smc": ("m<", 0.5, "SMC: G03"),
        "gor03_lmc": (("tab:orange", ">"), 0.5, "LMC: G03"),
        "fit07": ("k+", 0.5, "MW: FM07"),
        "gor09": ("kD", 0.75, "MW: GCC09"),
        "gor24_smc": ("b>", 0.5, "SMC: G24"),
        "gor24_smc_nobump": ("bo", 0.5, "SMC: Weak/absent 2175 A bump"),
        "gor24_smc_bump": ("rP", 0.5, "SMC: Significant 2175 A bump"),
        "gor24_smc_flat": ("cs", 0.5, "SMC: Flat"),
        "gor24_smc_lowebv": (
            ("tab:brown", "v"),
            0.5,
            r"SMC: $E(B-V)_\mathrm{SMC} < 0.1$",
        ),
    }

    fsize = (12, 8)
    fig, ax = plt.subplots(figsize=fsize)
    fontsize = 14
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=2)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    for cset in args.datasets:
        ptype, palpha, clabel = ptypes[cset]

        fname = f"data/{cset}_ensemble_params.dat"
        tdata = QTable.read(fname, format="ascii.ipac")

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

        medval = np.median(tdata[args.param])
        if hasattr(medval, "value"):
            medval = medval.value

        hinfo = ax.hist(
            tdata[args.param], bins=20, color=ptype[0], label=clabel, alpha=palpha
        )
        y = hinfo[0]
        x = hinfo[1]
        x = 0.5 * (x[0:-1] + x[1:])

        g_init = models.Gaussian1D(amplitude=50.0, mean=medval, stddev=1.0)
        fit_g = fitting.TRFLSQFitter()
        g = fit_g(g_init, x, y, maxiter=100000)
        ax.plot(
            x,
            g(x),
            label=rf"{clabel} model (m={g.mean.value:.3f}, $\sigma$={g.stddev.value:.3f})",
        )

    ax.set_xlabel(args.param)
    ax.set_ylabel("#")

    ax.legend()

    fig.tight_layout()

    fname = f"distributions_1d_{args.param}"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
