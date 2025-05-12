import warnings
import click
import pandas as pd

warnings.filterwarnings("ignore")


@click.command()
@click.option("-i", "--input-filepath", default="data/out/full/liu18_schweppe17_linked_residues_intra-homo_2370_nonredundant_final.csv")
@click.option("-i2", "--input-filepath2", default="data/in/liu18_schweppe17_linked_residues_intra-homo_2370_nonredundant.csv")
@click.option("-p", "--projections", default="peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2")
def main(input_filepath, input_filepath2, projections):
    print("====================================================================================================\n"
          "====================================================================================================\n"
          "BEFORE:")
    data = pd.read_csv(input_filepath2)
    new_keys = ["pep_a", "pep_b", "pos_a", "pos_b", "res_pos_a", "res_pos_b", "unip_id_a", "unip_id_b"]
    projections = {projections.split(',')[i]: new_keys[i] for i in range(len(new_keys))}
    data.rename(columns=projections, inplace=True)

    key_a, key_b = ("unip_id_a", "unip_id_b")
    intra = data[key_a] == data[key_b]
    print(f"number of unique proteins: {len(data[key_a].append(data[key_b]).unique())}\n")
    print(f"number of intra XLs: {len(data[intra])} / {len(data.index)} ({100 * len(data[intra]) / len(data.index):.2f}%), in {len(data[intra][key_a].append(data[intra][key_b]).unique())} proteins")
    print(f"number of inter XLs: {len(data[~intra])} / {len(data.index)} ({100 * len(data[~intra]) / len(data.index):.2f}%), in {len(data[~intra][key_a].append(data[~intra][key_b]).unique())} proteins"
          f"\n")

    print("====================================================================================================\n"
          "====================================================================================================\n"
          "AFTER:")
    data = pd.read_csv(input_filepath, index_col=0)
    non_multi_chain_indeces = []
    for i, ind in enumerate(data.index):
        ind = int(str(ind).split('_',maxsplit=1)[0])
        if ind not in [j for _, j in non_multi_chain_indeces]:
            non_multi_chain_indeces.append((i, ind))
    data = data.astype({"evidence": str}, errors="ignore").iloc[[i for i, _ in non_multi_chain_indeces]]

    key_a, key_b = ("unip_id_a", "unip_id_b")
    intra = data[key_a] == data[key_b]
    struct_found = (data.pdb_id != '-') | (data.topo_dist == 0)
    dist_calc = (intra & ~pd.isna(data.topo_dist)) | (~intra & ~pd.isna(data.topo_dist) & (data.pdb_id != '-'))
    print(f"number of unique proteins: {len(data[key_a].append(data[key_b]).unique())}\n")
    print(f"number of intra XLs: {len(data[intra])} / {len(data.index)} ({100 * len(data[intra]) / len(data.index):.2f}%), in {len(data[intra][key_a].append(data[intra][key_b]).unique())} proteins")
    print(f"number of inter XLs: {len(data[~intra])} / {len(data.index)} ({100 * len(data[~intra]) / len(data.index):.2f}%), in {len(data[~intra][key_a].append(data[~intra][key_b]).unique())} proteins"
          f"\n")
    print(f"number of analyzed xls: {len(data[intra | dist_calc].index)} / {len(data.index)} ({100 * len(data[intra | dist_calc].index) / len(data.index):.2f}%), in {len(data[intra | dist_calc][key_a].append(data[dist_calc][key_b]).unique())} proteins")
    print(f"\tfraction of analyzed xls given a structure was found: {len(data[intra | dist_calc].index)} / {len(data[struct_found].index)} ({100 * len(data[intra | dist_calc].index) / len(data[struct_found].index):.2f}%)\n")

    print(f"number of xls for which structures were found: {len(data[struct_found].index)} ({100 * len(data[struct_found].index) / len(data.index):.2f}%), in {len(data[struct_found][key_a].append(data[struct_found][key_b]).unique())} proteins"
          f"\t\t\t\t\t<- intra: {len(data[struct_found & intra].index)} ({100 * len(data[struct_found & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[struct_found & ~intra].index)} ({100 * len(data[struct_found & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"number of xls for which no structures were found: {len(data[~struct_found].index)} ({100 * len(data[~struct_found].index) / len(data.index):.2f}%), in {len(data[~struct_found][key_a].append(data[~struct_found][key_b]).unique())} proteins"
          f"\t\t\t\t<- intra: {len(data[~struct_found & intra].index)} ({100 * len(data[~struct_found & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[~struct_found & ~intra].index)} ({100 * len(data[~struct_found & ~intra].index) / len(data[~intra].index):.2f}%)\n")

    print(f"number of xls for which dists were computed: {len(data[dist_calc].index)} ({100 * len(data[dist_calc].index) / len(data.index):.2f}%), in {len(data[dist_calc][key_a].append(data[dist_calc][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t<- intra: {len(data[dist_calc & intra].index)} ({100 * len(data[dist_calc & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[dist_calc & ~intra].index)} ({100 * len(data[dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"\tfraction of xls for which dists were computed given a structure was found: {100 * len(data[dist_calc].index) / len(data[struct_found].index):.2f}%"
          f"\t\t\t<- intra: {100 * len(data[dist_calc & struct_found & intra].index) / len(data[struct_found & intra].index):.2f}%", end='')
    print(f", inter: {100 * len(data[dist_calc & struct_found & ~intra].index) / len(data[struct_found & ~intra].index):.2f}%")
    print(f"number of xls for which no dists were computed: {len(data[~dist_calc].index)} ({100 * len(data[~dist_calc].index) / len(data.index):.2f}%), in {len(data[~dist_calc][key_a].append(data[~dist_calc][key_b]).unique())} proteins"
          f"\t\t\t\t\t<- intra: {len(data[~dist_calc & intra].index)} ({100 * len(data[~dist_calc & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[~dist_calc & ~intra].index)} ({100 * len(data[~dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"\tfraction of xls for which no dists were computed given a structure was found: {100 * len(data[struct_found & ~dist_calc].index) / len(data[struct_found].index):.2f}%"
          f"\t\t<- intra: {100 * len(data[struct_found & ~dist_calc & intra].index) / len(data[struct_found & intra].index):.2f}%", end='')
    print(f", inter: {100 * len(data[struct_found & ~dist_calc & ~intra].index) / len(data[struct_found & ~intra].index):.2f}%\n")

    dist_evid = data.evidence.str.contains('distance') | data.evidence.str.contains('same')
    still_intra = intra & (data.evidence == 'nan')
    evidence_found = data.evidence != 'nan'
    print(f"number of computed distances in intra xls: {len(data[intra & dist_calc].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc][key_a].append(data[intra & dist_calc][key_b]).unique())} proteins")
    print(f"\tfraction of analyzed intra xls given a structure was found: {len(data[intra & dist_calc].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc].index) / len(data[intra & struct_found].index):.2f}%)")
    print(f"number of intra xls with dist in range: {len(data[intra & dist_calc & ~dist_evid].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc & ~dist_evid].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc & ~dist_evid][key_a].append(data[intra & dist_calc & ~dist_evid][key_b]).unique())} proteins")
    print(f"\tfraction of intra xls with dist in range given a structure was found: {len(data[intra & dist_calc & ~dist_evid].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc & ~dist_evid].index) / len(data[intra & struct_found].index):.2f}%)")
    print(f"number of intra xls with dist outside of range: {len(data[intra & dist_calc & dist_evid].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc & dist_evid].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc & dist_evid][key_a].append(data[intra & dist_calc & dist_evid][key_b]).unique())} proteins")
    print(f"\tfraction of intra xls with dist outside of range given a structure was found: {len(data[intra & dist_calc & dist_evid].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc & dist_evid].index) / len(data[intra & struct_found].index):.2f}%)")

    print(f"\nnumber of computed distances in inter xls: {len(data[~intra & dist_calc].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc][key_a].append(data[~intra & dist_calc][key_b]).unique())} proteins")
    print(f"\tfraction of analyzed inter xls given a structure was found: {len(data[~intra & dist_calc].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc].index) / len(data[~intra & struct_found].index):.2f}%)")
    print(f"number of inter xls with dist in range: {len(data[~intra & dist_calc & ~dist_evid].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc & ~dist_evid].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc & ~dist_evid][key_a].append(data[~intra & dist_calc & ~dist_evid][key_b]).unique())} proteins")
    print(f"\tfraction of inter xls with dist in range given a structure was found: {len(data[~intra & dist_calc & ~dist_evid].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc & ~dist_evid].index) / len(data[~intra & struct_found].index):.2f}%)")
    print(f"number of inter xls with dist outside of range: {len(data[~intra & dist_calc & dist_evid].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc & dist_evid].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc & dist_evid][key_a].append(data[~intra & dist_calc & dist_evid][key_b]).unique())} proteins")
    print(f"\tfraction of inter xls with dist outside of range given a structure was found: {len(data[~intra & dist_calc & dist_evid].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc & dist_evid].index) / len(data[~intra & struct_found].index):.2f}%)")

    print(f"\n\nnumber of intra xls remaining as intra: {len(data[still_intra].index)} / {len(data[intra].index)} ({100 * len(data[still_intra].index) / len(data[intra].index):.2f}%), in {len(data[still_intra][key_a].append(data[still_intra][key_b]).unique())} proteins")
    print(f"\tfraction of intra xls remaining as intra given a distance was computed: {len(data[still_intra].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[still_intra].index) / len(data[dist_calc & intra].index):.2f}%)")
    print(f"number of intra xls reclassified as homomer inter: {len(data[intra & evidence_found].index)} / {len(data[intra].index)} ({100 * len(data[intra & evidence_found].index) / len(data[intra].index):.2f}%), in {len(data[intra & evidence_found][key_a].append(data[intra & evidence_found][key_b]).unique())} proteins")
    print(f"\tfraction of intra xls reclassified as homomer inter given a distance was computed: {len(data[intra & evidence_found].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[intra & evidence_found].index) / len(data[dist_calc & intra].index):.2f}%)")
    print(f"number of intra xls reclassified as new homomer inter: {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index)} / {len(data[intra].index)} ({100 * len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index) / len(data[intra].index):.2f}%), in {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)][key_a].append(data[intra & evidence_found & pd.isna(data.swiss_model_homology)][key_b]).unique())} proteins")
    print(f"\tfraction of intra xls reclassified as new homomer inter given a distance was computed: {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index) / len(data[intra & ~(pd.isna(data.topo_dist))].index):.2f}%)")
    print(f"number of intra xls with ops: {len(data[intra & data.homo_pep_overl].index)} / {len(data[intra].index)} ({100 * len(data[intra & data.homo_pep_overl].index) / len(data[intra].index):.2f}%), in {len(data[intra & data.homo_pep_overl][key_a].append(data[intra & data.homo_pep_overl][key_b]).unique())} proteins")
    print(f"number of intra xls without ops: {len(data[intra & ~data.homo_pep_overl].index)} / {len(data[intra].index)} ({100 * len(data[intra & ~data.homo_pep_overl].index) / len(data[intra].index):.2f}%), in {len(data[intra & ~data.homo_pep_overl][key_a].append(data[intra & ~data.homo_pep_overl][key_b]).unique())} proteins\n")

    ops_only_evid = data.evidence.str.contains('overlap') & ~data.evidence.str.contains('same') & ~data.evidence.str.contains('distance')
    dist_only_evid = ~data.evidence.str.contains('overlap') & ~data.evidence.str.contains('same') & data.evidence.str.contains('distance')
    analysis_passed = dist_calc | intra
    same_evid = data.evidence.str.contains('same')
    both_evid = data.evidence.str.contains('overlap') & data.evidence.str.contains('distance')
    print(f"number of xls that passed either analysis: {len(data[analysis_passed].index)} ({100 * len(data[analysis_passed].index) / len(data.index):.2f}%), in {len(data[analysis_passed][key_a].append(data[analysis_passed][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t\t<- intra: {len(data[intra].index)} ({100 * len(data[intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[dist_calc & ~intra].index)} ({100 * len(data[dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"number of xls with no refuting evidence: {len(data[~evidence_found & analysis_passed].index)} ({100 * len(data[~evidence_found & analysis_passed].index) / len(data.index):.2f}%), in {len(data[~evidence_found & analysis_passed][key_a].append(data[~evidence_found & analysis_passed][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t\t\t<- intra: {len(data[~evidence_found & analysis_passed & intra].index)} ({100 * len(data[~evidence_found & analysis_passed & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[~evidence_found & analysis_passed & ~intra].index)} ({100 * len(data[~evidence_found & analysis_passed & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"number of xls with refuting evidence: {len(data[evidence_found].index)} ({100 * len(data[evidence_found].index) / len(data.index):.2f}%), in {len(data[evidence_found][key_a].append(data[evidence_found][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t\t\t\t<- intra: {len(data[evidence_found & intra].index)} ({100 * len(data[evidence_found & intra].index) / len(data[intra].index):.2f}%)", end='')
    print(f", inter: {len(data[evidence_found & ~intra].index)} ({100 * len(data[evidence_found & ~intra].index) / len(data[~intra].index):.2f}%)")

    print(f"\tfraction of evidences based on dist given evidence was found: {len(data[dist_only_evid].index)} ({100 * len(data[dist_only_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[dist_only_evid][key_a].append(data[dist_only_evid][key_b]).unique())} proteins"
          f"\t\t\t<- intra: {len(data[dist_only_evid & intra].index)} ({100 * len(data[dist_only_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)", end='')
    print(f", inter: {len(data[dist_only_evid & ~intra].index)} ({100 * len(data[dist_only_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(f"\tfraction of evidences based on ops given evidence was found: {len(data[ops_only_evid].index)} ({100 * len(data[ops_only_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[ops_only_evid][key_a].append(data[ops_only_evid][key_b]).unique())} proteins"
          f"\t\t\t<- intra: {len(data[ops_only_evid & intra].index)} ({100 * len(data[ops_only_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)", end='')
    print(f", inter: {len(data[ops_only_evid & ~intra].index)} ({100 * len(data[ops_only_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(f"\tfraction of evidences based on both analyses given evidence was found: {len(data[both_evid].index)} ({100 * len(data[both_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[both_evid][key_a].append(data[both_evid][key_b]).unique())} proteins"
          f"\t<- intra: {len(data[both_evid & intra].index)} ({100 * len(data[both_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)", end='')
    print(f", inter: {len(data[both_evid & ~intra].index)} ({100 * len(data[both_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(f"\tfraction of evidences based on same peptides given evidence was found: {len(data[same_evid].index)} ({100 * len(data[same_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[same_evid][key_a].append(data[same_evid][key_b]).unique())} proteins"
          f"\t<- intra: {len(data[same_evid & intra].index)} ({100 * len(data[same_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)", end='')
    print(f", inter: {len(data[same_evid & ~intra].index)} ({100 * len(data[same_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)\n")


    print("====================================================================================================\n"
          "====================================================================================================\n"
          "INCLUDING MULTI-CHAIN:")
    data = pd.read_csv(input_filepath, index_col=0)
    data = data.astype({"evidence": str}, errors="ignore")
    intra = data[key_a] == data[key_b]
    print(f"number of unique proteins: {len(data[key_a].append(data[key_b]).unique())}\n")
    print(f"number of intra XLs: {len(data[intra])} / {len(data.index)} ({100 * len(data[intra]) / len(data.index):.2f}%), in {len(data[intra][key_a].append(data[intra][key_b]).unique())} proteins")
    print(f"number of inter XLs: {len(data[~intra])} / {len(data.index)} ({100 * len(data[~intra]) / len(data.index):.2f}%), in {len(data[~intra][key_a].append(data[~intra][key_b]).unique())} proteins"
          f"\n")

    is_multi_chain_dp = data.index.str.contains('_')
    print(f"number of multi_chain datapoints: {len(data[is_multi_chain_dp].index)} ({100 * len(data[is_multi_chain_dp].index) / len(data.index):.2f}%), in {len(data[is_multi_chain_dp][key_a].append(data[is_multi_chain_dp][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t\t\t\t<- intra: {len(data[is_multi_chain_dp & intra].index)} ({100 * len(data[is_multi_chain_dp & intra].index) / len(data[is_multi_chain_dp].index):.2f}%)", end='')
    print(f", inter: {len(data[is_multi_chain_dp & ~intra].index)} ({100 * len(data[is_multi_chain_dp & ~intra].index) / len(data[is_multi_chain_dp].index):.2f}%)")
    is_confirmed = data.XL_confirmed
    print(f"number of confirmed datapoints: {len(data[is_confirmed].index)} ({100 * len(data[is_confirmed].index) / len(data.index):.2f}%), in {len(data[is_confirmed][key_a].append(data[is_confirmed][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t\t\t\t\t<- intra: {len(data[is_confirmed & intra].index)} ({100 * len(data[is_confirmed & intra].index) / len(data[is_confirmed].index):.2f}%)",
          end='')
    print(f", inter: {len(data[is_confirmed & ~intra].index)} ({100 * len(data[is_confirmed & ~intra].index) / len(data[is_confirmed].index):.2f}%)")

    is_double_validated = is_multi_chain_dp & is_confirmed
    print(f"number of confirmed an multi_chain datapoints: {len(data[is_double_validated].index)} ({100 * len(data[is_double_validated].index) / len(data.index):.2f}%), in {len(data[is_double_validated][key_a].append(data[is_double_validated][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t\t<- intra: {len(data[is_double_validated & intra].index)} ({100 * len(data[is_double_validated & intra].index) / len(data[is_double_validated].index):.2f}%)",
          end='')
    print(f", inter: {len(data[is_double_validated & ~intra].index)} ({100 * len(data[is_double_validated & ~intra].index) / len(data[is_double_validated].index):.2f}%)\n")

    key_a, key_b = ("unip_id_a", "unip_id_b")
    intra = data[key_a] == data[key_b]
    struct_found = (data.pdb_id != '-') | (data.topo_dist == 0)
    dist_calc = (intra & ~pd.isna(data.topo_dist)) | (~intra & ~pd.isna(data.topo_dist) & (data.pdb_id != '-'))
    print(f"number of analyzed xls: {len(data[intra | dist_calc].index)} / {len(data.index)} ({100 * len(data[intra | dist_calc].index) / len(data.index):.2f}%), in {len(data[intra | dist_calc][key_a].append(data[dist_calc][key_b]).unique())} proteins")
    print(f"\tfraction of analyzed xls given a structure was found: {len(data[intra | dist_calc].index)} / {len(data[struct_found].index)} ({100 * len(data[intra | dist_calc].index) / len(data[struct_found].index):.2f}%)\n")

    print(f"number of xls for which structures were found: {len(data[struct_found].index)} ({100 * len(data[struct_found].index) / len(data.index):.2f}%), in {len(data[struct_found][key_a].append(data[struct_found][key_b]).unique())} proteins"
          f"\t\t\t\t\t<- intra: {len(data[struct_found & intra].index)} ({100 * len(data[struct_found & intra].index) / len(data[intra].index):.2f}%)",
          end='')
    print(f", inter: {len(data[struct_found & ~intra].index)} ({100 * len(data[struct_found & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"number of xls for which no structures were found: {len(data[~struct_found].index)} ({100 * len(data[~struct_found].index) / len(data.index):.2f}%), in {len(data[~struct_found][key_a].append(data[~struct_found][key_b]).unique())} proteins"
          f"\t\t\t\t<- intra: {len(data[~struct_found & intra].index)} ({100 * len(data[~struct_found & intra].index) / len(data[intra].index):.2f}%)",
          end='')
    print(f", inter: {len(data[~struct_found & ~intra].index)} ({100 * len(data[~struct_found & ~intra].index) / len(data[~intra].index):.2f}%)\n")

    print(f"number of xls for which dists were computed: {len(data[dist_calc].index)} ({100 * len(data[dist_calc].index) / len(data.index):.2f}%), in {len(data[dist_calc][key_a].append(data[dist_calc][key_b]).unique())} proteins"
          f"\t\t\t\t\t\t<- intra: {len(data[dist_calc & intra].index)} ({100 * len(data[dist_calc & intra].index) / len(data[intra].index):.2f}%)",
          end='')
    print(f", inter: {len(data[dist_calc & ~intra].index)} ({100 * len(data[dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"\tfraction of xls for which dists were computed given a structure was found: {100 * len(data[dist_calc].index) / len(data[struct_found].index):.2f}%"
          f"\t\t\t<- intra: {100 * len(data[dist_calc & struct_found & intra].index) / len(data[struct_found & intra].index):.2f}%",
          end='')
    print(f", inter: {100 * len(data[dist_calc & struct_found & ~intra].index) / len(data[struct_found & ~intra].index):.2f}%")
    print(f"number of xls for which no dists were computed: {len(data[~dist_calc].index)} ({100 * len(data[~dist_calc].index) / len(data.index):.2f}%), in {len(data[~dist_calc][key_a].append(data[~dist_calc][key_b]).unique())} proteins"
          f"\t\t\t\t\t<- intra: {len(data[~dist_calc & intra].index)} ({100 * len(data[~dist_calc & intra].index) / len(data[intra].index):.2f}%)",
          end='')
    print(f", inter: {len(data[~dist_calc & ~intra].index)} ({100 * len(data[~dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(f"\tfraction of xls for which no dists were computed given a structure was found: {100 * len(data[struct_found & ~dist_calc].index) / len(data[struct_found].index):.2f}%"
          f"\t\t<- intra: {100 * len(data[struct_found & ~dist_calc & intra].index) / len(data[struct_found & intra].index):.2f}%",
          end='')
    print(f", inter: {100 * len(data[struct_found & ~dist_calc & ~intra].index) / len(data[struct_found & ~intra].index):.2f}%\n")

    dist_evid = data.evidence.str.contains('distance') | data.evidence.str.contains('same')
    still_intra = intra & (data.evidence == 'nan')
    evidence_found = data.evidence != 'nan'
    print(
        f"number of computed distances in intra xls: {len(data[intra & dist_calc].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc][key_a].append(data[intra & dist_calc][key_b]).unique())} proteins")
    print(
        f"\tfraction of analyzed intra xls given a structure was found: {len(data[intra & dist_calc].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc].index) / len(data[intra & struct_found].index):.2f}%)")
    print(
        f"number of intra xls with dist in range: {len(data[intra & dist_calc & ~dist_evid].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc & ~dist_evid].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc & ~dist_evid][key_a].append(data[intra & dist_calc & ~dist_evid][key_b]).unique())} proteins")
    print(
        f"\tfraction of intra xls with dist in range given a structure was found: {len(data[intra & dist_calc & ~dist_evid].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc & ~dist_evid].index) / len(data[intra & struct_found].index):.2f}%)")
    print(
        f"number of intra xls with dist outside of range: {len(data[intra & dist_calc & dist_evid].index)} / {len(data[intra].index)} ({100 * len(data[intra & dist_calc & dist_evid].index) / len(data[intra].index):.2f}%), in {len(data[intra & dist_calc & dist_evid][key_a].append(data[intra & dist_calc & dist_evid][key_b]).unique())} proteins")
    print(
        f"\tfraction of intra xls with dist outside of range given a structure was found: {len(data[intra & dist_calc & dist_evid].index)} / {len(data[intra & struct_found].index)} ({100 * len(data[intra & dist_calc & dist_evid].index) / len(data[intra & struct_found].index):.2f}%)")

    print(
        f"\nnumber of computed distances in inter xls: {len(data[~intra & dist_calc].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc][key_a].append(data[~intra & dist_calc][key_b]).unique())} proteins")
    print(
        f"\tfraction of analyzed inter xls given a structure was found: {len(data[~intra & dist_calc].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc].index) / len(data[~intra & struct_found].index):.2f}%)")
    print(
        f"number of inter xls with dist in range: {len(data[~intra & dist_calc & ~dist_evid].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc & ~dist_evid].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc & ~dist_evid][key_a].append(data[~intra & dist_calc & ~dist_evid][key_b]).unique())} proteins")
    print(
        f"\tfraction of inter xls with dist in range given a structure was found: {len(data[~intra & dist_calc & ~dist_evid].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc & ~dist_evid].index) / len(data[~intra & struct_found].index):.2f}%)")
    print(
        f"number of inter xls with dist outside of range: {len(data[~intra & dist_calc & dist_evid].index)} / {len(data[~intra].index)} ({100 * len(data[~intra & dist_calc & dist_evid].index) / len(data[~intra].index):.2f}%), in {len(data[~intra & dist_calc & dist_evid][key_a].append(data[~intra & dist_calc & dist_evid][key_b]).unique())} proteins")
    print(
        f"\tfraction of inter xls with dist outside of range given a structure was found: {len(data[~intra & dist_calc & dist_evid].index)} / {len(data[~intra & struct_found].index)} ({100 * len(data[~intra & dist_calc & dist_evid].index) / len(data[~intra & struct_found].index):.2f}%)")

    print(
        f"\n\nnumber of intra xls remaining as intra: {len(data[still_intra].index)} / {len(data[intra].index)} ({100 * len(data[still_intra].index) / len(data[intra].index):.2f}%), in {len(data[still_intra][key_a].append(data[still_intra][key_b]).unique())} proteins")
    print(
        f"\tfraction of intra xls remaining as intra given a distance was computed: {len(data[still_intra].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[still_intra].index) / len(data[dist_calc & intra].index):.2f}%)")
    print(
        f"number of intra xls reclassified as homomer inter: {len(data[intra & evidence_found].index)} / {len(data[intra].index)} ({100 * len(data[intra & evidence_found].index) / len(data[intra].index):.2f}%), in {len(data[intra & evidence_found][key_a].append(data[intra & evidence_found][key_b]).unique())} proteins")
    print(
        f"\tfraction of intra xls reclassified as homomer inter given a distance was computed: {len(data[intra & evidence_found].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[intra & evidence_found].index) / len(data[dist_calc & intra].index):.2f}%)")
    print(
        f"number of intra xls reclassified as new homomer inter: {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index)} / {len(data[intra].index)} ({100 * len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index) / len(data[intra].index):.2f}%), in {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)][key_a].append(data[intra & evidence_found & pd.isna(data.swiss_model_homology)][key_b]).unique())} proteins")
    print(
        f"\tfraction of intra xls reclassified as new homomer inter given a distance was computed: {len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index)} / {len(data[dist_calc & intra].index)} ({100 * len(data[intra & evidence_found & pd.isna(data.swiss_model_homology)].index) / len(data[intra & ~(pd.isna(data.topo_dist))].index):.2f}%)")
    print(
        f"number of intra xls with ops: {len(data[intra & data.homo_pep_overl].index)} / {len(data[intra].index)} ({100 * len(data[intra & data.homo_pep_overl].index) / len(data[intra].index):.2f}%), in {len(data[intra & data.homo_pep_overl][key_a].append(data[intra & data.homo_pep_overl][key_b]).unique())} proteins")
    print(
        f"number of intra xls without ops: {len(data[intra & ~data.homo_pep_overl].index)} / {len(data[intra].index)} ({100 * len(data[intra & ~data.homo_pep_overl].index) / len(data[intra].index):.2f}%), in {len(data[intra & ~data.homo_pep_overl][key_a].append(data[intra & ~data.homo_pep_overl][key_b]).unique())} proteins\n")

    ops_only_evid = data.evidence.str.contains('overlap') & ~data.evidence.str.contains(
        'same') & ~data.evidence.str.contains('distance')
    dist_only_evid = ~data.evidence.str.contains('overlap') & ~data.evidence.str.contains(
        'same') & data.evidence.str.contains('distance')
    analysis_passed = dist_calc | intra
    same_evid = data.evidence.str.contains('same')
    both_evid = data.evidence.str.contains('overlap') & data.evidence.str.contains('distance')
    print(
        f"number of xls that passed either analysis: {len(data[analysis_passed].index)} ({100 * len(data[analysis_passed].index) / len(data.index):.2f}%), in {len(data[analysis_passed][key_a].append(data[analysis_passed][key_b]).unique())} proteins"
        f"\t\t\t\t\t\t\t\t<- intra: {len(data[intra].index)} ({100 * len(data[intra].index) / len(data[intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[dist_calc & ~intra].index)} ({100 * len(data[dist_calc & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(
        f"number of xls with no refuting evidence: {len(data[~evidence_found & analysis_passed].index)} ({100 * len(data[~evidence_found & analysis_passed].index) / len(data.index):.2f}%), in {len(data[~evidence_found & analysis_passed][key_a].append(data[~evidence_found & analysis_passed][key_b]).unique())} proteins"
        f"\t\t\t\t\t\t\t\t\t<- intra: {len(data[~evidence_found & analysis_passed & intra].index)} ({100 * len(data[~evidence_found & analysis_passed & intra].index) / len(data[intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[~evidence_found & analysis_passed & ~intra].index)} ({100 * len(data[~evidence_found & analysis_passed & ~intra].index) / len(data[~intra].index):.2f}%)")
    print(
        f"number of xls with refuting evidence: {len(data[evidence_found].index)} ({100 * len(data[evidence_found].index) / len(data.index):.2f}%), in {len(data[evidence_found][key_a].append(data[evidence_found][key_b]).unique())} proteins"
        f"\t\t\t\t\t\t\t\t\t\t<- intra: {len(data[evidence_found & intra].index)} ({100 * len(data[evidence_found & intra].index) / len(data[intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[evidence_found & ~intra].index)} ({100 * len(data[evidence_found & ~intra].index) / len(data[~intra].index):.2f}%)")

    print(
        f"\tfraction of evidences based on dist given evidence was found: {len(data[dist_only_evid].index)} ({100 * len(data[dist_only_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[dist_only_evid][key_a].append(data[dist_only_evid][key_b]).unique())} proteins"
        f"\t\t\t<- intra: {len(data[dist_only_evid & intra].index)} ({100 * len(data[dist_only_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[dist_only_evid & ~intra].index)} ({100 * len(data[dist_only_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(
        f"\tfraction of evidences based on ops given evidence was found: {len(data[ops_only_evid].index)} ({100 * len(data[ops_only_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[ops_only_evid][key_a].append(data[ops_only_evid][key_b]).unique())} proteins"
        f"\t\t\t<- intra: {len(data[ops_only_evid & intra].index)} ({100 * len(data[ops_only_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[ops_only_evid & ~intra].index)} ({100 * len(data[ops_only_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(
        f"\tfraction of evidences based on both analyses given evidence was found: {len(data[both_evid].index)} ({100 * len(data[both_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[both_evid][key_a].append(data[both_evid][key_b]).unique())} proteins"
        f"\t<- intra: {len(data[both_evid & intra].index)} ({100 * len(data[both_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[both_evid & ~intra].index)} ({100 * len(data[both_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)")
    print(
        f"\tfraction of evidences based on same peptides given evidence was found: {len(data[same_evid].index)} ({100 * len(data[same_evid].index) / len(data[evidence_found].index):.2f}%), in {len(data[same_evid][key_a].append(data[same_evid][key_b]).unique())} proteins"
        f"\t<- intra: {len(data[same_evid & intra].index)} ({100 * len(data[same_evid & intra].index) / len(data[evidence_found & intra].index):.2f}%)",
        end='')
    print(
        f", inter: {len(data[same_evid & ~intra].index)} ({100 * len(data[same_evid & ~intra].index) / len(data[evidence_found & ~intra].index):.2f}%)\n")

    #     print("\n\n\n")
    #     print("Number of Nans in dist column:", sum(pd.isna(data["topo_dist"])))
    #     print("Number of datapoints with dist = 0:", sum(data["topo_dist"] == 0))
    #     print("Number of computed distances in dist column:", len(data.index) - sum(pd.isna(data["topo_dist"])))
    #     project_path = '/'.join(os.path.abspath(__file__).split('/')[:-3])
    #     project_path = project_path + '/' if project_path else ""
    #     print(f"number of successes:\n\ta:{len(data.index)}\n\t\t"
    #           f"dist_true:{len(data[~pd.isna(data.topo_dist)].index)}\n\t"
    #           f"b:{len(data.index)}\n\t\t"
    #           f"dist_true:{len(data[~pd.isna(data.topo_dist)].index)}")
    #     print(f"\n\nSuspicious datapoints:\n\tpublication + pdb_id / publication:\n\t\t"
    #           f"Schweppe et al. 2017: {round((len(data[(data.Publication == 'Schweppe et al. 2017') & (data.pdb_id != '-')].index) / (len(data[data.Publication == 'Schweppe et al. 2017'].index))) * 100, 2)}%"
    #           f"\n\t\tLiu et al. 2018: {round((len(data[(data.Publication == 'Liu et al. 2018') & (data.pdb_id != '-')].index) / (len(data[data.Publication == 'Liu et al. 2018'].index))) * 100, 2)}%"
    #           f"\n\tNo distance computed (total number = {len(data[pd.isna(data.topo_dist) & (data.pdb_id != '-')].index)}): {data[pd.isna(data.topo_dist) & (data.pdb_id != '-')][['unip_id_a', 'unip_id_b', 'pos_a', 'pos_b', 'topo_dist']]}"
    #           f"\n\tNot found in databases (total number = {len(data[(~struct_found)].index)}): {data[(~struct_found)][['unip_id_a', 'unip_id_b']]}"
    #           f"\n\tVery high distances (total number = {len(data[data.topo_dist >= 100].index)}): {data[data.topo_dist >= 100][['unip_id_a', 'unip_id_b', 'topo_dist']]}"
    #           f"\n\tNo distance computed but pdb_id found (total number = {len(data[~dist_calc].index)}): {data[pd.isna(data.topo_dist) & (data.pdb_id != '-')][['pdb_id', 'pos_a', 'pos_b', 'topo_dist']]}"
    #           f"\n\tVery low distances (total number = {len(data[(0 < data.topo_dist) & (data.topo_dist < 5)].index)}): {data[(0 < data.topo_dist) & (data.topo_dist < 5)][['unip_id_a', 'unip_id_b', 'topo_dist']]}")
    #     homomers_path = f'{project_path}data/out/full/homomers'
    #     structures_path = f'{project_path}data/out/full/structures'
    #     list_a = sorted([dir for dir in os.listdir(homomers_path) for f in os.listdir(f'{homomers_path}/{dir}')
    #                      if f.endswith('_.csv')])
    #     list_b_data = data[~data.swiss_model_homology.str.contains('mer', na=False) & (data.XL_type == 'inter')]
    #     list_b = sorted(list_b_data[key_a].append(list_b_data[key_b]).unique().tolist())
    #     total_dp = 2358
    #     print(f"\n\nFinal results:"
    #           f"\n\ttotal number of interactions: {len(data.index)}"
    #           f"\n\ttotal number of proteins: {len(data[key_a].append(data[key_b]).unique())}"
    #           f"\n\tnumber of downloaded structures: {len(os.listdir(structures_path))}"
    #           f"\n\tnumber of new inters: {sum(data.XL_type == 'inter')} "
    #           f"({(sum(data.XL_type == 'inter') / total_dp) * 100:.2f}%)"
    #           f"\n\tnumber of discovered homomers: {len(os.listdir(homomers_path))} "
    #           f"({(len(os.listdir(homomers_path)) / len(data[key_a].append(data[key_b]).unique())) * 100:.2f}%)"
    #           f"\n\tnumber of newly discovered homomers: {len(list_a)}\t== {len(list_b)} "
    #           f"({(len(list_a) / len(data[key_a].append(data[key_b]).unique())) * 100:.2f}%)"
    #           f"\n\t\t{list_a}\n\t\t == \n\t\t{list_b}\n\t\t-------------------------------------"
    #           f"\n\t\tunequal set: {[e for e in list_a + list_b if (e not in list_a) or (e not in list_b)]}"
    #           f"\n\thomomers with multiple possible states (possible issues?): "
    #           f"{[dir for dir in os.listdir(homomers_path) if len(os.listdir(f'{homomers_path}/{dir}')) > 2]}")
    #     if "score_XL_type" in data.columns:
    #         print(
    #             # f"\n\n{data[data[key_a].append(data[key_b]).str.contains('|'.join(['Q91VD9', 'Q9CPQ1', 'Q9DCN2', 'Q9WTP6']))].score_XL_type}"
    #             f"\n\nscore_XL_type != XL_type:"
    #             f"\n\t{data[~(data.score_XL_type == data.XL_type)][['score_XL_type', 'XL_type']]}")
    #             # f"\n\nobscurin:\n{final_data[final_data.unip_id == 'A2AAJ9'][['topo_dist', 'homo_pep_overl', 'inter_score', 'XL_type', 'swiss_model_homology']]}"
    #             # f"\n\tobscurin with inter:\n{final_data[(final_data.unip_id == 'A2AAJ9') & (final_data.XL_type == 'inter')][['topo_dist', 'homo_pep_overl', 'inter_score', 'XL_type', 'swiss_model_homology']]}")
    # else:
    #     print(f"number of unique proteins: {len(data['unip_id'].unique())}")
    #     print(f"number of homomers: {len(data[~pd.isna(data.evidence)]['unip_id'].unique())} ({100 * len(data[~pd.isna(data.evidence)]['unip_id'].unique()) / len(data['unip_id'].unique()):.2f}%)")
    #     print(f"number of known homomers: {len(data[~pd.isna(data.evidence) & ~pd.isna(data.swiss_model_homology)]['unip_id'].unique())} ({100 * len(data[~pd.isna(data.evidence) & ~pd.isna(data.swiss_model_homology)]['unip_id'].unique()) / len(data['unip_id'].unique()):.2f}% (of homomers: {100 * len(data[~pd.isna(data.evidence) & ~pd.isna(data.swiss_model_homology)]['unip_id'].unique()) / len(data[~pd.isna(data.evidence)]['unip_id'].unique()):.2f}%))")
    #     print(f"number of new homomers: {len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)]['unip_id'].unique())} ({100 * len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)]['unip_id'].unique()) / len(data['unip_id'].unique()):.2f}% (of homomers: {100 * len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)]['unip_id'].unique()) / len(data[~pd.isna(data.evidence)]['unip_id'].unique()):.2f}%))\n")
    #     print(f"number of xls for which structures were found: {len(data[struct_found].index)} ({100 * len(data[struct_found].index) / len(data.index):.2f}%)")
    #     print(f"number of xls for which no structures were found: {len(data[~struct_found].index)} ({100 * len(data[~struct_found].index) / len(data.index):.2f}%)"
    #           f"\n")
    #
    #     print(f"number of xls for which dists were computed: {len(data[~pd.isna(data.topo_dist)].index)} ({100 * len(data[~pd.isna(data.topo_dist)].index) / len(data.index):.2f}%)")
    #     print(f"\tfraction of xls for which dists were computed given a structure was found: {100 * len(data[dist_calc].index) / len(data[struct_found].index):.2f}%")
    #     print(f"number of xls for which no dists were computed: {len(data[pd.isna(data.topo_dist)].index)} ({100 * len(data[pd.isna(data.topo_dist)].index) / len(data.index):.2f}%)")
    #     print(f"\tfraction of xls for which no dists were computed given a structure was found: {100 * len(data[~dist_calc].index) / len(data[struct_found].index):.2f}%"
    #           f"\n")
    #
    #     print(f"number of intra xls in homomers: {len(data[~pd.isna(data.evidence)].index)} / {len(data.index)} ({100 * len(data[~pd.isna(data.evidence)].index) / len(data.index):.2f}%)")
    #     print(f"\tfraction of intra xls in homomers given a distance was computed: {len(data[~pd.isna(data.evidence)].index)} / {len(data[~(pd.isna(data.topo_dist))].index)} ({100 * len(data[~pd.isna(data.evidence)].index) / len(data[~(pd.isna(data.topo_dist))].index):.2f}%)")
    #     print(f"number of intra xls in new homomers: {len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)].index)} / {len(data.index)} ({100 * len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)].index) / len(data.index):.2f}%)")
    #     print(f"\tfraction of intra xls in new homomers given a distance was computed: {len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)].index)} / {len(data[~(pd.isna(data.topo_dist))].index)} ({100 * len(data[~pd.isna(data.evidence) & pd.isna(data.swiss_model_homology)].index) / len(data[~(pd.isna(data.topo_dist))].index):.2f}%)")


# nohup sh -c "python3 start01b_liu_uniprot_search.py -s True && python3 claudio_mod02_struct.py -i data/out/uniprot_search/supp_RA117.000470_133922_0_supp_23973_3zf3c5_table1.csv.sqcs -s True && python3 claudio_mod02_di.py -i2 data/out/uniprot_search/supp_RA117.000470_133922_0_supp_23973_3zf3c5_table1.csv.sqcs && python3 read_out.py" > logs/log111121_0344.log 2>&1 &

# nohup sh -c "python3 claudio_mod02_01.py && python3 claudio_mod02_struct.py && python3 claudio_mod02_di.py && python3 read_out.py" > logs/log220323_1400.log 2>&1 &

# nohup sh -c "python3 claudio_mod02_struct.py && python3 claudio_mod02_di.py && python3 read_out.py" > logs/log220204_1300.log 2>&1 &

# nohup sh -c "python3 claudio_mod02_di.py && python3 read_out.py" > logs/log220207_2000.log 2>&1 &

# nohup sh -c "python3 claudio_lists.py" > nohup.log 2>&1 &

# nohup sh -c "python3 claudio_ops.py" > nohup.log 2>&1 &

# nohup sh -c "python3 claudio_structdi.py && python3 read_out.py -i 'data/out/module02/liu18_schweppe17_linked_residues_intra-homo_2370_nonredundant.csv.sqcs.csv'" > logs/log220413_1330.log 2>&1 &

# nohup sh -c "python3 claudio_lists.py -o 'data/out/full' && python3 claudio_structdi.py -o 'data/out/full' && python3 claudio_ops.py -o 'data/out/full' && python3 claudio_xl.py -i 'data/out/full/liu18_schweppe17_linked_residues_intra-homo_2370_nonredundant.csv.sqcs.csv' -i2 'data/out/full/liu18_schweppe17_linked_residues_intra-homo_2370_nonredundant.csv_homosig.csv' -o 'data/out/full'" > logs/log220505_1230.log 2>&1 &

# nohup sh -c "python3 claudio.py -rt True" > logs/log221109_1830.log 2>&1 &
