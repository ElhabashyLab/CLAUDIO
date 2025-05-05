import cProfile
import os
import pstats
import sys
import time
import click

from claudio.module02.src_structure_search.io.read_input import read_in
from claudio.module02.src_structure_search.algorithm.structure_search import structure_search
from claudio.module02.src_structure_search.io.read_temp import read_temp_file
from claudio.module02.src_structure_search.algorithm.pdb_download import download_pdbs
from claudio.module02.src_structure_search.algorithm.chain_copies import create_ident_chain_copies
from claudio.module02.src_structure_search.io.write_out import write_output

from claudio.utils.utils import (verbose_print, clean_input_paths,
                                create_out_path, round_self)


@click.command()
@click.option("-i", "--input-filepath",
              default="test/out/sample/sample_data_random.sqcs")
@click.option("-it", "--input-temppath", default=None)
@click.option("-s", "--do-structure-search", default=True)
@click.option("-t", "--search-tool", default="blastp")
@click.option("-e", "--e-value", default=1e-5)
@click.option("-q", "--query-id", default=90.0)
@click.option("-c", "--coverage", default=50.0)
@click.option("-r", "--res-cutoff", default=4)
@click.option("-o", "--output-directory", default="test/out/sample")
@click.option("-bl", "--blast-bin", default=None)
@click.option("-bldb", "--blast-db", default="$BLASTDB")
@click.option("-hh", "--hhsearch-bin", default=None)
@click.option("-hhdb", "--hhsearch-db", default="$HHDB")
@click.option("-v", "--verbose-level", default=2)
def main(input_filepath, input_temppath, do_structure_search, search_tool,
         e_value, query_id, coverage, res_cutoff, output_directory, blast_bin,
         blast_db, hhsearch_bin, hhsearch_db, verbose_level):
    """
        Performs structure search as part of the structural analysis

        Parameters
        ----------
        input_filepath : str,
        input_temppath : str,
        do_structure_search : bool,
        search_tool : str,
        e_value : float,
        query_id : float,
        coverage : float,
        res_cutoff : int,
        output_directory : str,
        blast_bin : str | None,
        blast_db : str,
        hhsearch_bin : str | None,
        hhsearch_db : str,
        verbose_level : int

        Returns
        -------
        None

    """
    verbose_print("Start structure search", 0, verbose_level)
    start_time = time.time()
    profile = cProfile.Profile()
    profile.enable()   # --- start profiling

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, input_temppath, output_directory,
                     blast_bin, blast_db, hhsearch_bin, hhsearch_db]
    input_filepath, input_temppath, output_directory, blast_bin, blast_db, \
    hhsearch_bin, hhsearch_db = clean_input_paths(list_of_paths)

    # Create temporary dir
    temp_dir = create_out_path(input_temppath + "/structure_search" if input_temppath is not None else
                               output_directory + "temp/structure_search", input_filepath)

    # Check output directory
    output_directory = create_out_path(output_directory, input_filepath)

    # If parameters inputted by user valid
    if inputs_valid(input_filepath, input_temppath, do_structure_search,
                    search_tool, e_value, query_id, coverage, res_cutoff,
                    output_directory, blast_bin, blast_db, hhsearch_bin,
                    hhsearch_db, verbose_level):
        e_value = float(e_value)
        query_id = float(query_id)
        coverage = float(coverage)
        res_cutoff = float(res_cutoff)

        # Read dataset and add columns for results
        verbose_print("Read input", 0, verbose_level)
        data, filename = read_in(input_filepath)

        # If given variable do_structure_search is True perform new search,
        # else retrieve results from earlier temporary save file
        tmp_filepath = f"{temp_dir}{'.'.join(filename.split('.')[:-1])}_{search_tool}_bltmp.{filename.split('.')[-1]}"
        if (not do_structure_search) and os.path.exists(tmp_filepath):
            verbose_print("Read from temporary save file", 0, verbose_level)
            data = read_temp_file(data, tmp_filepath)
        else:
            verbose_print(f"Perform {search_tool} search", 0, verbose_level)
            data = structure_search(data, search_tool, e_value, query_id,
                                    coverage, tmp_filepath, blast_bin,
                                    blast_db, hhsearch_bin, hhsearch_db,
                                    verbose_level)

        # Download structure files from RCSB database into structures
        # subdirectory, if search tool found a proper result,
        # else use Uniprot ID in order to attempt retrieval of matching
        # AlphaFold entry
        verbose_print("Download structures from RCSB database, or AlphaFold database if not found there", 0,
                      verbose_level)
        if not os.path.exists(f"{output_directory}structures"):
            os.mkdir(f"{output_directory}structures")
        data = download_pdbs(data, search_tool, res_cutoff,
                             f"{output_directory}structures/", verbose_level)

        # Create copy datapoints with marked indeces for alternative but
        # identical chains
        data = create_ident_chain_copies(data)

        # Write new output
        write_output(data, filename, output_directory)
    runtime = round_self(time.time() - start_time, 2)
    verbose_print(f"\nEnd script (Elapsed time: {runtime}s)", 0, verbose_level)
    verbose_print("===================================", 0, verbose_level)
    profile.disable()  # --- stop profiling
    profile.create_stats()
    with open("profileM02_SS.txt", 'w', encoding="utf-8") as fp:
        stats = pstats.Stats(profile, stream=fp)
        stats.sort_stats('cumtime')
        stats.print_stats()
    sys.exit(0)


def inputs_valid(input_filepath: str, input_temppath: str,
                 do_structure_search: bool, search_tool: str, e_value: float,
                 query_id: float, coverage: float, res_cutoff: float,
                 output_directory: str, blast_bin: str | None, blast_db: str,
                 hhsearch_bin: str | None, hhsearch_db: str,
                 verbose_level: int):
    """
    check validity of inputted parameters

    Parameters
    ----------
    input_filepath : str,
    input_temppath : str,
    do_structure_search : bool,
    search_tool : str,
    e_value : float,
    query_id : float,
    coverage : float,
    res_cutoff : float,
    output_directory : str,
    blast_bin : str | None,
    blast_db : str,
    hhsearch_bin : str | None,
    hhsearch_db : str,
    verbose_level : int

    Returns 
    -------
    inputs_valid : bool

    Raises
    ------
        invalid input exceptions
    """

    # check whether an inputfile with the extension .sqcs is specified
    if input_filepath and input_filepath.endswith(".sqcs"):
        # check whether inputted search tool is either hhsearch or blastp
        if search_tool in ["blastp", "hhsearch"]:
            # check blast database path
            if (search_tool == "hhsearch") or os.path.exists(str(blast_db) + "pdbaa.phr"):
                # check hhsearch database path
                if (search_tool == "blastp") or os.path.exists(str(hhsearch_db) + "pdb70_a3m.ffdata"):
                    # check whether value given for e-value can be turned into
                    # a float variable
                    try:
                        e_value = float(e_value)
                        # check whether e-value is a value between 0 and 1
                        if 0 < e_value < 1:
                            # check whether value given for query identity
                            # can be turned into a float variable
                            try:
                                query_id = float(query_id)
                                # check whether query identity is a value
                                # in [0,100]
                                if 0 <= query_id <= 100:
                                    # check whether value given for coverage
                                    # can be turned into a float variable
                                    try:
                                        coverage = float(coverage)
                                        # check whether coverage is a value
                                        #  in [0,100]
                                        if 0 <= coverage <= 100:
                                            try:
                                                # check whether value given
                                                #  for resolution cutoff can
                                                # be turned into a float variable
                                                res_cutoff = float(res_cutoff)
                                                return True
                                            except:
                                                raise Exception(f"Error! Given value for resolution cutoff could not "
                                                                f"be turned into a float variable (given: "
                                                                f"{res_cutoff}).")
                                        else:
                                            raise Exception(f"Error! Given coverage is not within allowed interval of "
                                                            f"[0,100] (given: {coverage}).")
                                    except:
                                        raise Exception(f"Error! Given value for coverage could not be turned into a "
                                                        f"float variable (given: {coverage}")
                                else:
                                    raise Exception(f"Error! Given query identity is not within allowed interval of "
                                                    f"[0,100] (given: {query_id}).")
                            except:
                                raise Exception(f"Error! Given value for query identity could not be turned into a "
                                                f"float variable (given: {query_id}")
                        else:
                            raise Exception(f"Error! Given e-value is not within allowed interval of (0,1) "
                                            f"(given: {e_value}).")
                    except:
                        raise Exception(f"Error! Given value for e-value could not be turned into a float variable "
                                        f"(given: {e_value}")
                else:
                    raise Exception(f"Error! Could not find 'pdb70_a3m.ffdata' in given hhsearch database directory "
                                    f"(given: {hhsearch_db}).")
            else:
                raise Exception(f"Error! Could not find 'pdbaa.phr'-File in given blast database directory "
                                f"(given: {blast_db}).")
        else:
            raise Exception(f"Error! Invalid search tool selected (given: {search_tool}).")
    else:
        raise Exception(f"Error! The parameter \"input-filepath\" was not given or was not ending with the '.sqcs' "
                        f"extension (given: {input_filepath}).")
