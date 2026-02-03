#Dataset Description

Final validation of the tool will be performed on tissue-level data from the GTEx project. Specifically, transcripts per million (TPM) data from each tissue type will be individually downloaded and labelled, then the samples within each tissue will be aggregated into a median TPM value, and finally the RNA seq inputs will be compared against the array of tissue-specific median TPMs to identify the most probable tissue of origin. 

* Source website: https://gtexportal.org/home/downloads/adult-gtex/bulk_tissue_expression
* Specific data: .gct.gz files for each tissue listed under "Gene TPMs by tissue"
* Source version: Dataset will be sourced from GTEx Analysis V11. From website, "GTEx V11 updates the GTEx V10 data to use GENCODE 47 annotation. It contains no new samples or donors compared to V10."
* Data format: .GCT. This is a tab-delimited format for gene expression data. 
* Data structure: A GCT file is a matrix containing sample metadata and gene metadata, as well as their respective IDs. Genes are placed into the rows, and samples are placed into the columns. The TPM values reside in a data matrix at the interesection of the two heading groups. 
* Data size: Files for each tissue type range between 1 Mb and 100 Mb. Total expected size of all files is expected to be near 2.5 Gb. Given the median of samples will be determined for each tissue type, it is expected that a condensed file for all tissue types can be generated to be uploaded with the package.  
* Data subset: In order to test GTex-Tissue-Classifier during development, a smaller, simulated dataset will be employed. Specifically, using numpy, an example .GCT file will be generated containing 100 gene rows and 5 different samples. Importantly, the gene expression concentration will vary between tissues, such that example tissue A will have a subset of genes that are higher concentration than tissue B, to mimic the gene expression of actual tissues. Furthermore, simulated gene expression data from input samples will also be generated for testing input/cleaning features. 
* Data statistics: Dataset calculations will be performed as follows:
	1. Verification that TPMs per column sum to 1 million, to ensure proper TPM calculations from source.
	1. Calculation of median TPMs for each tissue.
	2. Variance calculations across tissues to isolate the 2000 most variable genes in each tissue, whcih will be used for identification. This removes uneeded genes that may weigh down the application. 


AI use disclaimer: Google Gemini was consulted for advice on processing the GTEx data.