import click
import sys
import time
import ast
import cProfile,pstats

from claudio.module04.src.io.read_ins import read_inputs
from claudio.module04.src.algorithm.combine_reevals import combine_inter_reevaluations
from claudio.module04.src.algorithm.retrieve_oligo_state import retrieve_oligomeric_states
from claudio.module04.src.algorithm.create_plots import create_plots
from claudio.module04.src.io.create_pymol_scripts import setup_pml_scripts
from claudio.module04.src.io.write_outs import write_outputs

from claudio.utils.utils import verbose_print, clean_input_paths, evaluate_boolean_input, \
    create_out_path, clean_dataset, round_self, minimize_dataset


@click.command()
@click.option("-i", "--input-filepath", default="test/out/sample/sample_data_random.sqcs_structdi.csv")
@click.option("-i2", "--input-filepath2", default="test/out/sample/sample_data_random.sqcs_ops.csv")
@click.option("-p", "--plddt-cutoff", default=70.0)
@click.option("-lmin", "--linker-minimum", default=5.0)
@click.option("-lmax", "--linker-maximum", default=35.0)
@click.option("-es", "--euclidean-strictness", default=None)
@click.option("-dm", "--distance-maximum", default=50.0)
@click.option("-c", "--cutoff", default=0.0)
@click.option("-o", "--output-directory", default="test/out/sample/")
@click.option("-s", "--compute-scoring", default=False)
@click.option("-v", "--verbose-level", default=2)
def main(input_filepath, input_filepath2, plddt_cutoff, linker_minimum, linker_maximum, euclidean_strictness,
         distance_maximum, cutoff, output_directory, compute_scoring, verbose_level):
    profile = cProfile.Profile()
    profile.enable()   # --- start profiling
    verbose_print("Start New Inter Interaction Analysis", 0, verbose_level)
    start_time = time.time()

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, input_filepath2, output_directory]
    input_filepath, input_filepath2, output_directory = clean_input_paths(list_of_paths)

    # Evaluate value of boolean inputs
    compute_scoring = evaluate_boolean_input(compute_scoring)

    # Check output directory
    output_directory = create_out_path(output_directory, input_filepath)

    # If parameters inputted by user valid
    if inputs_valid(input_filepath, input_filepath2, plddt_cutoff, linker_minimum, linker_maximum, euclidean_strictness,
                    distance_maximum, cutoff, output_directory, compute_scoring, verbose_level):
        plddt_cutoff = float(plddt_cutoff)
        linker_minimum = float(linker_minimum)
        linker_maximum = float(linker_maximum)
        euclidean_strictness = float(euclidean_strictness) if euclidean_strictness not in ["None", None] else None
        distance_maximum = float(distance_maximum)
        cutoff = float(cutoff)
        filename = input_filepath.split('/')[-1].split('.')[0]

        # Read inputs
        verbose_print("Read inputs", 0, verbose_level)
        data = read_inputs(input_filepath, input_filepath2)

        # Combine results of both reevaluations
        verbose_print("Combine results of both reevaluations", 0, verbose_level)
        data = combine_inter_reevaluations(data, plddt_cutoff, linker_minimum, linker_maximum,
                                           euclidean_strictness, distance_maximum, cutoff, compute_scoring)

        # Retrieve known oligomeric states from SWISS-MODEL
        verbose_print("Retrieve known oligomeric states from SWISS-MODEL", 0, verbose_level)
        data = retrieve_oligomeric_states(data, verbose_level)

        # Clean dataset for output
        data = clean_dataset(data)
        data[["unip_id_a", "unip_id_b", "pos_a", "pos_b", "pep_a", "pep_b", "res_pos_a", "res_pos_b", "pdb_id",
              "pdb_method", "pdb_resolution", "chain_a", "chain_b", "pdb_pos_a", "pdb_pos_b", "pLDDT_a", "pLDDT_b",
              "topo_dist", "eucl_dist", "homo_pep_overl", "evidence", "XL_type", "XL_confirmed",
              "swiss_model_homology"]].to_csv(f"{output_directory}{filename}_extended.csv")

        # Write pymol scripts
        verbose_print("Write pymol scripts", 0, verbose_level)
        setup_pml_scripts(data)

        # Minimze dataset
        data = minimize_dataset(data)

        # Create inter score histogram
        verbose_print("Create score histogram", 0, verbose_level)
        create_plots(data, filename, cutoff, compute_scoring, output_directory, linker_minimum, linker_maximum)

        # Write final csv containing all computed information, fastas for alphafold and protein-specific csv with
        # interaction restraints
        verbose_print("Write full outputs", 0, verbose_level)
        write_outputs(data, filename, compute_scoring, output_directory)

    verbose_print(f"\nEnd script (Elapsed time: {round_self(time.time() - start_time, 2)}s)", 0, verbose_level)
    verbose_print("===================================", 0, verbose_level)
    profile.disable()  # --- stop profiling
    profile.create_stats()
    with open("profileM04.txt", 'w') as fp:
        stats = pstats.Stats(profile, stream=fp)
        stats.sort_stats('cumtime')
        stats.print_stats()
    sys.exit()


def inputs_valid(input_filepath: str, input_filepath2: str, plddt_cutoff: float, linker_minimum: float, linker_maximum: float,
                euclidean_strictness: float, distance_maximum: float, cutoff: float, output_directory: str, compute_scoring: bool,
                verbose_level: int):
    """
    check validity of inputted parameters

    Parameters 
    ----------
    input_filepath : str,
    input_filepath2 : str,
    plddt_cutoff : float,
    linker_minimum : float,
    linker_maximum : float,
    euclidean_strictness : float,
    distance_maximum : float,
    cutoff : float,
    output_directory : str,
    compute_scoring : bool,
    verbose_level : int

    Returns
    -------
    inputs_valid : bool

    Raises 
    ------
        invalid input exceptions
    """

    # check whether outputfile from distance-based reevauation is specified
    if input_filepath.endswith(".sqcs_structdi.csv"):
        # check whether outputfile from homo-signal-based reevauation is specified
        if input_filepath2.endswith(".sqcs_ops.csv"):
            # check whether plddt cutoff has valid value
            try:
                plddt_cutoff = float(plddt_cutoff)
                if 0 <= plddt_cutoff <= 100:
                    # check whether minimum crosslinker distance has valid value
                    try:
                        linker_minimum = float(linker_minimum)
                        # check whether maximum crosslinker distance has valid value
                        try:
                            linker_maximum = float(linker_maximum)
                            # check whether euclidean strictness has valid value (either float or None)
                            try:
                                if euclidean_strictness is not None:
                                    euclidean_strictness = float(euclidean_strictness)
                            except ValueError:
                                try:
                                    if euclidean_strictness is not None:
                                        euclidean_strictness = ast.literal_eval(euclidean_strictness)
                                except ValueError:
                                    raise Exception(f"Error! Could not change type of given euclidean strictness to "
                                                    f"either float or None (given: {euclidean_strictness}).")
                            # check whether maximum distance has valid value
                            try:
                                distance_maximum = float(distance_maximum)
                                # check whether reevaluation cutoff has valid value
                                try:
                                    cutoff = float(cutoff)
                                    if 0 <= cutoff <= 1:
                                        return True
                                    else:
                                        raise Exception(f"Cutoff value for reclassification should be in [0, 1] "
                                                        f"(given: {cutoff}).")
                                except:
                                    raise Exception(f"Value given for reclassification cutoff should be possible to "
                                                    f"turn into a float (given: {cutoff}).")
                            except:
                                raise Exception(f"Value given for maximum distance value should be possible to turn "
                                                f"into a float (given: {distance_maximum}).")
                        except:
                            raise Exception(f"Value given for crosslinker maximum should be possible to turn into a "
                                            f"float (given: {linker_maximum}).")
                    except:
                        raise Exception(f"Value given for crosslinker minimum should be possible to turn into a float "
                                        f"(given: {linker_minimum}).")
                else:
                    raise Exception(f"pLDDT cutoff value should be in [0, 100] (given: {plddt_cutoff}).")
            except:
                raise Exception(f"Value given for pLDDT cutoff should be possible to turn into a float "
                                f"(given: {plddt_cutoff}).")
        else:
            raise Exception(f"Homo-signal reevaluation outputfile was either not correctly given or has wrong "
                            f"extension (given: {input_filepath2}).")
    else:
        raise Exception(f"Distance reevaluation outputfile was either not correctly given or has wrong extension "
                        f"(given: {input_filepath}).")
