import yaml

configfile: "configs/config.yaml"

with open(config["tissue_list"], 'r') as f:
    tissue_list = [line.strip() for line in f if line.strip()]

rule all:
    input: config["final_output"]

rule download_data:
    output:
        expand(f"{config['raw_dir']}/{{tissue}}.gct.gz", tissue=tissue_list)
    run:
        from gtex_tissue_classifier.real_data import download_gtex_data
        download_gtex_data(config["tissue_list"], config["raw_dir"])

rule process_tissue:
    input:
        f"{config['raw_dir']}/{{tissue}}.gct.gz"
    output:
        f"{config['processed_dir']}/{{tissue}}_median_tpm.csv"
    script:
        "scripts/process_tissue.py"

rule build_master_matrix:
    input:
        expand(f"{config['processed_dir']}/{{tissue}}_median_tpm.csv", tissue=tissue_list)
    output:
        config["final_output"]
    script:
        "scripts/merge_median_tpm.py"
