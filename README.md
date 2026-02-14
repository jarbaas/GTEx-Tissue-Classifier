# GTEx-Tissue-Classifier
A bioinformatics tool to predict tissue origin from unknown RNA-seq profiles using GTEx reference data. Built with Python.

## Biological Question
Sample identity is a cruical part of transcriptomics research. However, due to incorrect labeling of samples, loss of metadata, or cross-contaminiation, the tissue origins of particular samples may be missing. Furthermore, there are also forensic applications for the tracing of tissue origins in unknown samples. Provided the RNA sequencing of a given sample, can its tissue of origin be determined by comparing its gene expression signature to a human reference database?

This tool utilizes the Genotype-Tissue Expression (GTEx) Portal, a database of tissue and cell-specific gene expression with samples spanning 54 non-diseased tissue sites across ~1000 adults. By deriving a similarity score between the unknown sample's expression profile and GTEx reference tissues, this tool will offer a statistical likelihood of its tissue identity. 

## Project Description
GTEx-Tissue-Classifier is a command-line Python utlity that takes TPM-normalized, processed gene expression data and computes the similarity to a backend database of human tissue signatures. GTEx-Tissue-Classifier is novel in its approach to labeling samples by leveraging visuals and QC to enhance the interpretability of results. 

## Input and output specifications
### Input
The tool requires a TSV or CSV file containing processed RNA sequencing read quanitification that has been TPM normalized. The file requires a Gene column and TPM column, with the gene column accepting either symbols or Ensembl IDs. 

### Output
The tool will output a results folder with the following:
- A summary file providing the tissue prediction and associated confidence score
- A table comparing the similiarity score of the sample to each tissue option preseent in the GTEx database
- A bar chart featuring the scores of the top five matching tissues for presentation purposes

In instances where there are not enough genes present to make a prediction or there is a lack of housekeeping genes present, the tool will notify the user of QC failure so the sample can be re-evaluated.

## Data Sources
This tool uses data processed from the V11 Release of the [adult GTEx portal](https://gtexportal.org/home/aboutAdultGtex). 

## Limitations
- The GTEx database is built from healthy tissues. Inputting canceerous or diseased samples may result in lower correlation scores due to disease-specific gene dysregulation. 
- Single-cell RNA sequencing data may require pseudobulking before it will be accepted as input.
