"""Main script fo Module02, performs structural analysis using structure search and 
distance evaluation submodules."""
import sys
import click
import os
from claudio.module02.src_structure_search.main import main as run_structure_search
from claudio.module02.src_distance_reevaluation.main import main as run_distance_analysis

from claudio.utils.utils import (
    clean_input_paths,
    evaluate_boolean_input,
    create_out_path,
)
def _run_stage(command, **params):
    try:
        return click.get_current_context().invoke(command, **params)
    except SystemExit as error:
        if error.code not in (None, 0):
            raise

@click.command()
@click.option("-i", "--input-filepath",
              default="test/out/sample/sample_data_random.sqcs")
@click.option("-it", "--input-temppath", default="")
@click.option("-rt", "--read-temps", default=False)
@click.option("-t", "--search-tool", default="blastp")
@click.option("-x", "--xl-residues", default="K,M:N:1")
@click.option("-pc", "--plddt-cutoff", default=70.0)
@click.option("-lmin", "--linker-minimum", default=5.0)
@click.option("-lmax", "--linker-maximum", default=35.0)
@click.option("-e", "--e-value", default=1e-5)
@click.option("-qi", "--query-id", default=90.0)
@click.option("-c", "--coverage", default=50.0)
@click.option("-r", "--res-cutoff", default=4)
@click.option("-o", "--output-directory", default="test/out/sample")
@click.option("-bl", "--blast-bin", default=None)
@click.option("-bldb", "--blast-db", default="claudio/data/pdbaa")
@click.option("-hh", "--hhsearch-bin", default=None)
@click.option("-hhdb", "--hhsearch-db", default="$HHDB")
@click.option("-tl", "--topolink-bin", default=None)
@click.option("-v", "--verbose-level", default=2)
@click.option("--af-complex-model", default=None)
@click.option("--af-complex-auto", is_flag=True, default=False)
def main(input_filepath, input_temppath, read_temps, search_tool, xl_residues,
         plddt_cutoff, linker_minimum, linker_maximum, e_value, query_id,
         coverage, res_cutoff, output_directory, blast_bin, blast_db,
         hhsearch_bin, hhsearch_db, topolink_bin, verbose_level,
         af_complex_model=None, af_complex_auto=False):
    """
    Performs structural analysis using structure search and distance evaluation submodules
    
    Parameters
    ----------
    input_filepath : str,
    input_temppath : str,
    read_temps : bool,
    search_tool : str,
    xl_residues : str,
    plddt_cutoff : float,
    linker_minimum : float,
    linker_maximum : float,
    e_value : float,
    query_id : float,
    coverage : float,
    res_cutoff : int,
    output_directory : str,
    blast_bin : str | None,
    blast_db : str,
    hhsearch_bin : str | None,
    hhsearch_db : str,
    topolink_bin : str | None,
    verbose_level : int

    Returns
    -------
    None

    """
    if af_complex_auto and af_complex_model is not None:
        raise click.UsageError(
            "--af-complex-auto and --af-complex-model are mutually exclusive."
        )
    if af_complex_model is not None:
        af_complex_model = af_complex_model.strip()
        if not af_complex_model:
            raise click.BadParameter(
                "Model ID must not be empty",
                param_hint="--af-complex-model",
            )

    input_temppath = input_temppath or None
    paths = clean_input_paths([
        input_filepath, input_temppath, output_directory,
        blast_bin, blast_db, hhsearch_bin, hhsearch_db, topolink_bin,
    ])
    (
        input_filepath, input_temppath, output_directory,
        blast_bin, blast_db, hhsearch_bin, hhsearch_db, topolink_bin,
    ) = paths
    read_temps = evaluate_boolean_input(read_temps)
    output_directory = create_out_path(output_directory, input_filepath)
    structures_directory = create_out_path(
        output_directory + "structures", input_filepath
    )
    filename = input_filepath.split('/')[-1]
    output_filepath = f"{output_directory}{filename}_structdi.csv"

    _run_stage(
        run_structure_search,
        input_filepath=input_filepath,
        input_temppath=input_temppath,
        do_structure_search=not read_temps,
        search_tool=search_tool,
        e_value=e_value, query_id=query_id, coverage=coverage,
        res_cutoff=res_cutoff, output_directory=output_directory,
        blast_bin=blast_bin, blast_db=blast_db,
        hhsearch_bin=hhsearch_bin, hhsearch_db=hhsearch_db,
        verbose_level=verbose_level,
        af_complex_model=af_complex_model,
        af_complex_auto=af_complex_auto,
    )
    if not os.path.isfile(output_filepath):
        raise click.ClickException(
            f"Structure search output was not created: {output_filepath}"
        )

    _run_stage(
        run_distance_analysis,
        input_directory=structures_directory,
        input_filepath=output_filepath,
        input_temppath=input_temppath,
        search_tool=search_tool,
        xl_residues=xl_residues,
        plddt_cutoff=plddt_cutoff,
        linker_minimum=linker_minimum,
        linker_maximum=linker_maximum,
        output_directory=output_directory,
        topolink_bin=topolink_bin,
        verbose_level=verbose_level,
    )
    sys.exit(0)