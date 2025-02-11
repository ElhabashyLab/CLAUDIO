import os
import click
import time
import sys
import cProfile, pstats

from claudio.module02.src_distance_reevaluation.io.read_uniprot_search_out import read_unipsearch_out
from claudio.module02.src_distance_reevaluation.algorithm.search_pdb_pos import search_site_pos_in_pdb
from claudio.module02.src_distance_reevaluation.algorithm.calc_site_distances import calculate_site_dists
from claudio.module02.src_distance_reevaluation.io.write_out import write_output
from claudio.module02.src_distance_reevaluation.algorithm.create_plots import create_histogram

from claudio.utils.utils import verbose_print, create_out_path, clean_input_paths, build_xl_dataset, clean_dataset, \
    round_self


@click.command()
@click.option("-i", "--input-directory", default="test/out/sample/structures")
@click.option("-i2", "--input-filepath", default="test/out/sample/sample_data_random.sqcs_structdi.csv")
@click.option("-it", "--input-temppath", default=None)
@click.option("-t", "--search-tool", default="blastp")
@click.option("-x", "--xl-residues", default="K,M:N:1")
@click.option("-p", "--plddt-cutoff", default=70.0)
@click.option("-lmin", "--linker-minimum", default=5.0)
@click.option("-lmax", "--linker-maximum", default=35.0)
@click.option("-o", "--output-directory", default="test/out/sample")
@click.option("-tl", "--topolink-bin", default=None)
@click.option("-v", "--verbose-level", default=2)
def main(input_directory, input_filepath, input_temppath, search_tool, xl_residues, plddt_cutoff, linker_minimum,
         linker_maximum, output_directory, topolink_bin, verbose_level):
    verbose_print("Start intra interaction check", 0, verbose_level)
    start_time = time.time()
    profile = cProfile.Profile()
    profile.enable()   # --- start profiling

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, input_temppath, output_directory, topolink_bin]
    input_filepath, input_temppath, output_directory, topolink_bin = clean_input_paths(list_of_paths)

    # Check output directory
    output_directory = create_out_path(output_directory, input_filepath)

    # Create temporary dir
    temp_dir = create_out_path(input_temppath + "/dist_reeval" if input_temppath is not None else
                               output_directory + "temp/dist_reeval", input_filepath)

    # If parameters inputted by user valid
    if inputs_valid(input_directory, input_filepath, search_tool, xl_residues, plddt_cutoff, output_directory,
                    topolink_bin, verbose_level):
        # Define dataset for crosslink residues including possible positions and atom types
        df_xl_res = build_xl_dataset(xl_residues)

        # Read result from uniprot_search, e.g. sqcs-file
        verbose_print("Read peptide information from uniprot search results", 0, verbose_level)
        data = read_unipsearch_out(input_filepath)

        # Search for site positions in pdb files (replace rcsb pdb with alphafold, if not able to find it there)
        verbose_print("Search site pos in pdb files (replace rcsb-pdb with alphafold-pdb if needed)", 0, verbose_level)
        data = search_site_pos_in_pdb(data, df_xl_res, verbose_level)

        # Compute distances of sites, and if distance calculation successful compute new xl_type
        verbose_print("Calculate presumed interaction site distances and evaluate interaction likelihood", 0,
                      verbose_level)
        data = calculate_site_dists(data, temp_dir, df_xl_res, plddt_cutoff, topolink_bin, verbose_level)

        # Clean dataset for output
        data = clean_dataset(data)

        # Plot histograms of distances
        verbose_print("Create distance histograms", 0, verbose_level)
        create_histogram(data, input_filepath.split('/')[-1], output_directory, linker_minimum, linker_maximum)

        # Overwrite previous outputfile of module02
        verbose_print("Overwrite outputfile", 0, verbose_level)
        write_output(data, input_filepath)

    verbose_print(f"\nEnd script (Elapsed time: {round_self(time.time() - start_time, 2)}s)", 0, verbose_level)
    verbose_print("===================================", 0, verbose_level)
    
    profile.disable()  # --- stop profiling
    profile.create_stats()
    with open("profileM02_DR.txt", 'w') as fp:
        stats = pstats.Stats(profile, stream=fp)
        stats.sort_stats('cumtime')
        stats.print_stats()
    sys.exit(0)


def inputs_valid(input_directory: str, input_filename: str, search_tool: str, xl_residues: str, plddt_cutoff: float, output_directory: str,
                 topolink_bin: str | None, verbose_level: int):
    """
    check validity of inputted parameters

    Parameters
    ----------
    input_directory : str,
    input_filename : str,
    search_tool : str,
    xl_residues : str,
    plddt_cutoff : float,
    output_directory : str,
    topolink_bin : str | None,
    verbose_level : int
    
    Returns
    -------
    inputs_valid : bool

    Raises
    ------
        Invalid input parameters exceptions
    """

    if any([".pdb" in filename for filename in os.listdir(input_directory)]):
        if input_filename.endswith(".sqcs_structdi.csv"):
            if search_tool in ["blastp", "hhsearch"]:
                # check whether xl_residues can be turned into a proper DataFrame, else return False
                build_xl_dataset(xl_residues)
                # check whether plddt cutoff has valid value
                try:
                    plddt_cutoff = float(plddt_cutoff)
                    if 0 <= plddt_cutoff <= 100:
                        return True
                    else:
                        raise Exception(f"pLDDT cutoff value should be in [0, 100] (given: {plddt_cutoff}).")
                except:
                    raise Exception(f"Value given for pLDDT cutoff should be possible to turn into a float "
                                    f"(given: {plddt_cutoff}).")
            else:
                raise Exception(f"Error! Invalid search tool! (given: {search_tool})")
        else:
            raise Exception(f"Error! Given inputfile (-i2) extension hints at incorrect output of uniprot-search "
                            f"(given: {input_filename})!")
    else:
        print(f"Warning! No structure files created by structure_search tool found (given: {input_directory})!")
        return True
