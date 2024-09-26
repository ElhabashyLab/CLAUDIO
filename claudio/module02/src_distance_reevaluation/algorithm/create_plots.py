import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def create_histogram(data: pd.DataFrame, filename: str, output_directory: str, linker_minimum: float, linker_maximum: float,
                      add_labels=False):
    """
    Create histogram plots with matplotlib

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    output:directory : str,
    linker_minimum : float,
    linker_maximum : float,
    add_labels : bool

    Returns
    -------
        None    
    """

    # normal distance histograms
    dist_data = data[["eucl_dist", "topo_dist"]].copy()
    labels = ["euclidean distance", "topological distance"]
    bins = [x * 5 for x in range(16)]
    colors = ["#9ACE9A", "#464444"]
    bin_centers = np.diff(bins) * .5 + bins[:-1]
    dist_data[dist_data > 70] = 70
    plt.figure(figsize=(6.5, 6), constrained_layout=True)
    if add_labels:
        known_xy = []
    for col, label, color in zip(dist_data.columns, labels, colors):
        freq, _, _ = plt.hist(dist_data[[col]], bins=bins, alpha=.7, color=color,
                              label=f"{label} (n={len(dist_data[~pd.isna(dist_data[col])].index)})")
        if add_labels:
            for fr, x in zip(freq, bin_centers):
                height = int(fr)
                y = height
                if x in [val for val, _ in known_xy]:
                    known_y = known_xy[[val for val, _ in known_xy].index(x)][1]
                    rad = int(round(max(int(f) for f in freq) / 40) + 1)
                    if y in range(known_y-rad, known_y+rad+1) and y != known_y:
                        y = known_y - rad if y <= known_y else known_y + rad
                plt.annotate(str(height) if height > 0 else '', xy=(x, y), xytext=(0, .2), textcoords="offset points",
                             ha="center", va="bottom")
                known_xy.append((x, y))
    plt.axvline(linker_minimum, color="darkred", linestyle="dashed", linewidth=1)
    plt.axvline(linker_maximum, color="darkred", linestyle="dashed", linewidth=1)
    if add_labels:
        plt.text(linker_minimum + 1, plt.ylim()[1] * 0.85, f"Linker\nminimum: {linker_minimum}", color="darkred")
        plt.text(linker_maximum + 1, plt.ylim()[1] * 0.85, f"Linker\nmaximum: {linker_maximum}", color="darkred")
    plt.xlabel(f"distance " + r"[$\AA$]")
    plt.ylabel("frequency")
    x_labels = [str(x) for x in bins]
    x_labels[-1] = str(float("inf"))
    plt.xticks(bins, x_labels)
    plt.legend()
    plt.title("Frequency of structural crosslink distances")
    plt.savefig(f"{output_directory}{filename}_hist_unfiltered.png")

    # Clear figure
    plt.clf()

    # pdb method histogram
    method_data = data[["pdb_id", "pdb_method"]].copy()
    method_data = method_data.groupby("pdb_id").apply(lambda x: x.iloc[0])
    method_data = method_data.pdb_method.astype(str)
    labels = ["selected structure"]
    label_dict = {x: i for i, x in enumerate(sorted(pd.unique(method_data.values.ravel('K'))))}
    bins = list(range(len(label_dict) + 1))
    bin_centers = np.diff(bins) * .5 + bins[:-1]
    plt.figure(figsize=(6.5, 6), constrained_layout=True)
    freq, _, _ = plt.hist(method_data.map(label_dict), bins=bins, color=colors[0], label=f"{labels[0]}")
    if add_labels:
        known_xy = []
        for fr, x in zip(freq, bin_centers):
            height = int(fr)
            y = height
            if x in [val for val, _ in known_xy]:
                known_y = known_xy[[val for val, _ in known_xy].index(x)][1]
                rad = int(round(max(int(f) for f in freq) / 40) + 1)
                if y in range(known_y - rad, known_y + rad + 1) and y != known_y:
                    y = known_y - rad if y <= known_y else known_y + rad
            plt.annotate(str(height) if height > 0 else '', xy=(x, y), xytext=(0, .2),
                         textcoords="offset points", ha="center", va="bottom")
            known_xy.append((x, y))
    plt.xlabel(f"pdb experimental method")
    plt.ylabel("frequency")
    x_labels = [x.replace(' ', '\n') if x != "nan" else "unknown"
                for x in sorted(pd.unique(method_data.values.ravel('K')))]
    x_labels = [x if x != '-' else "not found" for x in x_labels]
    plt.xticks(bin_centers, x_labels, rotation=45)
    plt.legend()
    plt.title("Frequency of experimental methods of structures")
    plt.savefig(f"{output_directory}{filename}_pdb_exp.png")

    # Clear figure
    plt.clf()

    # pdb resolution histogram
    res_data = data[["pdb_id", "pdb_resolution"]].copy()
    res_data = res_data.groupby("pdb_id").apply(lambda x: x.iloc[0])
    labels = ["selected structure"]
    res_data[res_data == "ALPHAFOLD"] = -1
    res_data[res_data == '-'] = -2

    resolutions = []
    for res in res_data.pdb_resolution:
        try:
            resolutions.append(float(res))
        except ValueError:
            resolutions.append(-2)
    res_data = pd.Series(resolutions)

    res_data[res_data > 13] = 14
    bins = [x - 2 for x in range(18)]
    bin_centers = np.diff(bins) * .5 + bins[:-1]
    plt.figure(figsize=(6.5, 6), constrained_layout=True)
    freq, _, _ = plt.hist(res_data, bins=bins, color=colors[0], label=f"{labels[0]}")
    if add_labels:
        known_xy = []
        for fr, x in zip(freq, bin_centers):
            height = int(fr)
            y = height
            if x in [val for val, _ in known_xy]:
                known_y = known_xy[[val for val, _ in known_xy].index(x)][1]
                rad = int(round(max(int(f) for f in freq) / 40) + 1)
                if y in range(known_y-rad, known_y+rad+1) and y != known_y:
                    y = known_y - rad if y <= known_y else known_y + rad
            plt.annotate(str(height) if height > 0 else '', xy=(x, y), xytext=(0, .2),
                         textcoords="offset points", ha="center", va="bottom")
            known_xy.append((x, y))
    plt.xlabel(f"pdb resolution")
    plt.ylabel("frequency")
    x_labels = [f"[{x},{x+1})" if x != bins[-2] else f"[{x},{x+1}]" for x in bins[:-1]]
    x_labels[1] = "ALPHA-\nFOLD"
    x_labels[0] = "not\nfound"
    plt.xticks(bin_centers, x_labels, rotation=45, fontsize=8)
    plt.legend()
    plt.title("Frequency of structure resolutions")
    plt.savefig(f"{output_directory}{filename}_pdb_res.png")
