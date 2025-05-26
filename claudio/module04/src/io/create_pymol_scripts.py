"""Creates PyMOL scripts to highlight the observed cross-links in a three-dimensional structure."""
import numpy as np
import pandas as pd


def setup_pml_scripts(data, bg_color="white"):
    """
    Prepares PyMOL scripts for visualization of crosslink data.
    
    Parameters
    ----------
    data : pd.DataFrame
    bg_color : str
    
    Returns
    -------
    None
    
    """

    for pdb_id in data.pdb_id.unique():
        if pdb_id.replace(' ', '') != '' and \
                pdb_id != '-' and \
                not data[(data.pdb_id == pdb_id) & (data.path != '-')].empty:
            xl_set = data[(data.pdb_id == pdb_id) & (data.path != '-')]
            pdb_path_id = '.'.join(xl_set.iloc[0].path.split('.')[:-1])
            out_path = f"{pdb_path_id}.pml"

            chains = pd.concat([xl_set.chain_a, xl_set.chain_b]).unique()
            chains_dict = {}
            color_i = 3
            for chain in chains:
                dps_with_chain = xl_set[(xl_set.chain_a == chain)
                                        | (xl_set.chain_b == chain)]
                if np.any(~(pd.isna(dps_with_chain.pdb_pos_a)
                            | pd.isna(dps_with_chain.pdb_pos_b))):
                    color_i = color_i + 1 if color_i in [2, 4, 6, 13] else color_i
                    chains_dict[chain] = color_i
                    color_i += 1
            cm_map = {"bg": bg_color,
                      "chain": chains_dict,
                      "intra": {"valid": 2,
                                "out_range": 2,
                                "overlaps": 2,
                                "same": 2,
                                "unknown": "black"},
                      "inter": {"valid": 13,
                                "out_range": 13,
                                "overlaps": 13,
                                "same": 13,
                                "unknown": "black"}
                      }

            dists = {"intra": {"valid": [],
                               "out_range": [],
                               "overlaps": [],
                               "same": [],
                               "unknown": []},
                     "inter": {"valid": [],
                               "out_range": [],
                               "overlaps": [],
                               "same": [],
                               "unknown": []}}
            for row in xl_set.itertuples():
                i = row.Index
                if not (pd.isna(row.pdb_pos_a) or pd.isna(row.pdb_pos_b)) and (row.XL_confirmed or '_' not in str(i)):
                    dist_data = (i,
                                 (row.chain_a, row.pdb_pos_a,
                                  row.chain_b, row.pdb_pos_b)
                                )
                    dists[
                        "intra" if row.chain_a == row.chain_b else "inter"
                    ][
                        "valid" if (not row.evidence) and not pd.isna(row.topo_dist) else
                        ("out_range" if "distance" in row.evidence else
                         ("overlaps" if ("overlap" in row.evidence) else
                          ("unknown" if pd.isna(row.topo_dist) else "same")))
                    ].append(dist_data)

            write_pml_script(dists, cm_map, out_path)


def write_pml_script(dists, color_map, output_path, start=0, zoom=50):
    """
    Write PyMOL script to visualize crosslink data.
    
    Parameters
    ----------
    dists : dict
    color_map : dict
    output_path : str
    start : int
    zoom : int
    
    Returns
    -------
    None
    
    """

    chains = color_map["chain"].keys()
    pdb = output_path.split('/')[-1].split('.')[0]

    with open(output_path, 'w', encoding="utf-8") as f:
        file_content = f"load {pdb}.pdb\n" \
                       f"hide all\n" \
                       f"bg_color {color_map['bg'] if 'bg' in color_map.keys() else 'white'}\n" \
                       f"set transparency, 0.8\n" \
                       f"zoom center, {zoom};\n"
        for chain in chains:
            file_content += f"hide everything, show cartoon, chain {chain}\n"\
                            f"show surface, chain {chain} and {pdb}\n"\
                            f"color {color_map['chain'][chain]}, chain {chain}\n"\
                            f"show cartoon, chain {chain}\n"
        for d_type, sites in dists.items():
            for site in sites:
                dists_dict = sites[site]
                for _, dist in enumerate(dists_dict):
                    i, (chain_a, res_id_a, chain_b, res_id_b) = dist
                    res_id_a = int(res_id_a) + start
                    res_id_b = int(res_id_b) + start
                    file_content += f"dist {d_type}_{i}_{site} , " \
                                    f"resid {res_id_a} and {pdb} and chain {chain_a} and name cb, " \
                                    f"resid {res_id_b} and {pdb} and chain {chain_b} and name cb\n"
        file_content += "show dashes\n" \
                        "set dash_gap, 0.1\n"

        for d_type, sites in dists.items():
            color_specified = d_type in color_map.keys()
            for site in sites:
                file_content += f"color {color_map[d_type][site] if color_specified else 'white'}, {d_type}*_{site}\n"

        file_content += "set dash_gap, 1, *_out_range\n" \
                        "set dash_gap, 1, *_overlaps\n" \
                        "set dash_gap, 1, *_same\n" \
                        "hide dashes, *_unknown\n"

        file_content += f"set dash_width, 9\n" \
                        f"center\n" \
                        f"save {pdb}.pse\n" \
                        f"png {pdb}.png\n"
        f.write(file_content)
