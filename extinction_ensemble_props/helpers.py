import importlib.resources as importlib_resources
import numpy as np
from astropy.table import QTable

__all__ = ["poss_params", "param_labels", "ptypes", "get_dataset"]

# possible parameters
# fmt: off
poss_params = ["AV", "EBV", "RV", "IRV", "NHI", "NHI_EBV", "NHI_AV",
               "C1", "C2", "C3", "B3", "C4", "x0",
               "C1_AV", "C2_AV", "C3_AV", "B3_AV", "C4_AV",
               "gamma", "metallicity"]
# fmt: on

# parameter labels
param_labels = {
    "EBV": "$E(B-V)$ [mag]",
    "AV": "$A(V)$ [mag]",
    "RV": "$R(V)$",
    "IRV": "1/$R(V)$",
    "NHI": r"$N(HI)$ [$10^{21}~H~cm^{-2}$]",
    "NHI_EBV": r"$N(HI)/E(B-V)$ [$10^{21}~H~cm^{-2}~mag^{-1}$]",
    "NHI_AV": r"$N(HI)/A(V)$ [$10^{21}~H~cm^{-2}~mag^{-1}$]",
    "C1": "$C_1$ = UV intercept / $E(B-V)$",
    "C1_AV": "$C_1$ = UV intercept / $A(V)$",
    "C2": "$C_2$ = UV slope / $E(B-V)$",
    "C2_AV": "$C_2$ = UV slope / $A(V)$",
    "B3": "$B_3$ = bump amplitude / $E(B-V)$",
    "B3_AV": r"$B_3^{A(V)}$ = bump amplitude / $A(V)$",
    "C4": "$C_4$ = FUV rise amplitude / $E(B-V)$",
    "C4_AV": "$C_4$ = FUV rise amplitude / $A(V)$",
    "x0": r"$x_o$ = bump center [$\mu \mathrm{m}^{-1}$]",
    "gamma": r"$\gamma$ = bump width [$\mu \mathrm{m}^{-1}$]",
    "metallicity": r"Z/Z$_\odot$",
}

# plot types, colors, alphas, and legend names
basealpha = 0.5
ptypes = {
    "VCG04": ("k.", basealpha, "MW: VCG04"),
    "G03_smc": ("m<", basealpha, "SMC: G03"),
    "G03_lmc": (("tab:orange", ">"), basealpha, "LMC: G03"),
    "G03_lmc_ave": (("tab:orange", ">"), basealpha, "LMC Avg: G03"),
    "G03_lmc_lmc2": ("cs", basealpha, "LMC LMC2/30Dor: G03"),
    "FM07": ("k+", basealpha, "MW: FM07"),
    "GCC09": ("kD", basealpha, "MW: GCC09"),
    "C15_m31": (("tab:purple", "<"), basealpha, "M31: C15"),
    "G24_smc": ("b^", basealpha, "SMC: G24"),
    "G24_smc_nobump": ("bo", basealpha, "SMC: Weak/absent 2175 A bump"),
    "G24_smc_bump": ("rP", basealpha, "SMC: Significant 2175 A bump"),
    "G24_smc_flat": ("cs", basealpha, "SMC: G24 Flat"),
    "C25_m31": ("go", basealpha, "M31: C25"),
    "G26_m33": ("rD", basealpha, "M33: G26"),
    "G25_wisci": ("bo", basealpha, "MW: G25 WISCI"),
}


def _div_frac_unc(tdata, x, y):
    """
    Fractional uncertainty of x/y
    """
    frac_unc = np.zeros(len(tdata))
    gvals = (tdata[x] != 0.0) & (tdata[y] != 0.0)
    frac_unc[gvals] = (tdata[f"{x}_unc"][gvals] / tdata[x][gvals]) ** 2 + (
        tdata[f"{y}_unc"][gvals] / tdata[y][gvals]
    ) ** 2
    return np.sqrt(frac_unc)


def get_dataset(cset):
    """
    Get the data for a specific dataset.
    Generate some data based on data provided (e.g., inverse R(V))

    Parameters
    ----------
    cset : string
        string designating a dataset (e.g., VCG04)

    Returns
    -------
    tdata : astropy QTable
        table of the data for the specified dataset

    """
    ref = importlib_resources.files("extinction_ensemble_props") / "data"
    with importlib_resources.as_file(ref) as data_path:
        tdata = QTable.read(
            f"{data_path}/{cset}_ensemble_params.dat", format="ascii.ipac"
        )

    # add EBV is not present and AV, RV are present
    if (
        ("AV" in tdata.colnames)
        & ("RV" in tdata.colnames)
        & ("EBV" not in tdata.colnames)
    ):
        tdata["EBV"] = tdata["AV"] / tdata["RV"]
        tdata["EBV_unc"] = tdata["EBV"] * _div_frac_unc(tdata, "AV", "RV")

    if "IRV" not in tdata.colnames:
        tdata["IRV"] = 1.0 / tdata["RV"]
        tdata["IRV_unc"] = tdata["IRV"] * tdata["RV_unc"] / tdata["RV"]

    # now add data if missing and derivable from expected columns
    if "B3" not in tdata.colnames:
        tdata["B3"] = tdata["C3"] / (tdata["gamma"] ** 2)
        if "C3_unc" in tdata.colnames:
            tdata["B3_unc"] = np.absolute(tdata["B3"]) * np.sqrt(
                tdata["C3_unc"] ** 2 + 2.0 * (tdata["gamma_unc"].value ** 2)
            )
            # temp fix until LMC and MW GCC09 can be refit with B3
            # C3 and gamma strongly correlated
            tdata["B3_unc"] *= 0.2

    # add in FM90 parameters normalized by AV instead of EBV if not present
    # check only for B3 and assume the rest will be there
    # see Gordon et al. 2009 for the equations converting standard FM90
    #    parameters to normalized by A(V) versions
    if (
        ("B3" in tdata.colnames)
        & ("RV" in tdata.colnames)
        & ("B3_AV" not in tdata.colnames)
    ):
        if "C1" in tdata.colnames:
            tdata["C1_AV"] = tdata["C1"] / tdata["RV"] + 1.0
            tdata["C1_AV_unc"] = np.absolute(
                tdata["C1_AV"] * _div_frac_unc(tdata, "C1", "RV")
            )
        tdata["C2_AV"] = tdata["C2"] / tdata["RV"]
        tdata["C2_AV_unc"] = np.absolute(
            tdata["C2_AV"] * _div_frac_unc(tdata, "C2", "RV")
        )
        if "C3" in tdata.colnames:
            tdata["C3_AV"] = tdata["C3"] / tdata["RV"]
            tdata["C3_AV_unc"] = np.absolute(
                tdata["C3_AV"] * _div_frac_unc(tdata, "C3", "RV")
            )
        tdata["B3_AV"] = tdata["B3"] / tdata["RV"]
        tdata["B3_AV_unc"] = np.absolute(
            tdata["B3_AV"] * _div_frac_unc(tdata, "B3", "RV")
        )
        tdata["C4_AV"] = tdata["C4"] / tdata["RV"]
        tdata["C4_AV_unc"] = np.absolute(
            tdata["C4_AV"] * _div_frac_unc(tdata, "C4", "RV")
        )

    # divide by 10^21 to make easier to understand and fit numbers
    if "NHI" in tdata.colnames:
        tdata["NHI"] /= 1e21
        tdata["NHI_unc"] /= 1e21

    # add NHI_EBV
    if (
        ("NHI" in tdata.colnames)
        & ("EBV" in tdata.colnames)
        & ("NHI_EBV" not in tdata.colnames)
    ):
        tdata["NHI_EBV"] = tdata["NHI"] / tdata["EBV"]
        tdata["NHI_EBV_unc"] = tdata["NHI_EBV"] * _div_frac_unc(tdata, "NHI", "EBV")

    # add NHI_AV
    if (
        ("NHI" in tdata.colnames)
        & ("AV" in tdata.colnames)
        & ("NHI_AV" not in tdata.colnames)
    ):
        tdata["NHI_AV"] = tdata["NHI"] / tdata["AV"].value
        tdata["NHI_AV_unc"] = tdata["NHI_AV"] * _div_frac_unc(tdata, "NHI", "AV")

    return tdata
