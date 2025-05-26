"""Deprecated module for creating histograms and pie charts for cross-link validation results."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_histograms(data: pd.DataFrame, filename: str, cutoff,
                      compute_scoring: bool, output_directory: str):
    """
    create histograms for inter scores, and pie charts for final 
    validation results

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    compute_scoring : bool,
    output_directory : str

    Returns
    -------
        None
    """
    #TODO missing input parameter description: cutoff

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
            plt.xlabel("score")
            plt.ylabel("frequency")
            x_labels = [f"{x:.1f}" for x in bins]
            plt.xticks(bins, x_labels)
            plt.title(f"Inter Interaction Score (Reclassification cutoff = {cutoff})")
            plt.legend()
            plt.savefig(f"{output_directory}{filename}_inter_score.png")

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
        color_sets.append(["#464444", "#FFCC00", "#9ACE9A", "lightblue"])
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
        color_sets.append(["#464444", "red", "#9ACE9A", "lightblue"])

    def percentages(pct, all_vals):
        abs_val = int(np.round(pct / 100 * np.sum(all_vals)))
        return f"{pct:.1f}%\n(n={abs_val})" if abs_val > 0 else ''

    for charts_str, dataset, labels, colors in zip(charts_strs, data_sets,
                                                   label_sets, color_sets):
        plt.figure(figsize=(6.5, 6), constrained_layout=True)


        wedges, _, autos = plt.pie(dataset,
                                   autopct=lambda x: percentages(x, dataset),
                                   colors=colors,
                                   textprops=dict(weight="bold"))
        autos[0].set_color('w')
        plt.legend(wedges, labels)
        plt.title(f"Final distribution of {charts_str} cross-links (n={sum(dataset)})")
        plt.savefig(f"{output_directory}{filename}_validated_{charts_str}.png")

        # Clear figure
        plt.clf()
