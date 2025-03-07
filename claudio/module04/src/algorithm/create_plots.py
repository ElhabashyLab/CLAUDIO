import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_plots(data: pd.DataFrame, filename: str, cutoff: float, 
                 compute_scoring: bool, output_directory: str, 
                 linker_minimum: float, linker_maximum: float,
                 add_labels=False):
    """
    create histograms for inter scores, and pie charts for final 
    validation results

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    cutoff : float
    compute_scoring : bool,
    output_directory : str,
    linker_minimum : float,
    linker_maximum : float,
    add_labels : bool

    Returns
    -------
        None
    """

    colors = ["#9ACE9A", "#464444"]
    if compute_scoring:
        inter_data = data[(data.inter_score > cutoff) 
                          & (data.unip_id_a == data.unip_id_b)][["inter_score"]]
        if not inter_data.empty:
            label = "experimental confidence score for intra crosslinks (" \
                    + "$n_{>cutoff}$" + f" = {sum(inter_data.inter_score > cutoff)})"
            bins = np.array(list(range(11))) * .1
            bin_centers = np.diff(bins) * .5 + bins[:-1]
            plt.figure(figsize=(6.5, 6), constrained_layout=True)
            known_xy = []
            freq, _, _ = plt.hist(inter_data, bins=bins, color=colors[0], 
                                  label=label)
            for fr, x in zip(freq, bin_centers):
                height = int(fr)
                y = height
                if x in [val for val, _ in known_xy]:
                    known_y = known_xy[[val for val, _ in known_xy].index(x)][1]
                    rad = int(round(max(int(f) for f in freq) / 40) + 1)
                    if y in range(known_y - rad, known_y + rad + 1) and y != known_y:
                        y = known_y - rad if y <= known_y else known_y + rad
                plt.annotate(str(height) if height > 0 else '', xy=(x, y), 
                             xytext=(0, .2), textcoords="offset points",
                             ha="center", va="bottom")
                known_xy.append((x, y))
            plt.xlabel(f"score")
            plt.ylabel("frequency")
            x_labels = [f"{x:.1f}" for x in bins]
            plt.xticks(bins, x_labels)
            plt.title(f"Inter Interaction Score (Reclassification cutoff = {cutoff})")
            plt.legend()
            plt.savefig(f"{output_directory}{filename}_inter_score.png")

            # Clear figure
            plt.clf()

    # normal distance histograms
    dist_data = data[["eucl_dist", "topo_dist"]].copy()
    labels = ["euclidean distance", "topological distance"]
    bins = [x * 5 for x in range(16)]
    bin_centers = np.diff(bins) * .5 + bins[:-1]
    dist_data[dist_data > 70] = 70
    plt.figure(figsize=(6.5, 6), constrained_layout=True)
    if add_labels:
        known_xy = []
    for col, label, color in zip(dist_data.columns, labels, colors):
        freq, _, _ = plt.hist(dist_data[[col]], bins=bins, alpha=.7, 
                              color=color, 
                              label=f"{label} (n={len(dist_data[~pd.isna(dist_data[col])].index)})")
        if add_labels:
            for fr, x in zip(freq, bin_centers):
                height = int(fr)
                y = height
                if x in [val for val, _ in known_xy]:
                    known_y = known_xy[[val for val, _ in known_xy].index(x)][1]
                    rad = int(round(max(int(f) for f in freq) / 40) + 1)
                    if y in range(known_y - rad, known_y + rad + 1) and y != known_y:
                        y = known_y - rad if y <= known_y else known_y + rad
                plt.annotate(str(height) if height > 0 else '', xy=(x, y),
                             xytext=(0, .2), textcoords="offset points",
                             ha="center", va="bottom")
                known_xy.append((x, y))
    plt.axvline(linker_minimum, color="darkred", linestyle="dashed", 
                linewidth=1)
    plt.axvline(linker_maximum, color="darkred", linestyle="dashed", 
                linewidth=1)
    if add_labels:
        plt.text(linker_minimum + 1, plt.ylim()[1] * 0.85, 
                 f"Linker\nminimum: {linker_minimum}", color="darkred")
        plt.text(linker_maximum + 1, plt.ylim()[1] * 0.85, 
                 f"Linker\nmaximum: {linker_maximum}", color="darkred")
    plt.xlabel(f"distance " + r"[$\AA$]")
    plt.ylabel("frequency")
    x_labels = [str(x) for x in bins]
    x_labels[-1] = str(float("inf"))
    plt.xticks(bins, x_labels)
    plt.legend()
    plt.title("Frequency of structural crosslink distances")
    plt.savefig(f"{output_directory}{filename}_hist.png")

    # Clear figure
    plt.clf()

    charts_strs, data_sets, label_sets, color_sets = ([] for _ in range(4))
    intra_data = data[data.unip_id_a == data.unip_id_b].copy()
    inter_data = data[data.unip_id_a != data.unip_id_b].copy()

    if not intra_data.empty:
        charts_strs.append("intra")
        data_sets.append([len(intra_data[(intra_data.pdb_id == '-') 
                                         & (intra_data.XL_type == "intra")].index),
                          len(intra_data[(intra_data.pdb_id != '-') 
                                         & (intra_data.XL_type == "intra")].index),
                          len(intra_data[(intra_data.XL_type == "inter") 
                                         & (intra_data.swiss_model_homology != '')].index),
                          len(intra_data[(intra_data.XL_type == "inter") 
                                         & (intra_data.swiss_model_homology == '')].index)])
        label_sets.append(["remains intra (no structure found)", 
                           "remains intra (structure found)",
                           "homology reference found", "new lead"])
        color_sets.append(["silver", "#FFCC00", "#9ACE9A", "lightblue"])
    if not inter_data.empty:
        charts_strs.append("inter")
        data_sets.append([len(inter_data[inter_data.pdb_id == '-'].index),
                          len(inter_data[(inter_data.pdb_id != '-') 
                                         & (np.isnan(inter_data.topo_dist))]),
                          len(inter_data[(inter_data.pdb_id != '-') 
                                         & (~np.isnan(inter_data.topo_dist)) 
                                         & (inter_data.evidence == '')].index),
                          len(inter_data[(inter_data.pdb_id != '-') 
                                         & (~np.isnan(inter_data.topo_dist)) 
                                         & (inter_data.evidence != '')].index)])
        label_sets.append(["no structure found", 
                           "not analyzed (structure found)", 
                           "reference structure found",
                           "new lead"])
        color_sets.append(["silver", "red", "#9ACE9A", "lightblue"])

    for charts_str, dataset, labels, colors in zip(charts_strs, data_sets, 
                                                   label_sets, color_sets):
        plt.figure(figsize=(6.5, 6), constrained_layout=True)

        def percentages(pct, all_vals):
            abs_val = int(np.round(pct / 100 * np.sum(all_vals)))
            return f"{pct:.1f}%\n(n={abs_val})" if abs_val > 0 else ''

        wedges, _, _ = plt.pie(dataset, 
                               autopct=lambda x: percentages(x, dataset),
                               colors=colors, textprops={"weight": "bold", 
                                                         "color": 'black'})
        plt.legend(wedges, labels)
        plt.title(f"Final distribution of {charts_str} cross-links (n={sum(dataset)})")
        plt.savefig(f"{output_directory}{filename}_validated_{charts_str}.png")

        # Clear figure
        plt.clf()
