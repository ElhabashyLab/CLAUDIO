import click
import sys

from module02.src_structure_search.main import main as run_structure_search
from module02.src_distance_reevaluation.main import main as run_distance_analysis

from utils.utils import *


@click.command()
@click.option("-i", "--input-filepath", default="data/out/unique_protein_list/sample_data.sqcs")
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
@click.option("-r", "--res-cutoff", default=6.5)
@click.option("-o", "--output-directory", default="data/out/module02")
@click.option("-bl", "--blast-bin", default=None)
@click.option("-bldb", "--blast-db", default="$BLASTDB")
@click.option("-hh", "--hhsearch-bin", default=None)
@click.option("-hhdb", "--hhsearch-db", default="$HHDB")
@click.option("-tl", "--topolink-bin", default=None)
@click.option("-v", "--verbose-level", default=2)
def main(input_filepath, input_temppath, read_temps, search_tool, xl_residues, plddt_cutoff, linker_minimum,
         linker_maximum, e_value, query_id, coverage, res_cutoff, output_directory, blast_bin, blast_db, hhsearch_bin,
         hhsearch_db, topolink_bin, verbose_level):

    # Translate eventual windows paths and evaluate value of boolean inputs
    input_filepath, input_temppath, output_directory, blast_bin, blast_db, hhsearch_bin, hhsearch_db, topolink_bin = \
        translate_windowsos_path(
            [input_filepath, input_temppath, output_directory, blast_bin, blast_db, hhsearch_bin, hhsearch_db,
             topolink_bin]
        )
    read_temps = evaluate_boolean_input(read_temps)

    if not output_directory.endswith('/'):
        output_directory += '/'

    filename = input_filepath.split('/')[-1]
    try:
        run_structure_search(["-i", input_filepath, "-it", input_temppath, "-s", not read_temps, "-t", search_tool,
                              "-e", e_value, "-q", query_id, "-c", coverage, "-r", res_cutoff, "-o", output_directory,
                              "-bl", blast_bin, "-bldb", blast_db, "-hh", hhsearch_bin, "-hhdb", hhsearch_db,
                              "-v", verbose_level])
    except SystemExit:
        pass
    try:
        run_distance_analysis(["-i", f"{output_directory}structures",
                               "-i2", f"{output_directory}{filename}_structdi.csv", "-it", input_temppath,
                               "-t", search_tool, "-x", xl_residues, "-p", plddt_cutoff, "-lmin", linker_minimum,
                               "-lmax", linker_maximum, "-o", output_directory, "-tl", topolink_bin,
                               "-v", verbose_level])
    except SystemExit:
        pass

    sys.exit()