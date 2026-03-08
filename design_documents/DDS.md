# Design Document Specification (DDS)
Goal (from SRS): The goal of GTEx-Tissue-Classifier is to identify tissue origins of unknown RNA-seqsamples. The method for identifying tissues involves performing RNA sequencing of the sample, building a normalized list of TPM counts for gene expression, and input of this list into the command-line software. By comparing gene expression to the GTEx database, the tool will provide the user an output file containing the similarity scores for each tissue, including a most likely tissue type and a graph showing the top five tissue possibilities. 

 ## Objectives
 **Accuracy:** Gene expression correlation should have >95% accuracy in correctly identifying a tissue type. 
 **Efficiency:** Tool should streamline original heavyweight GTEx inputs into lighter modules containing necessary readouts, reducing overhead for users.
 **Usability:** CLI should cleanly integrate into existing RNA sequencing pipelines, streamlining usage for end-user.
 **Interpretability:** Heatmaps and bar charts will be produced to help simplify key classification decisions. 

## Modules
### Module 1 - Architecture
* Goal: Manage user inputs, choose between simulation vs real data runs, manages data flow between downstream modules. 
* Functions:
	* ```parse_arguments()``` - uses argparse to understand flags on data such as '--input', '--output', '--mode', and '--reference'
	* ```main()``` - Decides between running the tool on simulated data or real data. Once implemented, can run tool from start to finish. 
	* ```load_input(filepath)``` - Reads users CSV file, validates existence of "Gene" and "TPM" columns, returns Pandas DF
	* ```validate_normalization(df)``` - Ensures input sample is TPM normalized and raises error if raw counts are detected 

### Module 2 - Math Logic
* Goal: Purely numerical, accepts vectors and returns statistical scores
* Functions:
	* ```filter_variable_genes(df, n=2000)``` - Filters the gene lists in the tissue dataframe to the top 2000 most variable, relying on unique genes to distinguish tissues
	* ```calculate_spearman(vector, tissue_matrix)``` - Calculates correlation between input vector and tissue columns in the tissue matrix
	* ```rank_matches(correlation_dict)``` - Sorts the correlation results in descending order to identify closest matches
	
### Module 3 - Simulation
* Goal: Generates the simulation data for unit tests and function testing. Can be used to validate math functions without needing full GTEx dataset. 
**UPDATE 2/25** - Simulation data is generated based on GTEx master reference file, mimicking real data format and distribution.
* Functions:
	* ```generate_mock_tissues(rows=100, cols=5)``` - Creates a reference matrix with representative gene TPM values in rows and example tissues in columns
	* ```generate_mock_sample(target_tissue, noise)``` - Creates an unknown sample matrix with representative genes in rows and TPM values in columns.     Gaussian noise can be specified in args to verify algorithmic handling. 

### Module 4 - Real data
* Goal: Handles extraction, transformation and loading of raw GTEx source files. Used to build database for the full tool. 
* Functions:
	* ```read_file_data(relative_filepath)``` - Reads the data from a text file and returns it as a list of lines
	* ```download_gtex_data(tissue_filepath, output_dir)``` - Downloads .gct files for all tissues from the GTEx portal. Designate tissue list location in simple filepath argument, eg. /configs/tissue_list.txt. 
	* ```parse_raw_gct(filepath)``` - Parses the .gct files downloaded from GTEx database
	* ```compute_TPM(tissue_matrix)``` - Calculates median TPM vector for tissues in tissue matrix
	* ```extract_gene_mapping(filepath)``` - Extracts dictionary to map Ensembl ID to gene symbol. Served to replaced Ensembl IDs with gene symbols in final outputs. 

### Module 5 - Visualization and Outputs
* Goal: Converts the mathematical outputs in math module into graphs and images
* Functions: 
	* ```plot_correlations(results_dict, output_path)``` - Uses matplotlib to generate a bar chart of the top five tissue matches
	* ```plot_marker_heatmap(user_vector, ref_vector)``` - Generates a heatmap comparing top markers of input samples to top markers defining the closest matching tissue
	* ```write_summary_report(results, filename)``` - Outputs the final tissue prediction, confidence score and/or any warnings into an html file


## Milestones

### Milestone 1 - Architecture

**Goal:** Establish the repository, design documents and package architecture

**Tasks:**
* Set up directory structure
* Implement `pyproject.toml`
* Write design documents including SRS, WBS, DDS

### Milestone 2 - Simulation

**Goal:** Verify functions in math module work on simulation data

**Tasks:**
* Implement math module
* Implement simulation module
* Create simulation data
* Run math functions on sim data, assess accurate tissue verification

### Milestone 3 - Prototype

**Goal:** Design a working CLI prototype that can accept a user input and produce a math result

**Tasks:**
* Implement Module 1
* Verify inputs are properly loaded
* Write unit tests for `load_input()` to test for bad file structures
* Connect module 1 to module 2

### Milestone 4 - Real Data Integration

**Goal:** Replace sample data with full GTEx data

**Tasks:**
* Implement module 4
* Download GTEx tissue files and run `build_db()`
* Test sample data on `build_db()` to verify correct output

### Milestone 5 - Outputs

**Goal:** Create outputs for user visualization

**Tasks:**
* Implement module 5
* Test output functions on sample data, polish images to ensure clean output for users
* Verify output functions on real data
* Run complete build
* Finalize `README.md` and `datasets.md`
* Submit final build

### Milestone 6 - Documentation

**Goal:** Update and verify docstrings, type hints, README and design_documents

**Tasks:**
* Update docstring descriptions to match code functions
* Add type hints to functions
* Update README to better describe edge cases
* Update design documents to incorporate team feedback, project updates and outlook. 

### Milestone 7- Presentation

**Goal:** Design vignette and demo for presentation to colleagues

**Tasks:**
* Build vignette
* Design presentation

AI use disclaimer: Google Gemini was used for advice on structuring functions inside modules. All writing in this document is my own. 
