import cProfile
import pstats
import sys
import time
import click

from claudio.module03.src.io.read_in import read_in
from claudio.module03.src.algorithm.signal_analysis import analyse_homo_signals
from claudio.module03.src.algorithm.create_histograms import create_homo_signal_histograms
from claudio.module03.src.io.write_out import write_output

from claudio.utils.utils import (verbose_print, clean_input_paths,
                                 create_out_path, clean_dataset, round_self)


@click.command()
@click.option("-i", "--input-filepath",
              default="test/out/sample/sample_data_random.sqcs")
@click.option("-o", "--output-directory", default="test/out/sample/")
@click.option("-v", "--verbose-level", default=2)
def main(input_filepath, output_directory, verbose_level):
    """
    Performs overlapping peptide sequence (OPS) analysis

    Parameters
    ----------
    input_filepath : str
    output_directory : string
    verbose_level : int

    Returns
    -------
    None
    
    """
    profile = cProfile.Profile()
    profile.enable()   # --- start profiling
    verbose_print("Start Homo-signal analysis", 0, verbose_level)
    start_time = time.time()

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, output_directory]
    input_filepath, output_directory = clean_input_paths(list_of_paths)

    # If parameters inputted by user valid
    if inputs_valid(input_filepath, output_directory):
        # Check output directory
        output_directory = create_out_path(output_directory, input_filepath)

        # Read dataset and add columns for results
        verbose_print("Read input", 0, verbose_level)
        data = read_in(input_filepath)

        # Analyse homo signals
        verbose_print("Analyse homo signals", 0, verbose_level)
        data = analyse_homo_signals(data,verbose_level)

        # Clean dataset for output
        data = clean_dataset(data)

        # Create Homo-signal statistic histograms
        verbose_print("Create homo-signal histograms", 0, verbose_level)
        create_homo_signal_histograms(data, input_filepath.split('/')[-1],
                                      output_directory)

        # Write Output
        verbose_print("Write output", 0, verbose_level)
        write_output(data, input_filepath.split('/')[-1], output_directory)
    runtime = round_self(time.time() - start_time, 2)
    verbose_print(f"\nEnd script (Elapsed time: {runtime}s)", 0, verbose_level)
    verbose_print("===================================", 0, verbose_level)
    profile.disable()  # --- stop profiling
    profile.create_stats()
    with open("profileM03.txt", 'w', encoding="utf-8") as fp:
        stats = pstats.Stats(profile, stream=fp)
        stats.sort_stats('cumtime')
        stats.print_stats()
    sys.exit(0)


def inputs_valid(input_filepath: str, output_directory: str):
    """
    check validity of inputted parameters

    Parameters
    ----------
    input_filepath : str,
    output_directory : str

    Returns
    -------
    inputs_valid : bool
    """

    # check whether an inputfile with the extension .sqcs is specified
    if input_filepath and input_filepath.endswith(".sqcs"):
        return True
    raise Exception(f"Error! The parameter \"input-filepath\" was not given or was not ending with the '.sqcs' "
                    f"extension (given: {input_filepath}).")
