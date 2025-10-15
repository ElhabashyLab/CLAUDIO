# Module 01 - Unique protein (pair) listing tool

### The CLI - Command Line Interface
```
> claudio_lists [-i <filepath>] [-it <directorypath>] [-p <"comma-separated str">] [-s <True/False>] [-x <comma-separated str>] [-t <"blastp">] [-o <directorypath>] [-bl <directorypath>] [-bldb <directorypath>] [-hh <directorypath>] [-hhdb <directorypath>] [-v <int>]

-i,    --input-filepath,        path to inputfile,
                                default="test/sample_data_random.csv"
-it,   --input-temppath,        path to directory for temporary files, default=None
-p,    --projections,           comma-separated position-sensitive list that names the column names of the users dataset
                                containing the necessary information for the tool. The column names should contain and 
                                should be given in the following order: crosslinked peptide_a, crosslinked peptide_b, 
                                crosslinked residue position_a, crosslinked residue position_b, position of crosslinked 
                                residue in peptide_a, position of crosslinked residue in peptide_b, UniProt ID of 
                                protein belonging to peptide_a, UniProt ID of protein belonging to peptide_b.
                                Note: The positions of the crosslinked residue in the peptides are information only 
                                accessed, if the given full sequence positions do not match into the retrieved UniProt 
                                sequence. If the positions are confirmed you may simply create two substitute columns 
                                for the positions in the peptides instead and leave them empty.
                                default="peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2"
-s,    --uniprot_search,        if the tool has been run before with the same input a temporary file was saved, which 
                                can be used to retrieve the previous results of the uniprot and structure searches. In 
                                this case you can set uniprot_search=False and it will try to retrieve said temporary 
                                save file, instead of rerunning the uniprot sequence search, default=True
-x,    --xl-residues,           comma-separated one-letter-code residues, optional: add two ':' after the 
                                one-letter-code symbol of the residue in order to specify full sequence position 
                                (either 1 for start, or -1 for end position) and/or the atom used for the distance
                                computation, default="K,M:N:1"
-t,    --search-tool,           always set to "blastp" (as of this version), specifying the tool which should be used for pdb 
                                search, default="blastp"
-o,    --output-directory,      output directory for produced csv-files, default="test/out/sample"
-bl,   --blast-bin,             binary directory in blast installation, or None if binary directory has been added to 
                                PATH variable (e.g. if blast can be called from anywhere), default=None
-bldb, --blast-db,              database directory for blast database installation (will automatically update, if left 
                                on default), default="claudio/data/pdbaa"
-hh,   --hhsearch-bin,          binary directory in hh-suite installation, or None if binary directory has been added to
                                PATH variable (e.g. if hhsearch can be called from anywhere), default=None
-hhdb, --hhsearch-db,           database directory for hh-suite installation, default="$HHDB"
-v,    --verbose-level,         verbose level value, default=2:
                                    0: no outputs at all will be written to the commandline
                                    1: write tool inits and passed time
                                    2: write progressbars (where implemented)
                                    3: write alignments during data processing, and write extra information on process results
                                    4: write alignments during uniprot to pdb position translation
                                    5: write verfications during uniprot to pdb position translation
```
### Input
This tool requires a CSV-file containing multiple observed cross-linking interactions. One column has to contain the 
uniprot id associated with the crosslinked protein, two columns have to contain the observed peptides for each 
interacting residue and two columns have to contain the crosslinked residue's position within the full sequence 
(alternative: fill these with Nans, but add two columns with the crosslinked residue position in the respective 
peptide). Please make sure that the peptide
sequences only contain valid capitalized one-character representations of amino acids.\ It is recommended to start the analysis of your cross-linking dataset here, if you do not run the full 
pipeline. Most important for this first step is the customization of the parameter "-p / --projections". This parameter 
requires a comma-separated position-sensitive list, which maps the column names of your dataset to the ones used in the tool. You may
see examples for this in [this module](https://github.com/KohlbacherLab/CLAUDIO/tree/main/module01/src/main.py)
or in the [example configuration-file](https://github.com/KohlbacherLab/CLAUDIO/tree/main/config/config_description.txt).

### Output
This tool will return two CSV-files and one LOG-file. One contains a list of all unique proteins, their full uniprot 
sequences, additional information retrieved from uniprot, their pdb id and the number of occurences in the inputfile. 
The second CSV-file will have the extension '.sqcs', which marks it as the input for module02 or module03. The LOG-file 
lists eventual issues or errors in cross-linked residue positions in the inputfile that had to be changed/fixed for the 
output.

### Example
This module can be run like with default parameters on the sample dataset:
```
claudio_lists
```
This will result in two CSV-files in "data/out/unique_protein_list" pertaining the project's sample dataset 
['sample_data_random.csv'](https://github.com/KohlbacherLab/CLAUDIO/tree/main/test/sample_data_random.csv).
```
python3 claudio_lists.py -i "c/user/documents/cross_links.csv -o "c/user/documents/outs"
```
This will result in two csv-files in "c/user/documents/outs" for the input dataset 'cross_links.csv'.

## Authors
* **Alexander Röhl**
* **Hadeer Elhabashy**
* **Eugen Netz**
