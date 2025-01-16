import socket
import requests as r
import time
import ast
import pandas as pd

from claudio.utils.utils import verbose_print, round_self


def retrieve_oligomeric_states(data: pd.DataFrame, verbose_level: int):
    """
    retrieve oligomeric states known for each uniprot entry and add them to the dataset as a string
    
    Parameters
    ----------
    data : pd.DataFrame,
    verbose_level : int

    Returns
    ------- 
    data : pd.DataFrame
    """

    # container for already searched oligo-states
    start = time.time()
    known_ostates = query_oligo_states_from_swiss(data)
    print(f"Time taken to query oligomeric states from SWISS-MODEL: {time.time() - start}s")
    iteration_counter = [0, len(data.index)]
    data["swiss_model_homology"] = data.apply(
        lambda x: get_oligo_state_from_swiss(
            x, known_ostates, iteration_counter, verbose_level
        ), axis=1
    )
    verbose_print("", 1, verbose_level)

    return data


def query_oligo_states_from_swiss(data: pd.DataFrame):
    """
    query oligomeric states from SWISS-MODEL for all uniprot ids in the dataset
    
    Parameters
    ----------
    data : pd.DataFrame,
    verbose_level : int
    
    Returns
    -------
    known_ostates : dict[str, list[str]]

    """

    NUMBER_OF_CALL_REPEATS = 5
    DOWNLOAD_RATE_LIMITER_IN_SECONDS = 0.05

    known_ostates = {}
    base_url = "https://swissmodel.expasy.org/repository/uniprot/"

    # get all unique uniprot ids from the dataset
    unip_ids = pd.unique(data[['unip_id_a', 'unip_id_b']].values.ravel()).tolist()

    # if uniprot id not in already searched entries, do search in SWISS-MODEL
    for unip_id in unip_ids:
        # set up json url with uniprot id
        url = f"{base_url}{unip_id}.json"
        # repeat SWISS-MODEL calls for consistency (SWISS-MODEL has shown to inconsistently return empty or only
        # partial API call results)
        ostates = []
        num_fails = 0
        for _ in range(NUMBER_OF_CALL_REPEATS):
            try:
                try:
                    list_of_states = {structure["template"].split('.')[0]: structure["oligo-state"]
                                        for structure in
                                        ast.literal_eval(
                                            r.get(url).text.replace("null", "None")
                                        )["result"]["structures"]}
                    # add time skip to limit the rate of calls per second
                    # (see: https://swissmodel.expasy.org/docs/help#modelling_api)
                    time.sleep(DOWNLOAD_RATE_LIMITER_IN_SECONDS)
                except KeyError:
                    print(f"Warning! Received 'Exceeding rate limit'-error from SWISS API. "
                            f"Download speed will be reduced for Uniprot entry: {unip_id}.")
                    DOWNLOAD_RATE_LIMITER_IN_SECONDS += .1
                except ValueError:
                    if num_fails == NUMBER_OF_CALL_REPEATS:
                        raise ValueError(f"Error! Result json by Swiss-model could not be properly parsed as "
                                            f"dictionary for Uniprot entry: {unip_id}.\nReceived: {r.get(url).text}")
            except r.exceptions.Timeout:
                pass
            except (ConnectionError, socket.gaierror, r.exceptions.ConnectionError, ValueError) as e:
                if num_fails == NUMBER_OF_CALL_REPEATS:
                    print(f"No connection to SWISS-MODEL API possible for Uniprot entry: {unip_id}. "
                            f"Please try again later.")
                    print(e)
                    pass
                else:
                    num_fails += 1
            ostates.append(list_of_states)

        # Add resulting oligomeric states to list of known, if results not empty
        if ostates:
            # Ensure that missing data on repeats do not cause disturbances, by filling empty slots with "monomer"
            unique_keys = set(key for ostate in ostates for key in ostate.keys())
            for ostate in ostates:
                for key in unique_keys:
                    ostate.setdefault(key, ["monomer"])

            # Collect unique ostates of repeats
            ostates = {key: pd.unique([repeat[key] for repeat in ostates]).tolist() for key in unique_keys}

            # add result to known oligomeric states
            known_ostates[unip_id] = ostates
    return known_ostates



def get_oligo_state_from_swiss(data, known_ostates: dict[str, list[str]], i_iteration: list[int], verbose_level: int):
    """
    access SWISS-MODEL for given datapoint's uniprot ids, if not previously encountered, else retrieve known result
    from known_unips
    
    Parameters
    ----------
    data : pd.DataFrame,
    known_ostates : dict[str, list[str]],
    i_iteration : list[int],
    verbose_level : int

    Returns
    -------
    oligo_states : str
    """

    # progressbar
    ind, full_i = i_iteration
    ind += 1
    verbose_print(f"\r\t[{round_self((ind * 100) / full_i, 2)}%]", 1, verbose_level, end='')
    i_iteration[0] = ind

    # return homo-oligomer states if intra crosslink
    if data['unip_id_a'] == data['unip_id_b']:
        unique_ostates = sorted(pd.unique([state for states in known_ostates[data['unip_id_a']].values()
                                           for state in states]).tolist())
        unique_ostates = [state.replace('-', '') for state in unique_ostates if state not in ["heteromer", "monomer"]]
        return '_'.join(unique_ostates)
    # else, compute intersecting set of structures and return their oligomeric states
    else:
        intersect_oligo_states = {key: value for key, value in known_ostates[data['unip_id_a']].items()
                                  if key in known_ostates[data['unip_id_b']]}
        unique_intersect_ostates = sorted(pd.unique([state for states in intersect_oligo_states.values()
                                                     for state in states]).tolist())
        unique_intersect_ostates = [state.replace('-', '') for state in unique_intersect_ostates
                                    if (state != "monomer") and not state.startswith("homo")]
        return '_'.join(unique_intersect_ostates)
