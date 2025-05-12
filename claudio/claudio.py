import cProfile
import os
import pstats
import sys
import time
import click
import pkg_resources

from claudio.module01.src.main import main as run_claudio_lists
from claudio.module02.run_module02_intra import main as run_claudio_structdi
from claudio.module03.src.main import main as run_claudio_ops
from claudio.module04.src.main import main as run_claudio_xl

from claudio.utils.utils import verbose_print, round_self, evaluate_boolean_input

_DEFAULT_OPTIONS = ["test/sample_data_random.csv", None,
                    "peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2",
                    False, "K,M:N:1", "blastp", 1e-5, 90.0, 50.0, 4, 70.0,
                    0.0, 35.0, None, 50.0, 0.0, "test/out/sample/", None,
                    "$HOME/BLAST/db", None, "$HOME/HHSUITE/db", None, False, 2]
# ['test/sample_data_random.csv', None,
#  'peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2',
#  False, 'K,M:N:1', 'blastp', 1e-05, 90.0, 50.0, 4, 70.0, 0.0, 35.0,
#  None, 50.0, 0.0, 'test/out/sample/', None, '$HOME/BLAST/db', None,
#  '$HOME/HHSUITE/db', None, False, 2]


@click.command()
@click.option("-i", "--input-filepath", help="path to inputfile")
@click.option("-it", "--input-temppath",
              help="path to directory for temporary files")
@click.option("-p", "--projections",
              help="comma-separated position-sensitive list that names the column names of the users dataset\ncontaining the necessary information for the tool. The column names should contain and\nshould be given in the following order: crosslinked peptide_a, crosslinked peptide_b,\ncrosslinked residue position_a, crosslinked residue position_b, position of cross-linked\nresidue in peptide_a, position of cross-linked residue in peptide_b, UniProt ID of\nprotein belonging to peptide_a, UniProt ID of protein belonging to peptide_b.\nNote: The positions of the crosslinked residue in the peptides are information only\naccessed, if the given full sequence positions do not match into the retrieved UniProt\nsequence. If the positions are confirmed you may simply create two substitute columns\nfor the positions in the peptides instead and leave them empty.")
@click.option("-rt", "--read-temps",
              help="if the tool has been run before with the same input a temporary file was saved, which\ncan be used to skip some of the steps")
@click.option("-x", "--xl-residues",
              help="comma-separated one-letter-code residues, optional: add two ':' after the\none-letter-code symbol of the residue in order to specify full sequence position\n(either 1 for start, or -1 for end position) and/or the atom used for the distance\ncomputation")
@click.option("-t", "--search-tool",
              help="always set to \"blastp\" (as of this version), specifying the tool which should be used for pdb search")
@click.option("-e", "--e-value",
              help="e-value used in structure search")
@click.option("-qi", "--query-id",
              help="query identity used in structure search")
@click.option("-cv", "--coverage",
              help="coverage used in structure search")
@click.option("-r", "--res-cutoff",
              help="float value used as cutoff in angstrom for resolution of structure files")
@click.option("-pc", "--plddt-cutoff",
              help="float value used as cutoff for alphafold structure prediction confidences (plddt)")
@click.option("-lmin", "--linker-minimum",
              help="float value used as minimal crosslinker range in angstrom")
@click.option("-lmax", "--linker-maximum",
              help="float value used as maximal crosslinker range in angstrom")
@click.option("-es", "--euclidean-strictness",
              help="float value substracted from the linker ranges for the euclidean distance scoring\n(minimum will not go below 0)")
@click.option("-dm", "--distance-maximum",
              help="maximal distance value that seems realistic, if surpassed the distance will be set to\nthis value during the confidence scoring, to ensure its consistency")
@click.option("-ct", "--cutoff",
              help="float value used as confidence score cutoff, if surpassed, the linker type will be set\nto inter")
@click.option("-o", "--output-directory",
              help="output directory for produced csv-files")
@click.option("-bl", "--blast-bin",
              help="binary directory in blast installation, or None if binary directory has been added to\nPATH variable (e.g. if blast can be called from anywhere)")
@click.option("-bldb", "--blast-db",
              help="database directory for blast installation")
@click.option("-hh", "--hhsearch-bin",
               help="binary directory in hh-suite installation, or None if binary directory has been added to\nPATH variable (e.g. if hhsearch can be called from anywhere)")
@click.option("-hhdb", "--hhsearch-db",
              help="database directory for hh-suite installation")
@click.option("-tl", "--topolink-bin",
              help="binary directory in topolink installation, or None if binary directory has been added to\nPATH variable (e.g. if topolink can be called from anywhere)")
@click.option("-s", "--compute-scoring",
              help="boolean, for whether experimental scoring and resulting XL-type evluations should be\ncomputed and appended to result dataset")
@click.option("-v", "--verbose-level",
              help="verbose level value")
@click.option("-c", "--config",
              help="filepath to configuration file containing all input parameters")
def main(input_filepath, input_temppath, projections, read_temps, xl_residues,
         search_tool, e_value, query_id, coverage, res_cutoff, plddt_cutoff,
         linker_minimum, linker_maximum, euclidean_strictness, distance_maximum,
         cutoff, output_directory, blast_bin, blast_db, hhsearch_bin,
         hhsearch_db, topolink_bin, compute_scoring, verbose_level, config):
    """
    
    wrapper function for the full CLAUDIO pipeline, which includes the following modules:
    - Module01: uniprot_search
    - Module02: structural_analysis
    - Module03: ops_analysis
    - Module04: distance_reevaluation

    Parameters
    ----------
    input_filepath : str,
    input_temppath : str,
    projections : str,
    read_temps : bool,
    xl_residues : str,
    search_tool : str,
    e_value : float,
    query_id : float,
    coverage : float,
    res_cutoff : int,
    plddt_cutoff : float,
    linker_minimum : float,
    linker_maximum : float,
    euclidean_strictness : float | None,
    distance_maximum : float ,
    cutoff : float,
    output_directory : str,
    blast_bin : str | None,
    blast_db : str,
    hhsearch_bin : str | None,
    hhsearch_db : str,
    topolink_bin : str | None,
    compute_scoring : bool,
    verbose_level : int,
    config : str

    Returns
    -------
    None

    """
    profile = cProfile.Profile()
    profile.enable()   # --- start profiling
    verbose_print(f"Start full CLAUDIO v{pkg_resources.require('CLAUDIO')[0].version} pipeline", 0, 1)
    verbose_print("===================================", 0, 1)
    start_time = time.time()

    params = [input_filepath, input_temppath, projections, read_temps,
              xl_residues, search_tool, e_value, query_id, coverage,
              res_cutoff, plddt_cutoff, linker_minimum, linker_maximum,
              euclidean_strictness, distance_maximum, cutoff,
              output_directory, blast_bin, blast_db, hhsearch_bin,
              hhsearch_db, topolink_bin, compute_scoring, verbose_level,
              config]

    input_filepath, input_temppath, projections, read_temps, xl_residues, search_tool, e_value, query_id,\
        coverage, res_cutoff, plddt_cutoff, linker_minimum, linker_maximum, euclidean_strictness,\
        distance_maximum, cutoff, output_directory, blast_bin, blast_db, hhsearch_bin, hhsearch_db,\
        topolink_bin, compute_scoring, verbose_level \
        = parse_params(params)

    filename = '.'.join(input_filepath.split('/')[-1].split('.')[:-1])

    # Run Module01
    try:
        run_claudio_lists(["-i", input_filepath, "-it", input_temppath,
                           "-p", projections, "-s", not read_temps,
                           "-x", xl_residues, "-t", search_tool,
                           "-o", output_directory, "-bl", blast_bin,
                           "-bldb", blast_db, "-hh", hhsearch_bin,
                           "-hhdb", hhsearch_db, "-v", verbose_level])
    except SystemExit:
        pass
    if not os.path.exists(f"{output_directory}{filename}.sqcs"):
        sys.exit(1)

    # Run Module03
    try:
        run_claudio_ops(["-i", f"{output_directory}{filename}.sqcs",
                         "-o", output_directory, "-v", verbose_level])
    except SystemExit:
        pass
    if not os.path.exists(f"{output_directory}{filename}.sqcs_ops.csv"):
        sys.exit(1)

    # Run Module02
    try:
        run_claudio_structdi(["-i", f"{output_directory}{filename}.sqcs",
                              "-it", input_temppath, "-rt", read_temps,
                              "-t", search_tool, "-x", xl_residues,
                              "-pc", plddt_cutoff, "-lmin", linker_minimum,
                              "-lmax", linker_maximum, "-e", e_value,
                              "-qi", query_id, "-c", coverage,
                              "-r", res_cutoff, "-o", output_directory,
                              "-bl", blast_bin, "-bldb", blast_db,
                              "-hh", hhsearch_bin, "-hhdb", hhsearch_db,
                              "-tl", topolink_bin, "-v", verbose_level])
    except SystemExit:
        pass
    if not os.path.exists(f"{output_directory}{filename}.sqcs_structdi.csv"):
        sys.exit(1)

    # Run Module04
    try:
        if os.path.exists(f"{output_directory}{filename}.sqcs_structdi.csv") and \
                os.path.exists(f"{output_directory}{filename}.sqcs_ops.csv"):
            run_claudio_xl(["-i",
                            f"{output_directory}{filename}.sqcs_structdi.csv",
                            "-i2",
                            f"{output_directory}{filename}.sqcs_ops.csv",
                            "-p", plddt_cutoff, "-lmin", linker_minimum,
                            "-lmax", linker_maximum,
                            "-es", euclidean_strictness,
                            "-dm", distance_maximum, "-c", cutoff,
                            "-o", output_directory, "-s", compute_scoring,
                            "-v", verbose_level])
    except SystemExit:
        if os.path.exists(f"{output_directory}{filename}_final.csv"):
            os.remove(f"{output_directory}{filename}.sqcs")
            os.remove(f"{output_directory}{filename}.sqcs_structdi.csv")
            os.remove(f"{output_directory}{filename}.sqcs_ops.csv")
        pass

    verbose_print(f"\nEnd full CLAUDIO pipeline execution (Total elapsed time: "
                  f"{round_self(time.time() - start_time, 2)}s)",
                  0, verbose_level)
    verbose_print("===================================", 0, verbose_level)
    profile.disable()  # --- stop profiling
    profile.create_stats()
    with open("profile.txt", 'w', encoding="utf-8") as fp:
        stats = pstats.Stats(profile, stream=fp)
        stats.sort_stats('cumtime')
        stats.print_stats()
    sys.exit(0)


def parse_params(params: list[str]):
    """
    Parse input parameters, and differentiate whether it is given by the user,
    by the config, or is supposed to be default
    
    Parameters
    ----------
    params : list[str]

    Returns
    -------
    params : list[str]
    """

    # If configuration file given, parse its parameters
    if params[-1]:
        params[-1] = params[-1].replace('\\', '/')
        verbose_print("Configuration file given", 0, 1)
        config_params = read_config(params[-1], params[:-1])

    # If parameter is unspecified and config given, use config,
    # else if unspecified and no config use default, if
    # specified use given value
    for i, param in enumerate(params[:-1]):
        if (param is None) and params[-1]:
            params[i] = config_params[i]
        elif param is None:
            params[i] = _DEFAULT_OPTIONS[i]
        elif param != _DEFAULT_OPTIONS[i]:
            params[i] = param.replace('\\', '/')

    # add '/' to output_directory and turn verbose_level into integer
    if not params[16].endswith('/'):
        params[16] += '/'
    params[-2] = int(params[-2])

    return params[:-1]


def read_config(path: str, args: list[str]):
    """
    read configuration file from path, compare already set values to defaults
    thus checking whether params were given additionally to the config-file 
    and set values for other input parameters
    
    Parameters
    ----------
    path : str,
    args : list[str]

    Returns
    -------
    final_params : list[Any]
    """

    with open(path, 'r', encoding="utf-8") as f:
        config_content = f.read()
        input_lines = [l.replace('"', "'").replace(" = ", "=").replace("= ", "=").replace(" =", "=")
                       for l in config_content.split('\n')
                       if l and not l.startswith('#')]
        line_markers = ["input_filepath=", "input_temppath=", "projections=",
                        "read_temps=", "xl_residues=", "search_tool=", 
                        "e_value=", "query_id=", "coverage=", "res_cutoff=", 
                        "plddt_cutoff=", "linker_minimum=", "linker_maximum=",
                        "euclidean_strictness=", "distance_maximum=", 
                        "cutoff=", "output_directory=", "blast_bin=", 
                        "blast_db=", "hhsearch_bin=", "hhsearch_db=",
                        "topolink_bin=", "compute_scoring=", "verbose_level="]
        config_params = {marker: l[len(marker):]
                         for marker in line_markers for l in input_lines
                         if l.startswith(marker)}

        # Check whether boolean params can be correctly converted
        config_params["read_temps="] = evaluate_boolean_input(config_params["read_temps="])
        config_params["compute_scoring="] = evaluate_boolean_input(config_params["compute_scoring="])

        # Check whether already given args have default value
        defaults = _DEFAULT_OPTIONS.copy()

        # define dicts using line markers as keys, for arguments and
        # default values
        defaults = {marker: defaults[i]
                    for i, marker in enumerate(line_markers)}
        args = {marker: args[i] for i, marker in enumerate(line_markers)}

        # define dict containing booleans for each line marker,
        # if already given argument has default value
        arg_is_default = {marker: args[marker] == defaults[marker]
                          for marker in line_markers}

        # define final params, if already given argument is not default,
        # it takes precedence over param value in config-file
        final_params = [config_params[marker]
                        if (marker in config_params.keys()) and (args[marker] is None) else
                        args[marker] if not arg_is_default[marker] else
                        defaults[marker]
                        for marker in line_markers]

        return final_params


if __name__ == "__main__":
    main()
