# Work Breakdown Structure (WBS)
## Project: Incoporate feedback from HW 2

### Action: Validate and test edge cases

**Sub action: Validate sample matching accuracy**
- Tasks:
  * [] Download 10-20 RNA sequencing samples from GEO databases
  * [] Run tool on samples, evaluate if tool correctly predicts tissue origin
- Deliverable:
  * Accuracy score = (correct predictions / trials) * 100
- Completion:
  * Accuracy score >= 95%

**Sub action: Address edge cases**
- Tasks:
  * [] Update README to clarify how to handle samples that do not conform to package constraints. 
  * [] Migrate exceptions and error raising to helper functions inside of `validation.py`
- Deliverables:
  * `validation.py` with helper functions
- Completion:
  * README addresses edge cases
  * Error handling moved to functions in separate document, integrated into existing functions

**Sub action: Update docstrings**
- Tasks:
  * [] Add type hints to functions to specify input format of arguments
  * [] Edit docstrings to correctly describe functions and I/O parameters.
- Deliverable:
  * Type hints included in function. 
- Completion:
  * Each function has correct docstrings and type hints. 

## Project: Create package demo and vignette

- Tasks:
  * [] Create project demo
  * [] Create project vignette
- Deliverables:
  * Project vignette in `\tests`
  * Project demo in PowerPoint?
- Completion
 * Project is ready for presentation 
 
## Project:  Build package prototype 

### Action: Create script to test input and output of data

**Sub action: Create simulated data**

- Tasks:
  * [X] Test `generate_mock_tissues` and `generate_mock_sample` in `simulation.py`
- Deliverable:
  * Mock .CSV file representing sample data and .GCT file representing input files. 
- Completion:
  * Correctly formatted files present in `data\simulated_data`

UPDATE 2/25:
- Task:
  * [] Update simulation to produce sample data based on GTEx master document instead of random numbers
- Deliverable:
  * Simulated sample and tissue files in `data\simulated_data`
- Completion:
  * Files correctly match data distribution of GTEx reference file. 


**Sub action: Test loading and preparation of GTEx data**

- Tasks:
  * [X] Write unit tests for `parse_raw_gct` and `compute_TPM` functions
  * [X] Run unit tests to examine unwanted behavior. 
- Deliverable:
  * Unit tests in `tests\test_real_data.py`
- Completion:
  * Unit tests run without raising errors on functions

**Sub action: Write temporary script to test input and output of prototype**

- Tasks:
  * [X] Create Jupyter Notebook that generates sample RNA Seq and GTEx data, then parses and ranks correlation of TPM values.
- Deliverable: 
  * `tutorial.ipynb` in `\tests`
- Completion:
  * Jupyter Notebook successfully outputs a ranked list of correlated genes between simulated RNA Seq sample and GTEx sample. 

## Project: Compute the median TPM values of the GTEx tissues

**Tasks:**

- [X] Write `download_gtex_data`, `parse_raw_gct`, `compute_TPM` functions
- [X] Design snakemake file to parallelize dowloading and compiling master GTEx tissue file


## Project: Develop Architecture - Module 1

### Action: Design argument parsing

**Sub action: Create interface flags**

- Tasks:  
  * [X] Create specific flags for `argparse`
- Deliverable:  
  * `parse_arguments()` function (Module 1)
- Completion:  
  * `python main.py --help` should print help menu with flags and descriptions

**Sub action: Create logic for switching between modes**

- Task:  
  * [X] Create logic to tell architecture whether to run in simulation or real mode
- Deliverable:  
  * Logic fork in `main()` that correctly brings up the correct module based on input
- Completion criteria:  
  * Tool will print "Simulation" or "Real", indicating user choice.


### Action: Input validation

**Sub action: Design input function**

- Tasks:  
  * [X] Write `load_input(filepath)` which accepts CSV inputs and loads into a pandas DataFrame  
  * [X] Unit test `load_input()`
- Deliverable:  
  * Written function
- Completion criteria:  
  * Function should load CSV and display an error code if path or file type is invalid

**Sub action: Validate structure of input files**

- Tasks:  
  * [] `validate_normalization()` function to check if TPMs have been properly normalized  
  * Each column in RNA-seq input CSV should sum to 1,000,000
- Deliverable:  
  * Code should raise error if raw counts are inputted
- Completion criteria:  
  * Unit testing an improperly formatted file triggers an error
  UPDATE 2/25 - This task is being moved to Input Validation task for project partner as part of HW 3


## Project: Implement Math Module

### Action: Code correlations

- Task:  
  * [X] Write `calculate_spearman()` function
- Deliverable:  
  * Function returning `dict = {Tissue: Score}`
- Completion criteria:  
  * Same vectors should return a score of `1.0`

### Action: Design ranking algorithm

- Task:  
  * [X] Write `rank_matches()` function
- Deliverable:  
  * List of tuples `[(Tissue, Score)]`
- Completion criteria:  
  * Sample tissue types should generate top match for chosen sample


## Project: Implement Simulation Module

### Action: Create generators to build simulation data

**Sub action: Create a tissue matrix generator**

- Task:  
  * [X] Write `generate_mock_tissues()` to build 100x5 gene/tissue matrix
- Deliverable:  
  * CSV generator function
- Completion criteria:  
  * CSV should show high expression gene regions corresponding to a unique tissue

**Sub action: Create generator to build sample input data**

- Task:  
  * [X] Write `generate_mock_sample()` function  
  * ~~Incorporate Gaussian noise argument into function~~
- Deliverable:  
  * CSV generator function
- Completion criteria:  
  * ~~Samples generated by this function should be unique based on Gaussian noise~~

  UPDATE 2/25: Mock samples will now be based on GTEx reference document, should follow similar data distribution


---

AI use disclaimer: Google Gemini was used to help map a project outline overview, all writing is my own. 
