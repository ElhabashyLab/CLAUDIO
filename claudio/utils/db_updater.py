import click
import os
import datetime
import requests as r
from typing import Optional
from requests import HTTPError
import gzip
import tarfile
from io import BytesIO

_SIFTS_LAST_UPDATED = '2025-06-06'
_PDBAA_LAST_UPDATED = '2025-06-06'


@click.command()
@click.option("-s", "--sifts-threshold", help="number of days as threshold, "
                                              "that if surpassed updates the sifts database", default=14)
@click.option("-p", "--pdbaa-threshold", help="number of days as threshold, "
                                              "that if surpassed updates the pdbaa database", default=30)
@click.option("-d", "--pdbaa-dir", help="database directory for blast installation", default=None)
def main(sifts_threshold: float, pdbaa_threshold: float, pdbaa_dir: Optional[str]):
    this_file_path = os.path.abspath(__file__)
    project_path = '/'.join(this_file_path.replace('\\\\', '/').replace('\\', '/').split('/')[:-2])

    # lookup claudio data directory
    if project_path.endswith('/claudio'):
        # Update dbs
        sifts_updated, sifts_path = sifts_db_updater(project_path, sifts_threshold)
        if sifts_updated: print(f"SIFTS DB was updated in {sifts_path}.")
        pdbaa_updated, pdbaa_path = pdbaa_updater(pdbaa_dir, pdbaa_threshold)
        if pdbaa_updated: print(f"PDBAA DB was updated in {pdbaa_path}.")

        # Update this files' last updated datetimes
        update_last_updated(this_file_path, sifts_updated, pdbaa_updated)
    else:
        raise RuntimeError("Script was unable to find project directory, because it seems to have been moved.")


def sifts_db_updater(project_path: str, threshold: float) -> tuple[bool, str]:
    """
    Download or update the SIFTS database file pdb_chain_uniprot.csv

    Parameters
    ----------
    project_path : str
    threshold : float

    Returns
    -------
    was_updated: bool
    output_path : str
    """
    last_updated = datetime.date.fromisoformat(_SIFTS_LAST_UPDATED)
    if (datetime.date.today() - last_updated).days > threshold:
        try:
            # download database
            url = 'https://ftp.ebi.ac.uk/pub/databases/msd/sifts/flatfiles/csv/pdb_chain_uniprot.csv.gz'
            response = r.get(url)
            # check download request status
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise HTTPError(f"Unable to retrieve db file from https://ebi.ac.uk.\n"
                                f"Status ({response.status_code}): {e}")

            # wrap content in BytesIO
            payload = BytesIO(response.content)
            with gzip.open(payload, 'rb') as b:
                filename = url.split('/')[-1].replace('.gz', '')
                output_path = project_path + f'/data/{filename}'
                # write to csv in data directory
                with open(output_path, 'w') as f:
                    f.write(b.read().decode('utf-8'))
                    return True, output_path
        except Exception:
            pass
    return False, ''


def pdbaa_updater(pdbaa_dir: Optional[str], threshold: float) -> tuple[bool, str]:
    """
    Update pdbaa database file for blast in specified directory

    Parameters
    ----------
    pdbaa_dir : str / None
    threshold : float

    Returns
    -------
    was_updated: bool
    output_path : str
    """
    if pdbaa_dir:
        last_updated = datetime.date.fromisoformat(_PDBAA_LAST_UPDATED)
        if (datetime.date.today() - last_updated).days > threshold:
            try:
                # download database
                url = 'https://ftp.ncbi.nlm.nih.gov/blast/db/pdbaa.tar.gz'
                response = r.get(url)
                # check download request status
                try:
                    response.raise_for_status()
                except HTTPError as e:
                    raise HTTPError(f"Unable to retrieve db file from https://ftp.ncbi.nlm.nih.gov.\n"
                                    f"Status ({response.status_code}): {e}")
                with tarfile.open(fileobj=BytesIO(response.content), mode='r:gz') as f:
                    try:
                        f.extractall(pdbaa_dir)
                    # If extractall fails because of individual file read/write permissions, try individual extraction
                    except IOError:
                        for file in f:
                            try:
                                f.extract(member=file, path=pdbaa_dir)
                            # If individual extraction for a file fails, remove existing file first before trying
                            # extraction again
                            except IOError:
                                member_path = pdbaa_dir + ('/' if not pdbaa_dir.endswith('/') else '') + f.name
                                os.remove(member_path)
                                f.extract(member=file, path=pdbaa_dir)
                    return True, pdbaa_dir
            except Exception:
                pass
    return False, ''


def update_last_updated(filepath: str, sifts_updated: bool, pdbaa_updated: bool) -> None:
    """
    Update last updated datetimes for sifts and pdbaa in this file

    Parameters
    ----------
    filepath : str
    sifts_updated : bool
    pdbaa_updated : bool

    Returns
    -------
    None
    """
    if sifts_updated or pdbaa_updated:
        with open(filepath, 'r') as f:
            lines = f.read().split('\n')
            tdy = datetime.date.today()
            for i, l in enumerate(lines):
                if sifts_updated and l.startswith('_SIFTS_LAST_UPDATED = '):
                    lines[i] = f"_SIFTS_LAST_UPDATED = '{tdy}'"
                elif pdbaa_updated and l.startswith('_PDBAA_LAST_UPDATED = '):
                    lines[i] = f"_PDBAA_LAST_UPDATED = '{tdy}'"
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))

def get_last_updated() -> None:
    """
    Print the last updated dates for SIFTS and PDBAA databases.

    Returns
    -------
    None
    """
    print(f"SIFTS Last Updated: {_SIFTS_LAST_UPDATED}")
    print(f"PDBAA Last Updated: {_PDBAA_LAST_UPDATED}")

if __name__ == "__main__":
    main()
