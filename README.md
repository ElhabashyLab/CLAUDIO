# CLAUDIO 

*CLAUDIO*, the tool for "**C**ross-**l**inking **a**nalysis **u**sing **di**stances and **o**verlaps", allows
for an in-depth evaluation of structure and sequence information, automating necessary post-experiment analysis. 
It downloads protein structures for this, and returns protein-link-specific small-datasets containing structural 
restraints in CSV-format, and the input dataset extended by its results.
These include...
* ... PDB IDs of protein structures searched by BLASTP
* ... Mapping of UniProt protein to structure sequence positions
* ... Structural distances calculated with TopoLink
* ... Information on Homo-signal responses (e.g. overlapping peptide sequences in same-protein cross-links)
* ... Information on possible oligomeric states discovered by SWISS-MODEL homology
* ... Cross-link type estimations

## Setup
For a quick setup, run the following command with the ``pip``-installation associated with your version of python 3, 
while your current working directory is the directory containing this README file (alternatively: replace '``.``' in the
command with the path to said directory):
```
pip install .
```

### External Tools
In order to run *CLAUDIO* you need to install the following external tools:
* **Topolink**[[1]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references) (for structural analysis)
* **BLASTP**[[2]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references) (for finding suitable protein structures)

#### Installation Instructions
* **Blast** with *pdbaa* database (see [Windows or Unix Manuals](https://www.ncbi.nlm.nih.gov/books/NBK52638/), or see this [MacOS Manual](https://www.blaststation.com/intl/members/en/howtoblastmac.html))
  * For Blast, you also have to download the newest *pdbaa* database. You may do so by navigating into your 
  Blast installation directory and running the following command:
    ```
    perl bin/update_blastdb.pl --passive --decompress pdbaa
    ```
    This download method requires `perl` to be executable from your commandline, which is not installed by 
  default on Windows and MacOS systems. You may install it with this 
  [Windows-Manual](https://learn.perl.org/installing/windows.html) or 
  [MacOS-Manual](https://learn.perl.org/installing/osx.html), or manually download the database 
  [here](https://ftp.ncbi.nlm.nih.gov/blast/db/).
  * Hint: If you followed the Installation Manual (linked up top) to-the-letter, you may have added the environmental 
    variable `$BLASTDB` to your paths. If so, you can use this variable instead of the full path in the input parameters
    of CLAUDIO.
* **TopoLink** (see [Installation Manual](https://m3g.github.io/topolink/download.html))
  * Topolink possesses a standalone executable for Windows 10 systems (or higher), which can be downloaded directly
  [here](https://m3g.github.io/topolink/Windows_Binaries/Windows10-64bits/topolink.exe).

To ease the execution of *CLAUDIO* you may want to ensure that these tools can be executed directly from your terminal 
(e.g. add their respective `bin` directories to the `Path` variable of your OS). Otherwise, you may specify the
location of the `bin` directories in the input parameters.

### Online connection
*CLAUDIO* calls upon the API of a number of bioinformatic online databases ([UniProt](https://www.uniprot.org/)
[[3]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references), [RCSB](https://www.rcsb.org/)
[[4]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references), [AlphaFold](https://alphafold.ebi.ac.uk/)
[[5]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references), and [SWISS-MODEL](https://swissmodel.expasy.org/)
[[6]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references)) during its computations. This means it cannot be 
run offline.\
It is furthermore recommended having a stable internet connection, as otherwise certain API calls may not be answered or
lead to empty results. This of course, also necessitates the database server's side to be running properly as well. If 
errors or suspicious inconsistencies in the results persist due to this, you may want to try again later.

### Offline Databases
In addition to the aforementioned online databases, *CLAUDIO* accesses the SIFTS database
[[7,8]](https://github.com/KohlbacherLab/CLAUDIO/tree/main#references). The file in question can be found 
[here](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/data/pdb_chain_uniprot.csv).\
We also recommend updating this file from time to time ([download here](http://ftp.ebi.ac.uk/pub/databases/msd/sifts/flatfiles/csv/pdb_chain_uniprot.csv.gz)) 
in order to keep up its efficiency, though this is not a necessity (last updated: 16.01.2025).

### Optional: Packages (background info)
This tool is written in and has to be run with python 3 (last tested v3.11).\
It has the following requirements:

* biopython 1.79
* click 8.1.3
* matplotlib 3.6.3
* pandas 1.5.3
* requests 2.28.2
* numpy==1.23.5

The packages may be installed all at once with the file [requirements.txt](https://github.com/KohlbacherLab/CLAUDIO/tree/main/requirements.txt):
```
pip install -r requirements.txt
```
or individually:
```
pip install biopython==1.79
pip install click==8.1.3
pip install matplotlib==3.6.3
pip install pandas==1.5.3
pip install requests==2.28.2
pip install numpy==1.23.5
```
Note: Both approaches need to refer to the pip-installer associated to the python installation, that will be used to run
the tool.

## Usage
*CLAUDIO* consists of a total of 4 modules. Each module can be run independently as long as appropriate inputs are 
delivered. For details on how to run the modules individually see their respective README-files.
* [Module 01 - Unique protein (pair) listing tool](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module01/README.md)
* [Module 02 - Structural distance analysis tool](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module02/README.md)
* [Module 03 - Overlapping peptide sequence analysis tool](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module03/README.md)
* [Module 04 - XL-type evaluation](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module04/README.md)

For details on how to run the **full** pipeline continue below.

---

---

## CLAUDIO - Full pipeline
### The CLI - Command Line Interface
```
> claudio [-i <filepath>] [-it <diretorypath>] [-o <directorypath/"">] [-p <"comma-separated str">] [-bl <directorypath/None>] [-bldb <directorypath>] [-tl <directorypath>] [-x <comma-separated str>] [-lmin <float>] [-lmax <float>] [-t <"blastp">] [-e <float] [-qi <float>] [-cv <float>] [-r <float>] [-rt <True/False>] [-pc <float>] [-s <True/False>] [-v <int>] [-es <float>] [-dm <float>] [-ct <float>] [-c <filepath>] 

-i,    --input-filepath,        path to inputfile, default="test/sample_data_random.csv"
-it,   --input-temppath,        path to directory for temporary files, default=None
-o,    --output-directory,      output directory for produced csv-files, default="test/out/sample"
-p,    --projections,           comma-separated position-sensitive list that names the column names of the users dataset
                                containing the necessary information for the tool. The column names should contain and 
                                should be given in the following order: crosslinked peptide_a, crosslinked peptide_b, 
                                crosslinked residue position_a, crosslinked residue position_b, position of cross-linked
                                residue in peptide_a, position of cross-linked residue in peptide_b, UniProt ID of 
                                protein belonging to peptide_a, UniProt ID of protein belonging to peptide_b.
                                Note: The positions of the crosslinked residue in the peptides are information only 
                                accessed, if the given full sequence positions do not match into the retrieved UniProt 
                                sequence. If the positions are confirmed you may simply create two substitute columns 
                                for the positions in the peptides instead and leave them empty.
                                default="peptide1,peptide2,position1,position2,k_pos1,k_pos2,entry1,entry2"
-bl,   --blast-bin,             binary directory in blast installation, or None if binary directory has been added to 
                                PATH variable (e.g. if blast can be called from anywhere), default=None
-bldb, --blast-db,              database directory for blast installation, default="$BLASTDB"
-tl,   --topolink-bin,          binary directory in topolink installation, or None if binary directory has been added to
                                PATH variable (e.g. if topolink can be called from anywhere), default=None
-x,    --xl-residues,           comma-separated one-letter-code residues, optional: add two ':' after the 
                                one-letter-code symbol of the residue in order to specify full sequence position 
                                (either 1 for start, or -1 for end position) and/or the atom used for the distance
                                computation (allowed: "N", "CA", "C", "O", "CB"), default="K,M:N:1"
-lmin, --linker-minimum,        float value used as minimal crosslinker range in angstrom, default=5.0
-lmax, --linker-maximum,        float value used as maximal crosslinker range in angstrom, default=35.0
-t,    --search-tool,           always set to "blastp" (as of this version), specifying the tool which should be used for pdb 
                                search, default="blastp"
-e,    --e-value,               e-value used in structure search, default=1e-5
-qi,   --query-id,              query identity used in structure search, default=90.0
-cv,   --coverage,              coverage used in structure search, default=50.0
-r,    --res-cutoff,            float value used as cutoff in angstrom for resolution of structure files, default=4.0
-rt,   --read-temps,            if the tool has been run before with the same input a temporary file was saved, which
                                can be used to skip some of the steps, default=False
-pc,   --plddt-cutoff,          float value used as cutoff for alphafold structure prediction confidences (plddt), 
                                default=70.0
-s,    --compute-scoring,       boolean, for whether experimental scoring and resulting XL-type evluations should be 
                                computed and appended to result dataset, default=False
-v,    --verbose-level,         verbose level value, default=3:
                                    0: no outputs at all will be written to the commandline
                                    1: write tool inits and passed time
                                    2: write progressbars (where implemented)
                                    3: write alignments during data processing, and write extra information on process results
                                    4: write alignments during uniprot to pdb position translation
                                    5: write verfications during uniprot to pdb position translation
-es,   --euclidean-strictness,  float value substracted from the linker ranges for the euclidean distance scoring
                                (minimum will not go below 0), default=5.0
-dm,   --distance-maximum,      maximal distance value that seems realistic, if surpassed the distance will be set to 
                                this value during the confidence scoring, to ensure its consistency, default=50.0
-ct,   --cutoff,                float value used as confidence score cutoff, if surpassed, the linker type will be set 
                                to inter, default=0.0
                                
-c,    --config,                filepath to configuration file containing all input parameters, default=''
```
### Input
This tool requires a CSV-file containing multiple observed cross-linking interactions. Two columns have to contain 
uniprot ids for each interacting residue, two columns have the observed peptides for each interacting residue
and two columns the crosslinked residue's position within the full sequence (alternative: fill these 
with Nans, but add two columns with the residue's positions in the respective peptides).
1. The input file should then be specified as such with the "-i / --input-filepath"-parameter.
2. If you intend to run CLAUDIO on separate datasets simultaneously, or want to split your dataset into smaller ones,
you have to specify the parameter "-it / --input-temppath". CLAUDIO generates multiple temporary files during its
computation, most of which are in- or outputs of the third-party tools used. If parallel executions of CLAUDIO are run
with the same tempfile path, conflicts may be caused disrupting or falsifying some results. Thereby make sure to specify
different paths here, if you run the tool in parallel.
3. It is important to customize the parameter "-p / --projections". This parameter requires a comma separated list
as input, which maps the column names of your dataset to the ones used in the tool.
4. You need to specify the paths to the local external tool installations (BLASTP and TopoLink).
The parameters for this are "-bl / --blast-bin" for the binary directory of blast, "-bldb / --blast-db" for the database
directory containing the *pdbaa* database files, and "-tl / --topolink-bin" for the binary directory of TopoLink.
5. Make sure you customize the settings pertaining the cross-linking experiments specifications, e.g. 
"-x / --xl-residues" for the aminoacids which may be cross-linked, and both "-lmin / --linker-minimum" and 
"-lmax / --linker-maximum" for the cross-linker's range capability. Besides this specify the amino acids the used cross-
linker is able to bind to. For this specify a tiny comma-separated list of possibly crosslinked residues, as 
one-letter-code symbols. Optionally you may add two colon-symbols, if they wish to specify the position of the 
residue in the sequence and/or the atom in the residue used for the distance computation. After the first colon-symbol 
they may place the atom type for the distance computation, e.g. 'CB', 'CA', or 'N', etc. . If no value is set here 'CB'
will be used by default. After the second colon-symbol they may place one of three position values: 0 if the residue
may occur anywhere in the protein, 1 if the residue has to be at the N-terminus, or -1 if the residue has to be at the
C-terminus (ex.: use "K:CB:0" to calculate the cross-link distance between lysin C-beta-atoms at any position in the
chain). If you want to specify multiple possible positions for the same symbol you have to add them
individually (ex.: "M::1,M::-1" for methionine at either the beginning or end of the chain). By default, 0 is set here,
e.g. the residue may be placed anywhere.\
Note: If the position or the atom type is specified there have to be two colon-symbols (ex.: "K,M:1" will not be
accepted as input). You can leave the respective specification empty though, if you wish to use the default here (ex.:
"K::1" is equal to "K:CB:1", "M:N:0" is equal to "M:N:", "K:CB:0" is equal to "K::" and also to just "K").

With this the relevant settings are defined. You may choose to further specify the structure searche's settings in terms
of coverage, sequence identity, and e-value, as well as the resolution cutoff during the structure selection, or even 
the advanced settings.

You may see examples for all parameters in the [example configuration-file](https://github.com/KohlbacherLab/CLAUDIO/tree/main/config/config.txt),
which also serves as an alternative to supply all parameter inputs.


### Output
This tool returns all the outputs listed in the modules (see 
[module01](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module01),
[module02](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module02),
[module03](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module03),
[module04](https://github.com/KohlbacherLab/CLAUDIO/tree/main/claudio/module04)).

Note: All CSV-file outputs pertaining the input dataset are summarized into a single one (marked with 
'_final.csv'-extension), e.g. the output CSV-file of module01 ending with '.sqcs', of module02 ending with 
'.sqcs_structdi.csv', and of module03 ending with '.sqcs_ops.csv' will be summarized here. 

### Example
**CLAUDIO** (in full) can be run like this:
* with a configuration file with all parameters (this will run the test dataset, when using the default config.txt, with all non-described parameters being filled with default values)
```
claudio -c config/config.txt
```
* with a configuration file and a few overwriting CLI parameters (this will run the larger benchmark dataset)
```
claudio -c config/config.txt -i benchmark_data.csv -o test/out/benchmark
```
* with mostly default parameters and a few set as CLI parameters
```
claudio -i /home/user/me/docs/xl_dataset.csv -o /home/user/me/docs/claudio_outputs
```
\
Also, you may return all CLI parameter options on the terminal like this:
```
claudio --help
```

## Authors
* **Alexander Röhl**
* **Tobias Löser**
* **Hadeer Elhabashy**
* **Eugen Netz**

## Citation
If you use CLAUDIO, please cite:
Röhl, Alexander, Eugen Netz, Oliver Kohlbacher, and Hadeer Elhabashy. "CLAUDIO: automated structural analysis of cross-linking data." Bioinformatics 40, no. 4 (2024): btae146.

## References
* [1] Ferrari, Allan JR, et al. "TopoLink: evaluation of structural models using chemical crosslinking distance constraints." Bioinformatics 35.17 (2019): 3169-3170.
* [2] Altschul, Stephen F., et al. "Basic local alignment search tool." Journal of molecular biology 215.3 (1990): 403-410.
* [3] UniProt Consortium. "UniProt: a worldwide hub of protein knowledge." Nucleic acids research 47.D1 (2019): D506-D515.
* [4] Kouranov, Andrei, et al. "The RCSB PDB information portal for structural genomics." Nucleic acids research 34.suppl_1 (2006): D302-D305.
* [5] David, Alessia, et al. "The AlphaFold database of protein structures: a biologist’s guide." Journal of molecular biology 434.2 (2022): 167336.
* [6] Schwede, Torsten, et al. "SWISS-MODEL: an automated protein homology-modeling server." Nucleic acids research 31.13 (2003): 3381-3385.
* [7] Dana, Jose M., et al. "SIFTS: updated Structure Integration with Function, Taxonomy and Sequences resource allows 40-fold increase in coverage of structure-based annotations for proteins." Nucleic acids research 47.D1 (2019): D482-D489.
* [8] Velankar, Sameer, et al. "SIFTS: structure integration with function, taxonomy and sequences resource." Nucleic acids research 41.D1 (2012): D483-D489.
