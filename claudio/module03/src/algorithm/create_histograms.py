import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_homo_signal_histograms(data : pd.DataFrame, filename : str, output_directory : str):
    """
    create histograms for homology signal, e.g. for adjacency of interaction sites and peptide overlaps
    between/including interacting residues

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    output_directory : str

    Returns
    -------
        None 
    """

    # adjacency histogram
    adj_data = data["homo_adjacency"].copy()
    adj_data = adj_data[~np.isnan(adj_data)]
    colors = ["#9ACE9A", "silver"]
    if not adj_data.empty:
        bins = [round(x * 0.1, 1) for x in range(11)]
        plt.figure(figsize=(6.5, 6), constrained_layout=True)
        freq, _, _ = plt.hist(adj_data, bins=bins, color=colors[0])
        plt.xlabel(f"relative adjacency")
        bin_centers = np.diff(bins) * .5 + bins[:-1]
        for fr, x in zip(freq, bin_centers):
            height = int(fr)
            plt.annotate(str(height) if height > 0 else '', xy=(x, height), xytext=(0, .2), textcoords="offset points",
                         ha="center", va="bottom")
        plt.ylabel("frequency")
        x_labels = [str(x) for x in bins]
        plt.xticks(bins, x_labels)
        plt.title("Frequency of relative interaction site adjacencies " +
                  "$\left[adj = 1-\\frac{|pos_a - pos_b|}{len_{seq}}\\right]$")
        plt.savefig(f"{output_directory}{filename}_adj_hist.png")

        # Clear figure
        plt.clf()

    # histogram of peptide overlaps between/including interacting residues
    overl_data = data["homo_int_overl"].copy()
    overl_data = overl_data[~np.isnan(overl_data)]
    if not overl_data.empty:
        bins = [round(x * 0.1, 1) for x in range(11)]
        plt.figure(figsize=(6.5, 6), constrained_layout=True)
        freq, _, _ = plt.hist(overl_data, bins=bins, color=colors[0])
        bin_centers = np.diff(bins) * .5 + bins[:-1]
        for fr, x in zip(freq, bin_centers):
            height = int(fr)
            plt.annotate(str(height) if height > 0 else '', xy=(x, height), xytext=(0, .2), textcoords="offset points",
                         ha="center", va="bottom")
        plt.xlabel(f"relative overlap")
        plt.ylabel("frequency")
        x_labels = [str(x) for x in bins]
        plt.xticks(bins, x_labels)
        plt.title("Relative peptide overlaps (" + '$n_{\\neg 0}$' + f" = {len(overl_data[overl_data > 0].index)})")
        plt.savefig(f"{output_directory}{filename}_int_ovl.png")

        # Clear figure
        plt.clf()

    # histogram of peptide overlaps between/including interacting residues
    if "unip_id" in data.columns:
        overl_data_bool = data["homo_pep_overl"].copy()
    else:
        overl_data_bool = data[data.unip_id_a == data.unip_id_b]["homo_pep_overl"].copy()
    overl_data_bool = overl_data_bool[~np.isnan(overl_data_bool)]
    if not overl_data_bool.empty:
        bins = [0, .5,  1]
        plt.figure(figsize=(6.5, 6), constrained_layout=True)
        freq, _, _ = plt.hist(overl_data_bool.astype(int), bins=bins, color=colors[0])
        bin_centers = np.diff(bins) * .5 + bins[:-1]
        for fr, x in zip(freq, bin_centers):
            height = int(fr)
            plt.annotate(str(height) if height > 0 else '', xy=(x, height), xytext=(0, .2), textcoords="offset points",
                         ha="center", va="bottom")
        plt.ylabel("frequency")
        x_labels = [False, True]
        plt.xticks(bin_centers, x_labels)
        plt.title("Boolean distinction whether peptides overlap or not (intra-links only)")
        plt.savefig(f"{output_directory}{filename}_pep_ovl.png")

        # Clear figure
        plt.clf()

    # pie chart of peptide overlaps between/including interacting residues
    if "unip_id" in data.columns:
        overl_data_bool = data["homo_pep_overl"].copy()
    else:
        overl_data_bool = data[data.unip_id_a == data.unip_id_b]["homo_pep_overl"].copy()
    if not overl_data_bool.empty:
        data = [len(overl_data_bool[overl_data_bool].index),
                len(overl_data_bool[~overl_data_bool].index)]
        labels = ["overlap found", "no overlap"]
        plt.figure(figsize=(6.5, 6), constrained_layout=True)

        def percentages(pct, all_vals):
            abs_val = int(np.round(pct / 100 * np.sum(all_vals)))
            return f"{pct:.1f}%\n(n={abs_val})"

        wedges, _, _ = plt.pie(data, autopct=lambda x: percentages(x, data),
                                   colors=colors, textprops={"weight": "bold", "color": 'black'})
        plt.legend(wedges, labels)
        plt.title("Boolean distinction whether peptides overlap or not (intra-links only)")
        plt.savefig(f"{output_directory}{filename}_pep_ovl_pie.png")
