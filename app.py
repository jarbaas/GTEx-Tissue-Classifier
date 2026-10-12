import os
import tempfile

import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="GTEx Tissue Classifier", layout="centered")
st.title("GTEx Tissue Classifier")
st.write(
    "Upload a TPM-normalized RNA-seq sample as CSV or TSV with **Gene** and **TPM** "
    "columns. Gene IDs should be Ensembl identifiers (for example `ENSG00000186092`)."
)

sample_file = st.file_uploader("Sample file", type=["csv", "tsv"])
num_genes = st.number_input(
    "Number of highly variable genes",
    min_value=1,
    value=2000,
    step=100,
    help="Filters the GTEx reference to the top N most variable genes (CLI --num-genes).",
)
reference_file = st.file_uploader(
    "Optional custom reference matrix",
    type=["csv", "gct", "tsv"],
    help="Leave empty to use the bundled GTEx reference matrix.",
)


def _write_temp_upload(uploaded_file) -> str:
    suffix = os.path.splitext(uploaded_file.name)[1] or ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name


if st.button("Run Classifier"):
    if sample_file is None:
        st.error("Please upload a sample CSV or TSV file.")
    else:
        sample_path = None
        reference_path = None
        try:
            from gtex_tissue_classifier.architecture import run_classifier

            sample_path = _write_temp_upload(sample_file)
            if reference_file is not None:
                reference_path = _write_temp_upload(reference_file)

            ranked_tissues = run_classifier(
                sample_path=sample_path,
                reference_path=reference_path,
                num_genes=int(num_genes),
            )

            top_tissue, top_score = ranked_tissues[0]
            st.success(f"Top match: **{top_tissue}** (Spearman {top_score:.4f})")

            top_5 = ranked_tissues[:5]
            tissues = [item[0] for item in top_5]
            correlations = [item[1] for item in top_5]
            fig, ax = plt.subplots()
            ax.barh(tissues, correlations, height=0.5)
            ax.set_title("Highest Likelihood Tissue Matches")
            ax.set_xlabel("Spearman Correlation")
            ax.set_ylabel("Tissue Type")
            ax.invert_yaxis()
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        except (ValueError, FileNotFoundError) as exc:
            st.error(str(exc))
        finally:
            for path in (sample_path, reference_path):
                if path and os.path.exists(path):
                    os.remove(path)
