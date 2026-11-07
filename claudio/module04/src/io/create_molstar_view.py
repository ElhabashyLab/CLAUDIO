"""Export existing structure and cross-link results for the Mol* viewer."""
import html
import math
import zipfile
from pathlib import Path
from string import Template

import pandas as pd
from Bio.PDB import MMCIFParser, PDBParser
from Bio.PDB.Polypeptide import three_to_one

from claudio.utils.utils import build_xl_dataset


def export_molstar_visualization(data, output_directory, atom_name="CB", xl_residues=None):
    """Write portable scenes and an HTML viewer without changing the results.

    Parameters
    ----------
    data : pd.DataFrame
        M4 records containing structure paths, chain IDs and pdb_pos_a/b.
        Optional pdb_hetflag_a/b and pdb_icode_a/b specify full residue IDs.
    output_directory : str | Path
        New or empty directory for the HTML page and MVSX packages.
    atom_name : str
        Atom to display when a record has no explicit pdb_atom_a/b value.
        This must agree with the atom used for the distance calculation.
    xl_residues : str | None
        Existing CLAUDIO cross-link configuration, such as "K:CA:,M:N:1".
        Selects the configured atom for each residue instead of atom_name.
        Explicit pdb_atom_a/b values take precedence when available.

    Returns
    -------
    output_directory : Path
    """
    from molviewspec import create_builder

    required = {"path", "chain_a", "chain_b", "pdb_pos_a", "pdb_pos_b"}
    missing = sorted(required.difference(data.columns))
    if missing:
        raise ValueError(f"Missing visualization columns: {', '.join(missing)}")
    atom_name = _text(atom_name)
    if not atom_name:
        raise ValueError("An atom name is required for visualization")
    df_xl_res = build_xl_dataset(xl_residues) if xl_residues is not None else None

    output_directory = Path(output_directory).expanduser().resolve()
    if output_directory.exists() and any(output_directory.iterdir()):
        raise ValueError("Use a new or empty visualization directory")

    groups = {}
    table_rows = []
    for index, row in data.iterrows():
        source_id = _text(row.get("source_record_id")) or _text(
            row.get("xlms_source_record_id")
        ) or str(index)
        record = {"row": row, "source_id": source_id,
                  "status": "not drawn: no structure", "model": ""}
        table_rows.append(record)
        path = _text(row["path"])
        if path and path != "-":
            groups.setdefault(Path(path).expanduser().resolve(), []).append(record)

    output_directory.mkdir(parents=True, exist_ok=True)
    options = []
    for number, (path, records) in enumerate(groups.items(), start=1):
        label = _text(records[0]["row"].get("pdb_id")) or path.stem
        for record in records:
            record["model"] = label
        try:
            suffix = path.suffix.lower()
            if suffix not in {".pdb", ".cif", ".mmcif"}:
                raise ValueError("supported structure formats are PDB and mmCIF")
            parser = PDBParser(QUIET=True) if suffix == ".pdb" else MMCIFParser(QUIET=True)
            models = list(parser.get_structure("model", str(path)).get_models())
            if len(models) != 1:
                raise ValueError("a single coordinate model is required")
            model = models[0]
        except (OSError, ValueError, KeyError) as error:
            for record in records:
                record["status"] = f"not drawn: {error}"
            continue

        builder = create_builder()
        bundled_name = "structure.pdb" if suffix == ".pdb" else "structure.cif"
        structure = builder.download(url=bundled_name).parse(
            format="pdb" if suffix == ".pdb" else "mmcif"
        ).model_structure(model_index=0)
        palette = ["#7c9ec9", "#d8b365", "#83b89e", "#b898bc"]
        for chain_number, chain in enumerate(model):
            structure.component(selector={"auth_asym_id": chain.id}).representation(
                type="cartoon"
            ).color(color=palette[chain_number % len(palette)])

        for record in records:
            row = record["row"]
            try:
                endpoints = [_endpoint(model, row, site, atom_name, df_xl_res) for site in "ab"]
            except (ValueError, KeyError) as error:
                record["status"] = f"not drawn: {error}"
                continue
            a, b = endpoints
            record["status"] = "drawn"
            notes = [f"Source: {record['source_id']}", f"{a[2]} -- {b[2]}"]
            for column in ("original_XL_type", "XL_type", "eucl_dist", "topo_dist", "evidence"):
                notes.append(f"{column}: {_text(row.get(column)) or 'not provided'}")
            tooltip = "<br>".join(html.escape(note) for note in notes)
            color = {"intra": "#2878b5", "inter": "#d64c4c"}.get(
                _text(row.get("XL_type")), "#666666"
            )
            structure.component(selector=[a[1], b[1]]).representation(
                type="ball_and_stick"
            ).color(color=color)
            structure.component(selector=[a[1], b[1]]).tooltip(text=tooltip)
            structure.primitives(tooltip=tooltip).distance(
                start=a[0], end=b[0], color=color, radius=0.08,
                dash_length=0.25, label_template="{{distance}}",
                label_size=3.0, label_color="#333333",
            )

        state = builder.get_state(title=f"CLAUDIO: {label}")
        if hasattr(state, "model_dump_json"):
            scene = state.model_dump_json(exclude_none=True, indent=2)
        else:
            scene = state.json(exclude_none=True, indent=2)
        package_name = f"model_{number:04d}.mvsx"
        with zipfile.ZipFile(output_directory / package_name, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("index.mvsj", scene)
            archive.write(path, bundled_name)
        options.append(f'<option value="{package_name}">{html.escape(label)} ({number})</option>')

    rows_html = []
    for record in table_rows:
        row = record["row"]
        values = [record["source_id"], record["model"],
                  _text(row.get("original_XL_type")), _text(row.get("XL_type")),
                  _text(row.get("eucl_dist")), _text(row.get("topo_dist")),
                  _text(row.get("evidence")), record["status"]]
        rows_html.append("<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in values) + "</tr>")
    template = Template(Path(__file__).with_name("molstar_view.html").read_text(encoding="utf-8"))
    page = template.substitute(model_options="\n".join(options), link_rows="\n".join(rows_html))
    (output_directory / "index.html").write_text(page, encoding="utf-8")

    print(f"Structure visualization saved: {output_directory}")
    if options:
        print("Open Mol* online viewer: https://molstar.org/viewer/")
        print("Choose Home > Open Files and select a model_*.mvsx file from the folder above "
              "(Format: Auto or MVSX), or drag the file into the viewer.")
        print("For HPC runs, download the .mvsx file(s) to your computer first.")
    else:
        print("No usable structure was available for 3D visualization.")
    print("Double-click index.html for the result table and viewing instructions.")
    return output_directory


def _text(value):
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _endpoint(model, row, site, atom_name, df_xl_res=None):
    """Resolve a structure residue and atom; never substitute a nearby site."""
    status = _text(row.get(f"mapping_status_{site}"))
    if status and status != "mapped":
        raise ValueError(f"endpoint {site} mapping status is {status}")
    chain_id = _text(row[f"chain_{site}"])
    if chain_id not in model:
        raise ValueError(f"chain {chain_id!r} not found")
    value = row[f"pdb_pos_{site}"]
    if isinstance(value, bool):
        raise ValueError(f"endpoint {site} has an invalid structure position")
    try:
        position = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"endpoint {site} has no integer structure position") from None
    if not math.isfinite(position) or not position.is_integer():
        raise ValueError(f"endpoint {site} has no integer structure position")

    hetflag = row.get(f"pdb_hetflag_{site}")
    icode = row.get(f"pdb_icode_{site}")
    has_hetflag = hetflag is not None and not pd.isna(hetflag)
    has_icode = icode is not None and not pd.isna(icode)
    residues = [residue for residue in model[chain_id]
                if residue.id[1] == int(position)
                and (residue.id[0] == (_text(hetflag) or " ") if has_hetflag else residue.id[0] == " ")
                and (not has_icode or residue.id[2] == (_text(icode) or " "))]
    if len(residues) != 1:
        raise ValueError(f"endpoint {site} structure residue is missing or ambiguous")
    residue = residues[0]
    selected_atom = _text(row.get(f"pdb_atom_{site}"))
    if not selected_atom and df_xl_res is not None:
        try:
            residue_name = three_to_one(residue.resname)
        except KeyError:
            raise ValueError(f"endpoint {site} residue has no configured atom") from None
        atoms = df_xl_res.loc[df_xl_res.res == residue_name, "atom"].unique()
        if len(atoms) != 1:
            raise ValueError(f"endpoint {site} configured atom is missing or ambiguous")
        selected_atom = atoms[0]
    selected_atom = selected_atom or atom_name
    if selected_atom not in residue:
        raise ValueError(f"endpoint {site} atom {selected_atom} not found")
    coordinates = [float(value) for value in residue[selected_atom].coord]
    if not all(math.isfinite(value) for value in coordinates):
        raise ValueError(f"endpoint {site} atom coordinates are not finite")
    selector = {"auth_asym_id": chain_id, "auth_seq_id": int(position),
                "pdbx_PDB_ins_code": residue.id[2].strip(),
                "auth_comp_id": residue.resname, "auth_atom_id": selected_atom}
    label = f"{chain_id}:{int(position)}{residue.id[2].strip()} {selected_atom}"
    return coordinates, selector, label
