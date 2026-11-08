"""Main script for the distance evaluation submodule of Module02's structural analysis.
Computes distances between observed crosslink sites in 3D structures and evaluates
the likelihood of interactions based on these distances."""
import os
import sys
import time
import click
import pandas as pd
from claudio.module02.src_distance_reevaluation.algorithm.af_complex_distances import (
    calculate_complex_site_dists,
)
from claudio.module02.src_distance_reevaluation.io.read_uniprot_search_out import read_unipsearch_out
from claudio.module02.src_distance_reevaluation.algorithm.search_pdb_pos import search_site_pos_in_pdb
from claudio.module02.src_distance_reevaluation.algorithm.calc_site_distances import calculate_site_dists
from claudio.module02.src_distance_reevaluation.io.write_out import write_output
from claudio.module02.src_distance_reevaluation.algorithm.create_plots import create_histogram

from claudio.utils.utils import (verbose_print, create_out_path, clean_input_paths,
                                 build_xl_dataset, clean_dataset, round_self)


@click.command()
@click.option("-i", "--input-directory", default="test/out/sample/structures")
@click.option("-i2", "--input-filepath",
              default="test/out/sample/sample_data_random.sqcs_structdi.csv")
@click.option("-it", "--input-temppath", default=None)
@click.option("-t", "--search-tool", default="blastp")
@click.option("-x", "--xl-residues", default="K,M:N:1")
@click.option("-p", "--plddt-cutoff", default=70.0)
@click.option("-lmin", "--linker-minimum", default=5.0)
@click.option("-lmax", "--linker-maximum", default=35.0)
@click.option("-o", "--output-directory", default="test/out/sample")
@click.option("-tl", "--topolink-bin", default=None)
@click.option("-v", "--verbose-level", default=2)
def main(input_directory, input_filepath, input_temppath, search_tool,
         xl_residues, plddt_cutoff, linker_minimum, linker_maximum,
         output_directory, topolink_bin, verbose_level):
    """
    Performs distance evaluation as part of the structural analysis
    
    Parameters
    ----------
    input_directory : str,
    input_filepath : str,
    input_temppath : str,
    search_tool : str,
    xl_residues : str,
    plddt_cutoff : float,
    linker_minimum : float,
    linker_maximum : float,
    output_directory : str,
    topolink_bin : str | None,
    verbose_level : int

    Returns
    -------
    None

    """
    verbose_print("[3.2] Start Structural Analysis", 0, verbose_level, start='')
    start_time = time.time()

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, input_temppath, output_directory,
                     topolink_bin]
    input_filepath, input_temppath, output_directory, topolink_bin = clean_input_paths(list_of_paths)

    # Check output directory
    output_directory = create_out_path(output_directory, input_filepath)

    # Create temporary dir
    temp_dir = create_out_path(input_temppath + "/dist_reeval" if input_temppath is not None else
                               output_directory + "temp/dist_reeval", input_filepath)

    # If parameters inputted by user valid
    if inputs_valid(input_directory, input_filepath, search_tool, xl_residues,
                    plddt_cutoff, output_directory, topolink_bin,
                    verbose_level):
        # Define dataset for crosslink residues including possible positions
        # and atom types
        df_xl_res = build_xl_dataset(xl_residues)

        # Read result from uniprot_search, e.g. sqcs-file
        verbose_print("Read peptide information from uniprot search results",
                      0, verbose_level)
        data = read_unipsearch_out(input_filepath)

        # Select the distance engine for each candidate row.
        if "structure_backend" in data.columns:
            _known_backends = data["structure_backend"].isin(
                ["af_complex", "legacy"]
            )
            if not _known_backends.all():
                raise ValueError(
                    "Unknown or missing structure_backend value."
                )

            _af_mask = data["structure_backend"].eq("af_complex")

        elif "af_match_status" in data.columns:
            # Support result files written before structure_backend existed.
            _af_mask = data["af_match_status"].notna()

        else:
            _af_mask = pd.Series(False, index=data.index)

        _results = []

         # Process empty AF tables too, so output headers are preserved.
        if _af_mask.any() or (
            data.empty and "af_match_status" in data.columns
        ):
            verbose_print(
                "Map AF complex sites and calculate distances",
                0, verbose_level,
            )
            _af_data = calculate_complex_site_dists(
                data.loc[_af_mask].copy(),
                temp_dir,
                xl_residues,
                plddt_cutoff,
                topolink_bin,
                verbose_level,
            )
            _af_data["eucl_dist"] = _af_data.pop("eucl_dist_tplk")
            _af_data["topo_dist"] = _af_data.pop("topo_dist_tplk")
            _results.append(_af_data)

        if (~_af_mask).any():
            verbose_print(
                "Search site pos in pdb files",
                0, verbose_level,
            )
            _legacy_data = search_site_pos_in_pdb(
                data.loc[~_af_mask].copy(),
                df_xl_res,
                verbose_level,
            )
            verbose_print(
                "Calculate structural site distances",
                0, verbose_level,
            )
            _legacy_data = calculate_site_dists(
                _legacy_data,
                temp_dir,
                df_xl_res,
                plddt_cutoff,
                topolink_bin,
                verbose_level,
            )
            _legacy_data = clean_dataset(_legacy_data)
            _results.append(_legacy_data)

        if _results:
            data = pd.concat(_results, sort=False)

        # Plot histograms of distances
        if not data.empty:
            verbose_print("Create distance histograms", 0, verbose_level)
            create_histogram(
                data, input_filepath.split('/')[-1], output_directory,
                linker_minimum, linker_maximum,
            )
        # Overwrite previous outputfile of module02
        verbose_print("Overwrite outputfile", 0, verbose_level)
        write_output(data, input_filepath)
    runtime = round_self(time.time() - start_time, 2)
    verbose_print(f"Finished successfully (Elapsed time: {runtime}s)", 0, verbose_level, start='')
    verbose_print("===================================", 0, verbose_level, start='')

    sys.exit(0)


def inputs_valid(input_directory: str, input_filename: str, search_tool: str,
                 xl_residues: str, plddt_cutoff: float, output_directory: str,
                 topolink_bin: str | None, verbose_level: int):
    """Validate options for PDB, mmCIF, and no-model inputs."""
    if not os.path.isdir(input_directory):
        raise FileNotFoundError(
            f"Structure directory does not exist: {input_directory}"
        )
    if not input_filename.endswith(".sqcs_structdi.csv"):
        raise RuntimeError(
            f"Expected a .sqcs_structdi.csv input: {input_filename}"
        )
    if search_tool not in ("blastp", "hhsearch"):
        raise ValueError(f"Invalid search tool: {search_tool}")

    build_xl_dataset(xl_residues)
    try:
        cutoff = float(plddt_cutoff)
    except (TypeError, ValueError) as error:
        raise TypeError("pLDDT cutoff must be a number") from error
    if not 0 <= cutoff <= 100:
        raise ValueError("pLDDT cutoff must be between 0 and 100")
    return True