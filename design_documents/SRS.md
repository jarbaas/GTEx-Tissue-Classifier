# Software Requirements Specification (SRS) for GTEx-Tissue-Classifier

## Introduction
The goal of GTEx-Tissue-Classifier is to identify tissue origins of unknown RNA-seqsamples. The method for identifying tissues involves performing RNA sequencing of the sample, building a normalized list of TPM counts for gene expression, and input of this list into the command-line software. By comparing gene expression to the GTEx database, the tool will provide the user an output file containing the similarity scores for each tissue, including a most likely tissue type and a graph showing the top five tissue possibilities. 

## Use Cases
A common use case of GTEx-Tissue-Classifier is if contamination of a lab sample is suspected, sequencing can be performed on the sample and inputted into software to identify tissue candidates. Furthermore, if a labeling or metadata of a lab sample is lost, GTEx-Tissue-Classifier willl provide a probable estimate of the tissue origin. 

Further use cases of the tool are represented in forensic analysis, where a tissue of unknown origin may be present at a crime scene, allowing investigators to narrow down the source of the sample with a higher degree of confidence. 

## Goals

* Calculate similarity scores between gene expression input data and tissue markers
* Assemble similarity scores into both ranked and diagrammatic outputs to demonstrate tissue origin likelihood
* Provide QC estimates by flagging contaminated or incomplete samples
