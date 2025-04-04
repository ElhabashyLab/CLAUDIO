# Module 04 - XL-type evaluation

### The CLI - Command Line Interface
```
> claudio_xl [-i <filepath>] [-i2 <filepath>] [-p <float>] [-lmin <float>] [-lmax <float>] [-es <float>] [-dm <float] [-c <float>] [-o <directorypath>] [-s <True/False>] [-v <int>]

-i,   --input-filepath,         path to outputfile of structural distance analysis,
                                default="test/out/sample/sample_data_random.sqcs_structdi.csv"
-i2,  --input-filepath2,        path to outputfile of ops analysis,
                                default="test/out/sample/sample_data_random.sqcs_ops.csv"
-p,   --plddt-cutoff,           float value used as cutoff for alphafold structure prediction confidences (plddt), 
                                default=70.0  
-lmin,  --linker-minimum,         float value used as minimal crosslinker range in angstrom, default=0.0
-lmax,  --linker-maximum,         float value used as maximal crosslinker range in angstrom, default=35.0
-es,  --euclidean-strictness,   float value substracted from the linker ranges for the euclidean distance scoring
                                (minimum will not go below 0), default=5.0
-dm,  --distance-maximum,       maximal distance value that seems realistic, if surpassed the distance will be set to 
                                this value during the confidence scoring, to ensure its consistency, default=50.0
-c,   --cutoff,                 float value used as confidence score cutoff, if surpassed, the linker type will be set 
                                to inter, default=0.0  
-o,   --output-directory,       output directory for produced csv-files, default="test/out/sample/"
-s,   --compute-scoring,        boolean, for whether experimental scoring and resulting XL-type evluations should be 
                                computed and appended to result dataset, default=False
-v,   --verbose-level,          verbose level value, default=2:
                                    0: no outputs at all will be written to the commandline
                                    1: write tool inits and passed time
                                    2: write progressbars (where implemented)
                                    3: write alignments during data processing, and write extra information on process results
                                    4: write alignments during uniprot to pdb position translation
                                    5: write verfications during uniprot to pdb position translation
```

### Input
This tool requires the outputs of the [Structural distance](https://github.com/KohlbacherLab/CLAUDIO/tree/main/module02)
and [OPS-analysis](https://github.com/KohlbacherLab/CLAUDIO/tree/main/module03) tools as input.

### Output
This tool will return one CSV-file with all results of the previous analysis as well as the computed confidence scores 
and new cross-link types (intra or inter), one histogram showing the confidence score distribution, and a directory
called 'homomers' containing subdirectories for each unique protein, which in turn each contain a csv-file with all 
restraints and one or multiple fasta files for each possible related oligomeric state found by SWISS-MODEL. Additionally
it will add pymol scripts to the folder containing the pdb structures.

### Example
This module can be run like with default parameters on the sample dataset:
```
claudio_xl
```
This will result in a CSV-file in "test/out/sample" containing the full dataset with the results of the structural 
distance analysis tool, OPS analysis tool, and final cross-link type evaluation, as well as one histogram depicting the 
confidence score distribution, all pertaining the project's default dataset 
['sample_data_random.csv'](https://github.com/KohlbacherLab/CLAUDIO/tree/main/test/sample_data_random.csv).
```
claudio_xl -i c/user/documents/cross_links.csv -o c/user/documents/outs
```
This will result in the respective outputs into the directory "c/user/documents/outs" for the input dataset 
'cross_links.csv' with a fresh uniprot search for the full protein sequences.

## Authors
* **Alexander Röhl**
* **Hadeer Elhabashy**
* **Eugen Netz**
