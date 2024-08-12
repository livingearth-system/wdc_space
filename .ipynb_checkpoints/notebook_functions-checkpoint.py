"""
Living Wales Common Functions

File containing common functions and definitions for use in notebooks

Author: Dan Clewley
"""

import numpy as np
import pandas as pd
import matplotlib.colors as colors


def stat_summary(xarr, scheme):
    """
    A function to perform summary statistics on an xarray object and return as a pandas
    dataframe.
    """
    # Search habitat types in farm
    farm_types = np.unique(xarr, return_counts=True)

    # Create dictionary to store outputs. Will convert this to a pandas data frame
    out_stat_dict = {"CATEGORY": [], "HECTARE": []}

    for color, label in scheme.items():
        if (label[0] in farm_types[0]) & (label[0] != 0):
            out_stat_dict["CATEGORY"].append(label[1])
            area_ha = (farm_types[1][list(farm_types[0]).index(label[0])] * 100) / 10000
            out_stat_dict["HECTARE"].append(area_ha)

    # Convert to a pandas dataframe
    out_stat_df = pd.DataFrame.from_dict(out_stat_dict)

    # Calculate percentage
    out_stat_df["PERCENT"] = 100 * out_stat_df["HECTARE"] / out_stat_df["HECTARE"].sum()
    return out_stat_df


# Level3plus colour scheme
level3plus_scheme = {
    "#FFFFFF": [0.0, "Not classified"],
    "#D1E133": [111.0, "Cultivated or managed terrestrial vegetation"],
    "#007A02": [113.0, "Semi-natural terrestrial woody vegetation"],
    "#95c748": [114.0, "Semi-natural terrestrial herbaceous vegetation"],
    "#4EEEE8": [123.0, "Cultivated or managed aquatic vegetation"],
    "#02C077": [124.0, "Semi-natural aquatic vegetation"],
    "#DA5C69": [215.0, "Artificial surface"],
    "#F3AB69": [216.0, "Bare surface"],
    "#4D9FDC": [220.0, "Water"],
}


def get_level3plus_cmap():
    return colors.ListedColormap(list(level3plus_scheme.keys()))


def get_level3plus_norm():
    return colors.BoundaryNorm([value[0] for value in level3plus_scheme.values()], 9)


# Habitat colour scheme
broadhabitat_scheme = {
    "#FFFFFF": [0.0, "Not classified"],
    "#00C502": [1.0, "Broadleaved Woodland"],
    "#006902": [2.0, "Needle-leaved Woodland"],
    "#CEF191": [3.0, "Semi-natural Grassland"],
    "#C91FCC": [4.0, "Heathland and Scrub"],
    "#F2A008": [5.0, "Bracken"],
    "#F8F8C9": [6.0, "Bog"],
    "#177E88": [7.0, "Fen/Marsh/Swamp"],
    "#FFFF00": [8.0, "Cultivated or managed vegetation"],
    "#00DDA4": [9.0, "Coastal habitat"],
    "#0E00ED": [10.0, "Open Water"],
    "#908E8D": [11.0, "Natural Bare Surfaces"],
    "#000000": [12.0, "Artificial Bare Surfaces"],
    "#DAC654": [13.0, "Young trees/Felled/Coppice"],
    "#5d994e": [14.0, "Woodland and scrub"],
}


def get_broadhabitat_cmap():
    return colors.ListedColormap(list(broadhabitat_scheme.keys()))


def get_broadhabitat_norm():
    return colors.BoundaryNorm([value[0] for value in broadhabitat_scheme.values()], 15)


# detailed habitat colour scheme
detailedhabitat_scheme = {
    "#45fb82": [3, "Semi-natural Grassland"],
    "#577117": [4, "Juncus Rushes"],
    "#cef191": [5, "Molinia Grassland"],
    "#efe67e": [9, "Young Plantations"],
    "#399c4f": [10, "Woodland and Scrub"],
    "#0ac72d": [12, "Broadleaved Woodland"],
    "#286b35": [16, "Needle-leaved Woodland"],
    "#6d5742": [23, "Ulex Dominated Scrub"],
    "#d7d236": [35, "Acid Grassland"],
    "#c5d833": [38, "Neutral Grassland"],
    "#c3c000": [41, "Calcareous Grassland"],
    "#fced13": [44, "Improved Grassland"],
    "#518388": [45, "Marsh/Marshy Grassland"],
    "#f37e1c": [50, "Bracken"],
    "#9c0f85": [58, "Dry Dwarf Shrub Heath"],
    "#e2a7ed": [61, "Wet Dwarf Shrub Heath"],
    "#df0f4a": [70, "Blanket Bog"],
    "#f74428": [71, "Raised Bog"],
    "#f7eebb": [72, "Modified Bog"],
    "#6bdac2": [78, "Fen"],
    "#000000": [85, "Peat (bare)"],
    "#4eb0e0": [86, "Swamp"],
    "#013ff6": [90, "Open water"],
    "#a5ffdc": [106, "Intertidal vegetation"],
    "#3b4b61": [107, "Intertidal bare surfaces"],
    "#4de5fc": [119, "Saltmarsh"],
    "#ecb641": [128, "Open dune"],
    "#30aa87": [130, "Dune grassland"],
    "#6e1ae3": [131, "Dune heath"],
    "#7c3843": [132, "Dune scrub"],
    "#7286bb": [134, "Maritime cliff and slope (unvegetated)"],
    "#5a5860": [135, "Maritime cliff and slope (vegetated)"],
    "#020b09": [142, "Natural rock exposure and waste"],
    "#c6c3d3": [143, "Inland cliff"],
    "#e7ebeb": [155, "Quarry"],
    "#fb9a71": [159, "Arable crops"],
    "#ddf0f1": [200, "Artificial bare surfaces"],
    "#a0ada9": [201, "Natural bare surfaces"],
    "#8cbd77": [202, "Semi-natural herbaceous vegetation (other)"],
}


def get_detailedhabitat_cmap():
    return colors.ListedColormap(list(detailedhabitat_scheme.keys()))


def get_detailedhabitat_norm():
    return colors.BoundaryNorm(
        [value[0] for value in detailedhabitat_scheme.values()], 203
    )


# Water persistence colour scheme
waterper_scheme = {
    "#FFFFFF": [0.0, "Not affected"],
    "#0a549e": [1.0, "9+ months"],
    "#2172b6": [2.0, "8 months"],
    "#3e8ec4": [3.0, "7 months"],
    "#60a6d2": [4.0, "6 months"],
    "#89bfdd": [5.0, "5 months"],
    "#b0d2e8": [6.0, "4 months"],
    "#cde0f2": [7.0, "3 months"],
    "#cde0f2": [8.0, "2 months"],
    "#e8f2fb": [9.0, "1 month"],
}


def get_waterper_cmap():
    return colors.ListedColormap(list(waterper_scheme.keys()))


def get_waterper_norm():
    return colors.BoundaryNorm([value[0] for value in waterper_scheme.values()], 11)
