# Module 02 - Structural distance analysis tool

### The CLI - Command Line Interface
```
> claudio_structdi [-i <filepath>] [-it <directorypath>] [-rt <True/False>] [-t <"blastp">] [-x <comma-separated str>] [-pc <float>] [-lmin <float>] [-lmax <float>] [-e <float>] [-qi <float>] [-c <float>] [-r <float>] [-o <directorypath>] [-bl <directorypath>] [-bldb <directorypath>] [-hh <directorypath>] [-hhdb <directorypath>] [-tl <directorypath>] [-v <int>]

-i,    --input-filepath,        path to inputfile,
                                default="test/out/sample/sample_data_random.sqcs"
-it,   --input-temppath,        path to directory for temporary files, default=None
-rt,   --read-temps,            if the tool has been run before with the same input a temporary file was saved, which 
                                can be used to retrieve the previous results of the uniprot and structure searches,
                                default=False
-t,    --search-tool,           always set to "blastp" (as of this version), specifying the tool which should be used for pdb 
                                search, default="blastp"
-x,    --xl-residues,           comma-separated one-letter-code residues, optional: add two ':' after the 
                                one-letter-code symbol of the residue in order to specify full sequence position 
                                (either 1 for start, or -1 for end position) and/or the atom used for the distance
                                computation (allowed: "N", "CA", "C", "O", "CB"), default="K,M:N:1"
-pc,   --plddt-cutoff,          float value used as cutoff for alphafold structure prediction confidences (plddt), 
                                default=70.0
-lmin, --linker-minimum,        float value used as minimal crosslinker range in angstrom, default=5.0
-lmax, --linker-maximum,        float value used as maximal crosslinker range in angstrom, default=35.0
-e,    --e-value,               e-value used in structure search, default=1e-5
-qi,   --query-id,              query identity used in structure search, default=90.0
-c,    --coverage,              coverage used in structure search, default=50.0
-r,    --res-cutoff,            float value used as cutoff in angstrom for resolution of structure files, default=4
-o,    --output-directory,      output directory, default="test/out/sample"
-bl,   --blast-bin,             binary directory in blast installation, or None if binary directory has been added to 
                                PATH variable (e.g. if blast can be called from anywhere), default=None
-bldb, --blast-db,              database directory for blast database installation (will automatically update, if left 
                                on default), default="claudio/data/pdbaa"
-hh,   --hhsearch-bin,          binary directory in hh-suite installation, or None if binary directory has been added to
                                PATH variable (e.g. if hhsearch can be called from anywhere), default=None
-hhdb, --hhsearch-db,           database directory for hh-suite installation, default="$HHDB"
-tl,   --topolink-bin,          binary directory in topolink installation, or None if binary directory has been added to
                                PATH variable (e.g. if topolink can be called from anywhere), default=None
-v,    --verbose-level,         verbose level value, default=2:
                                    0: no outputs at all will be written to the commandline
                                    1: write tool inits and passed time
                                    2: write progressbars (where implemented)
                                    3: write alignments during data processing, and write extra information on process results
                                    4: write alignments during uniprot to pdb position translation
                                    5: write verfications during uniprot to pdb position translation
```

### Input
This tool requires a CSV-file containing multiple observed cross-linking interactions. Two columns have to contain 
UniProt IDs for each interacting residue, two columns the observed peptides for each interacting residue,
two columns the crosslinked residue's position within the full sequence (alternative: fill these with
Nans, but add two columns with the residue's positions in the respective peptides), two columns with the UniProt sequences,
and one column with the initial cross-link type estimation.\
It is recommended to start the analysis of your dataset with [module01](https://github.com/KohlbacherLab/CLAUDIO/tree/main/module01),
which will generate said CSV-file with the extension '.sqcs'. If you wish to skip this step though, or if you customized
the output file used as input here, check this list to ensure that you can run this module:
* file has to have the extension '.sqcs'
* file is formatted like a normal CSV-file
* file has columns "unip_id", "pep_a", "pep_b", "seq", "pos_a", "pos_b", "res_pos_a", "res_pos_b", 
each filled with information (in that order) of UniProt IDs [strings], peptides [strings], UniProt sequences [strings], 
crosslinked residue positions in full UniProt sequences [integers], and (alternative to normal positions) positions of 
the crosslinked residue in the peptides [integers].

### Output
This tool will return a directory full of pdb structure files, which were necessary for the computation, a CSV-file 
ending with the extension '.sqcs_structdi.csv', which is the result of the structure search including the 
structural distance computation's results, two histogram PNG-files depicting the computed structural distances and their
differences, and two more which depict the experimental methods and their resolution for each pdb structure.

### Example
This module can be run like with default parameters on the sample dataset:
```
claudio_structdi
```
This will result in a directory called 'structures' in "test/out/sample" filled with pdb structures, two 
histograms describing their resolutions and experimental methods, and one CSV-file with the associated results of the
structural distance analysis, all pertaining the project's default dataset 
['sample_data_random.csv'](https://github.com/KohlbacherLab/CLAUDIO/tree/main/test/sample_data_random.csv).
```
claudio_structdi -i c/user/documents/cross_links.csv -rt True -o "c/user/documents/outs"
```
This will result in the respective outputs into the directory "c/user/documents/outs" for the input dataset 
'cross_links.csv' using the temporary save files from the last execution (if this has not been run previously with the 
same input, this will return an error).

## Authors
* **Alexander Röhl**
* **Hadeer Elhabashy**
* **Eugen Netz**
