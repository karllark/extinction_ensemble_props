import importlib.resources as importlib_resources
import numpy as np
from astropy.table import QTable

__all__ = ["poss_params", "param_labels", "ptypes", "get_dataset"]

# possible parameters
# fmt: off
poss_params = ["AV", "EBV", "RV", "IRV", "NHI", "NHI_EBV", "NHI_AV",
               "C1", "C2", "C3", "B3", "C4", "x0", "gamma"]
# fmt: on

# parameter labels
param_labels = {
    "EBV": "$E(B-V)$",
    "AV": "$A(V)$",
    "RV": "$R(V)$",
    "IRV": "1/$R(V)$",
    "NHI": "$N(HI)$ [$10^{21}~H~cm^{-2}$]",
    "NHI_EBV": "$N(HI)/E(B-V)$ [$10^{21}~H~cm^{-2}~mag^{-1}$]",
    "NHI_AV": "$N(HI)/A(V)$ [$10^{21}~H~cm^{-2}~H~cm^{-2}~mag^{-1}$]",
    "C1": "$C_1$ = UV intercept",
    "C2": "$C_2$ = UV slope",
    "B3": "$B_3$ = bump amplitude",
    "C4": "$C_4$ = FUV rise amplitude",
    "x0": "$x_o$ = bump center",
    "gamma": r"$\gamma$ = bump width",
}

# plot types, colors, alphas, and legend names
ptypes = {
    "VCG04": ("k.", 0.25, "MW: VCG04"),
    "G03_smc": ("m<", 0.5, "SMC: G03"),
    "G03_lmc": (("tab:orange", ">"), 0.5, "LMC: G03"),
    "FM07": ("k+", 0.5, "MW: FM07"),
    "GCC09": ("kD", 0.5, "MW: GCC09"),
    "G24_smc": ("b>", 0.5, "SMC: G24"),
    "G24_smc_nobump": ("bo", 0.5, "SMC: Weak/absent 2175 A bump"),
    "G24_smc_bump": ("rP", 0.5, "SMC: Significant 2175 A bump"),
    "G24_smc_flat": ("cs", 0.5, "SMC: Flat"),
    "C25_m31": ("rs", 0.75, "M31: C25"),
    "G25_wisci": ("bo", 0.5, "MW: G25 WISCI"),
}

# ptypes = {
#     "G03_lmc": (("tab:orange", ">"), 0.1, "LMC: G03"),
#     "GCC09": ("kD", 0.1, "MW: GCC09"),
#     "G24_smc": ("b<", 0.1, "SMC: G24"),
#     "C25_m31": ("rs", 0.75, "M31"),
#     "C25_m31_blue": ("bs", 0.75, "M31: Blue"),
#     "C25_m31_green": ("go", 0.75, "M31: Green"),
#     "C25_m31_red": ("rD", 0.75, "M31: Red"),
#     "C25_m31_black": ("kv", 0.75, "M31: Black"),
# }

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

    if "IRV" not in tdata.colnames:
        tdata["IRV"] = 1.0 / tdata["RV"]
        tdata["IRV_unc"] = tdata["IRV"] * tdata["RV_unc"] / tdata["RV"]

    # divide by 10^21 to make easier to undertand and fit numbers
    if "NHI" in tdata.colnames:
        tdata["NHI"] /= 1e21
        tdata["NHI_unc"] /= 1e21

    if ("NHI" in tdata.colnames) & ("NHI_EBV" not in tdata.colnames):
        tdata["NHI_EBV"] = tdata["NHI"] / tdata["EBV"]
        tdata["NHI_EBV_unc"] = (tdata["NHI_unc"] / tdata["NHI"]) ** 2 + (
            tdata["EBV_unc"] / tdata["EBV"]
        ) ** 2
        tdata["NHI_EBV_unc"] = tdata["NHI_EBV"] * np.sqrt(tdata["NHI_EBV_unc"])

    if ("NHI" in tdata.colnames) & ("NHI_AV" not in tdata.colnames):
        tdata["NHI_AV"] = tdata["NHI"] / tdata["AV"]
        tdata["NHI_AV_unc"] = (tdata["NHI_unc"] / tdata["NHI"]) ** 2 + (
            tdata["AV_unc"] / tdata["AV"]
        ) ** 2
        tdata["NHI_AV_unc"] = tdata["NHI_AV"] * np.sqrt(tdata["NHI_AV_unc"])

    return tdata
