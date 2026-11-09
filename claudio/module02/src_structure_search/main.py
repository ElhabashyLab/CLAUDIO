"""Main script for the structure search submodule of Module02's structural analysis.
Performs structure search using BLAST or HHsearch and retrieves PDB files."""
import os
import sys
import time
import click
import pandas as pd
from claudio.module02.src_structure_search.io.read_input import read_in
from claudio.utils.af_complex import restore_preprocessing_tracking
from claudio.module02.src_structure_search.algorithm.structure_search import structure_search
from claudio.module02.src_structure_search.io.read_temp import read_temp_file
from claudio.module02.src_structure_search.algorithm.pdb_download import download_pdbs
from claudio.module02.src_structure_search.algorithm.chain_copies import create_ident_chain_copies
from claudio.module02.src_structure_search.io.write_out import write_output
from claudio.module02.src_structure_search.algorithm.af_complex_search import (
    retrieve_af_complex,
    retrieve_discovered_complexes,
)

from claudio.utils.utils import (verbose_print, clean_input_paths,
                                create_out_path, round_self)

_STRUCTURE_INPUT_ROW = "_claudio_structure_input_row"


def _af_complex_fallback_input(_input_data, _legacy_data):
    """Select original input rows without an accepted experimental PDB."""
    if _legacy_data.empty:
        return _input_data.copy()

    _pdb_ids = _legacy_data["pdb_id"].fillna("").astype(str)
    _methods = _legacy_data["pdb_method"].fillna("").astype(str)
    _paths_exist = _legacy_data["path"].map(
        lambda _path: isinstance(_path, str) and os.path.isfile(_path)
    )
    _has_pdb = (
        _pdb_ids.str.fullmatch(r"[A-Za-z0-9]{4}", na=False)
        & ~_methods.str.contains("ALPHAFOLD", case=False, na=False)
        & _paths_exist
    )
    _covered_rows = set(
        _legacy_data.loc[_has_pdb, _STRUCTURE_INPUT_ROW]
    )
    _positions = [
        _position for _position in range(len(_input_data))
        if _position not in _covered_rows
    ]
    return _input_data.iloc[_positions].copy()


def _search_legacy_candidates(
    _data, _tmp_filepath, _structures_dir,
    _do_structure_search, _search_tool,
    _e_value, _query_id, _coverage, _res_cutoff,
    _blast_bin, _blast_db, _hhsearch_bin, _hhsearch_db,
    _verbose_level,
):
    """Retrieve candidates through the existing structure-search pipeline."""
    if not _do_structure_search and os.path.exists(_tmp_filepath):
        verbose_print(
            "Read from temporary save file", 0, _verbose_level
        )
        _data = read_temp_file(_data, _tmp_filepath)
    else:
        verbose_print(
            f"Perform {_search_tool} search", 0, _verbose_level
        )
        _data = structure_search(
            _data, _search_tool, _e_value, _query_id,
            _coverage, _tmp_filepath, _blast_bin,
            _blast_db, _hhsearch_bin, _hhsearch_db,
            _verbose_level,
        )

    verbose_print(
        "Download structures from RCSB database, "
        "or AlphaFold database if not found there",
        0, _verbose_level,
    )
    os.makedirs(_structures_dir, exist_ok=True)
    _data = download_pdbs(
        _data, _search_tool, _res_cutoff,
        _structures_dir, _verbose_level,
    )
    _data = create_ident_chain_copies(_data)
    _data["structure_backend"] = "legacy"

    return _data
def _combine_structure_candidates(_frames):
    """Preserve all candidates and assign unique row indices."""
    _combined = pd.concat(_frames, sort=False)

    # Reserve existing names so generated indices cannot overwrite them.
    _reserved = {str(_index) for _index in _combined.index}
    _used = set()
    _indices = []

    for _index in _combined.index:
        _new_index = _index
        _suffix = 1

        while str(_new_index) in _used:
            _new_index = f"{_index}_{_suffix}"
            _suffix += 1

            while str(_new_index) in _reserved:
                _new_index = f"{_index}_{_suffix}"
                _suffix += 1

        _used.add(str(_new_index))
        _indices.append(_new_index)

    _combined.index = pd.Index(
        _indices, name=_combined.index.name
    )
    return _combined
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
@click.option("-bldb", "--blast-db", default="claudio/data/pdbaa")
@click.option("-hh", "--hhsearch-bin", default=None)
@click.option("-hhdb", "--hhsearch-db", default="$HHDB")
@click.option(
    "--af-complex-model",
    default=None,
    help="Retrieve a specified existing AFDB protein-complex model.",
)
@click.option(
    "--af-complex-auto/--no-af-complex-auto",
    default=None,
    help=(
        "Discover existing AFDB complexes automatically. "
        "Enabled by default unless a model is specified."
    ),
)
@click.option("-v", "--verbose-level", default=2)
def main(input_filepath, input_temppath, do_structure_search, search_tool,
         e_value, query_id, coverage, res_cutoff, output_directory, blast_bin,
         blast_db, hhsearch_bin, hhsearch_db, verbose_level, af_complex_model=None, af_complex_auto=None):
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
    if af_complex_auto and af_complex_model is not None:
        raise click.UsageError(
            "--af-complex-auto and --af-complex-model are mutually exclusive."
        )
    if af_complex_auto is None:
        af_complex_auto = af_complex_model is None
    verbose_print("[3.1] Start Structure Search", 0, verbose_level, start='')
    start_time = time.time()

    # Get absolute paths and translate eventual windows paths
    list_of_paths = [input_filepath, input_temppath, output_directory,
                     blast_bin, blast_db, hhsearch_bin, hhsearch_db]
    input_filepath, input_temppath, output_directory, blast_bin, blast_db, \
    hhsearch_bin, hhsearch_db = clean_input_paths(list_of_paths)
    _legacy_input = None
    if af_complex_auto or af_complex_model is not None:
        if not input_filepath or not input_filepath.endswith(".sqcs"):
            raise click.BadParameter(
                "Input must be a .sqcs file.",
                param_hint="--input-filepath",
            )

        output_directory = create_out_path(
            output_directory, input_filepath
        )
        data, filename = read_in(input_filepath)
        data = restore_preprocessing_tracking(data, input_filepath)
        _legacy_input = data.copy()

        # A manually selected model continues to bypass automatic search.
        if af_complex_model is not None:
            structures_dir = os.path.join(output_directory, "structures")
            data = retrieve_af_complex(
                data, af_complex_model, structures_dir,
            )
            data["structure_backend"] = "af_complex"
            matched = data["af_match_status"].eq("matched")
            data.loc[matched, "pdb_id"] = data.loc[matched, "af_model_id"]
            data.loc[matched, "pdb_method"] = "ALPHAFOLD"
            data.loc[matched, "pdb_resolution"] = "ALPHAFOLD"
            write_output(data, filename, output_directory)

            runtime = round_self(time.time() - start_time, 2)
            verbose_print(
                f"Finished AF complex retrieval (Elapsed time: {runtime}s)",
                0, verbose_level,
            )
            return

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

        # Use the same input records for both search backends.
        verbose_print("Read input", 0, verbose_level)
        if _legacy_input is None:
            data, filename = read_in(input_filepath)
        else:
            data = _legacy_input.copy()

        _tmp_filepath = (
            f"{temp_dir}"
            f"{'.'.join(filename.split('.')[:-1])}"
            f"_{search_tool}_bltmp.{filename.split('.')[-1]}"
        )
        if af_complex_auto:
            if _STRUCTURE_INPUT_ROW in data.columns:
                raise ValueError(
                    f"Reserved internal column: {_STRUCTURE_INPUT_ROW}"
                )
            _legacy_input = data.copy()
            data[_STRUCTURE_INPUT_ROW] = range(len(data))

        data = _search_legacy_candidates(
            _data=data,
            _tmp_filepath=_tmp_filepath,
            _structures_dir=f"{output_directory}structures/",
            _do_structure_search=do_structure_search,
            _search_tool=search_tool,
            _e_value=e_value,
            _query_id=query_id,
            _coverage=coverage,
            _res_cutoff=res_cutoff,
            _blast_bin=blast_bin,
            _blast_db=blast_db,
            _hhsearch_bin=hhsearch_bin,
            _hhsearch_db=hhsearch_db,
            _verbose_level=verbose_level,
        )

        if af_complex_auto:
            _fallback_input = _af_complex_fallback_input(
                _legacy_input, data,
            )
            data = data.drop(
                columns=[_STRUCTURE_INPUT_ROW], errors="ignore",
            )

            if not _fallback_input.empty:
                verbose_print(
                    f"Search AF complexes for {len(_fallback_input)} "
                    "input candidates without an available PDB",
                    0, verbose_level,
                )
                _af_candidates = retrieve_discovered_complexes(
                    _fallback_input,
                    os.path.join(output_directory, "structures"),
                )
                _af_candidates["structure_backend"] = "af_complex"
                _matched = _af_candidates["af_match_status"].eq("matched")
                _af_candidates.loc[_matched, "pdb_id"] = (
                    _af_candidates.loc[_matched, "af_model_id"]
                )
                _af_candidates.loc[_matched, "pdb_method"] = "ALPHAFOLD"
                _af_candidates.loc[_matched, "pdb_resolution"] = "ALPHAFOLD"
                data = _combine_structure_candidates(
                    [data, _af_candidates]
                )

        # Write all structure candidates together.
        write_output(data, filename, output_directory)
    runtime = round_self(time.time() - start_time, 2)
    verbose_print(f"Finished successfully (Elapsed time: {runtime}s)", 0, verbose_level, start='')
    verbose_print("===================================", 0, verbose_level, start='')

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
                if (search_tool == "blastp") or os.path.exists(str(hhsearch_db)
                                                               + "pdb70_a3m.ffdata"):
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
                                            except Exception as exc:
                                                raise TypeError(f"Error! Given value for resolution cutoff could not "
                                                                f"be turned into a float variable (given: "
                                                                f"{res_cutoff}).") from exc
                                        else:
                                            raise ValueError(f"Error! Given coverage is not within allowed interval of "
                                                            f"[0,100] (given: {coverage}).")
                                    except Exception as exc:
                                        raise TypeError(f"Error! Given value for coverage could not be turned into a "
                                                        f"float variable (given: {coverage}") from exc
                                else:
                                    raise ValueError(f"Error! Given query identity is not within allowed interval of "
                                                    f"[0,100] (given: {query_id}).")
                            except Exception as exc:
                                raise TypeError(f"Error! Given value for query identity could not be turned into a "
                                                f"float variable (given: {query_id}") from exc
                        else:
                            raise ValueError(f"Error! Given e-value is not within allowed interval"
                                            f" of (0,1) (given: {e_value}).")
                    except Exception as exc:
                        raise TypeError(f"Error! Given value for e-value could not be turned into "
                                        f"a float variable (given: {e_value}") from exc
                else:
                    raise FileNotFoundError(f"Error! Could not find 'pdb70_a3m.ffdata' in given "
                                            f"hhsearch database directory (given: {hhsearch_db}).")
            else:
                raise FileNotFoundError(f"Error! Could not find 'pdbaa.phr'-File in given blast"
                                        f" database directory (given: {blast_db}).")
        else:
            raise ValueError(f"Error! Invalid search tool selected (given: {search_tool}).")
    else:
        raise RuntimeError(f"Error! The parameter \"input-filepath\" was not given or was not "
                           f"ending with the '.sqcs' extension (given: {input_filepath}).")
