import os
import sys
import time
import click
from importlib.metadata import version as _pkg_version

from claudio.module01.src.main import main as run_claudio_lists
from claudio.module02.run_module02_intra import main as run_claudio_structdi
from claudio.module03.src.main import main as run_claudio_ops
from claudio.module04.src.main import (
    main as run_claudio_xl, _assessment_policies,
)

from claudio.utils.utils import verbose_print, round_self, evaluate_boolean_input, clean_input_paths, create_out_path
from claudio.utils.db_updater import main as db_updater

_DEFAULT_OPTIONS = ["test/sample_data_random.csv", None,
                    "peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2",
                    False, "K,M:N:1", "blastp", 1e-5, 90.0, 50.0, 4, 70.0,
                    0.0, 35.0, None, 50.0, 0.0, "test/out/sample/", None,
                    "$HOME/BLAST/db", "claudio/data/pdbaa", "$HOME/HHSUITE/db", None, False, 2]
# ['test/sample_data_random.csv', None,
#  'peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2',
#  False, 'K,M:N:1', 'blastp', 1e-05, 90.0, 50.0, 4, 70.0, 0.0, 35.0,
#  None, 50.0, 0.0, 'test/out/sample/', None, 'claudio/data/pdbaa', None,
#  '$HOME/HHSUITE/db', None, False, 2]


def _run_stage(command, **params):
    context = click.get_current_context()
    if isinstance(command, click.Command):
        for option in command.params:
            if option.name in params:
                params[option.name] = option.type_cast_value(
                    context, params[option.name]
                )
    try:
        return context.invoke(command, **params)
    except SystemExit as error:
        if error.code not in (None, 0):
            raise


def _require_output(path):
    if not os.path.isfile(path):
        raise click.ClickException(f"Expected output was not created: {path}")


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
@click.option("--af-complex-model", default=None)
@click.option("--af-complex-auto", is_flag=True, default=False)
@click.option("-c", "--config",
              help="filepath to configuration file containing all input parameters")
@click.option(
    "--topolink-seed",
    type=click.IntRange(1, 2147483647),
    default=None,
    help="Fixed TopoLink seed; omitted values use the native input template.",
)
@click.option(
    "--euclidean-assessment",
    type=(float, float, click.Choice(["inclusive", "exclusive"])),
    default=None,
    help="Euclidean MIN MAX BOUNDARY; provide both assessment options to enable.",
)
@click.option(
    "--topological-assessment",
    type=(float, float, click.Choice(["inclusive", "exclusive"])),
    default=None,
    help="TopoLink MIN MAX BOUNDARY; provide both assessment options to enable.",
)
def main(input_filepath, input_temppath, projections, read_temps, xl_residues,
         search_tool, e_value, query_id, coverage, res_cutoff, plddt_cutoff,
         linker_minimum, linker_maximum, euclidean_strictness, distance_maximum,
         cutoff, output_directory, blast_bin, blast_db, hhsearch_bin,
         hhsearch_db, topolink_bin, compute_scoring, verbose_level, config,
         af_complex_model=None, af_complex_auto=False, topolink_seed=None,
         euclidean_assessment=None, topological_assessment=None):
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
    policies = _assessment_policies(
        euclidean_assessment, topological_assessment,
    )
    assessment_options = {}
    if policies is not None:
        assessment_options = {
            "euclidean_assessment": euclidean_assessment,
            "topological_assessment": topological_assessment,
        }
    if af_complex_auto and af_complex_model is not None:
        raise click.UsageError(
            "--af-complex-auto and --af-complex-model are mutually exclusive."
        )
    if af_complex_model is not None:
        af_complex_model = af_complex_model.strip()
        if not af_complex_model:
            raise click.BadParameter(
                "Model ID must not be empty", param_hint="--af-complex-model",
            )
    af_mode = af_complex_auto or af_complex_model is not None

    verbose_print(f"Start full CLAUDIO v{_pkg_version('CLAUDIO')} pipeline", 0, 1, start='')
    verbose_print("===================================", 0, 1, start='')
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

    input_filepath, input_temppath, output_directory, blast_bin, blast_db, hhsearch_bin, hhsearch_db, topolink_bin \
        = clean_input_paths([input_filepath, input_temppath, output_directory, blast_bin, blast_db, hhsearch_bin,
                             hhsearch_db, topolink_bin])

    read_temps = evaluate_boolean_input(read_temps)
    compute_scoring = evaluate_boolean_input(compute_scoring)
    input_temppath = input_temppath or None
    output_directory = create_out_path(output_directory, input_filepath)
    filename = os.path.splitext(os.path.basename(input_filepath))[0]
    sqcs_path = f"{output_directory}{filename}.sqcs"
    ops_path = f"{sqcs_path}_ops.csv"
    structure_path = f"{sqcs_path}_structdi.csv"
    final_path = f"{output_directory}{filename}_final.csv"

    if not af_mode:
        verbose_print("Check updates for SIFTS and pdbaa databases.",
                      0, verbose_level)
        _run_stage(
            db_updater, sifts_threshold=14, pdbaa_threshold=14,
            pdbaa_dir=blast_db,
        )

    _run_stage(
        run_claudio_lists,
        input_filepath=input_filepath, input_temppath=input_temppath,
        projections=projections, uniprot_search=not read_temps,
        xl_residues=xl_residues, search_tool=search_tool,
        output_directory=output_directory, blast_bin=blast_bin,
        blast_db=blast_db, hhsearch_bin=hhsearch_bin,
        hhsearch_db=hhsearch_db, verbose_level=verbose_level,
        skip_protein_structure_search=af_mode,
        preserve_source_records=af_mode or policies is not None,
    )
    _require_output(sqcs_path)

    _run_stage(
        run_claudio_ops, input_filepath=sqcs_path,
        output_directory=output_directory, verbose_level=verbose_level,
    )
    _require_output(ops_path)

    _run_stage(
        run_claudio_structdi,
        input_filepath=sqcs_path, input_temppath=input_temppath,
        read_temps=read_temps, search_tool=search_tool,
        xl_residues=xl_residues, plddt_cutoff=plddt_cutoff,
        linker_minimum=linker_minimum, linker_maximum=linker_maximum,
        e_value=e_value, query_id=query_id, coverage=coverage,
        res_cutoff=res_cutoff, output_directory=output_directory,
        blast_bin=blast_bin, blast_db=blast_db,
        hhsearch_bin=hhsearch_bin, hhsearch_db=hhsearch_db,
        topolink_bin=topolink_bin, verbose_level=verbose_level,
        af_complex_model=af_complex_model, af_complex_auto=af_complex_auto,
        topolink_seed=topolink_seed
    )
    _require_output(structure_path)

    _run_stage(
        run_claudio_xl,
        input_filepath=structure_path, input_filepath2=ops_path,
        plddt_cutoff=plddt_cutoff, linker_minimum=linker_minimum,
        linker_maximum=linker_maximum,
        euclidean_strictness=euclidean_strictness,
        distance_maximum=distance_maximum, cutoff=cutoff,
        output_directory=output_directory, compute_scoring=compute_scoring,
        xl_residues=xl_residues, verbose_level=verbose_level,
        **assessment_options,
    )
    _require_output(final_path)

    # AF intermediate tables retain source, model, and mapping details.
    if not af_mode:
        for path in (sqcs_path, structure_path, ops_path):
            os.remove(path)

    verbose_print(f"\nFinished full CLAUDIO pipeline execution (Total elapsed time: "
                  f"{round_self(time.time() - start_time, 2)}s)",
                  0, verbose_level, start='')
    verbose_print("===================================", 0, verbose_level, start='')

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
