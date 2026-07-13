# Specify computer
FROM continuumio/miniconda3:latest

# Create working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Build environment
RUN conda env create -f environment.yml

# Use environment by default
ENV PATH="/opt/conda/envs/gtex-env/bin:$PATH"

# Copy remaining Python scripts
COPY . .

# Run commands 
CMD ["python", "main.py"]