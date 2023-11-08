# Data Pipeline Project

## Overview

This project is a Python-based data pipeline that processes datasets related to drugs, PubMed articles, and clinical trials. It loads data from CSV and JSON files, processes it to create a graph structure, and outputs the result in JSON format.

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for package management and dependency resolution.
- Hydra for configuration management.
- Pre-commit for code quality checks.

## Installation

To set up the project environment and install the necessary dependencies using Poetry, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://your-repository-url.com/servier_test/data-pipeline-project.git
    cd data-pipeline-project
    ```

2. Install the dependencies using Poetry:

    ```sh
    poetry install
    ```

   This command will create a virtual environment and install all the dependencies listed in the `pyproject.toml` file.

3. Activate the Poetry virtual environment:

    ```sh
    poetry shell
    ```

4. Install pre-commit hooks within the virtual environment:

    ```sh
    pre-commit install
    ```

## Configuration

Hydra is used for configuration management. The configuration files are located in the `conf` directory. Update the `config.yaml` file to set the paths for the input datasets and the output file.

## Running the Project

To run the data pipeline, ensure you are within the Poetry virtual environment and then execute the main script:

```sh
python main.py
```

## Project Structure
- main.py: The main script that orchestrates the data pipeline.
- conf/: Directory containing configuration files for Hydra.
- data_ingestion/: Module for loading data from various sources.
- data_processing/: Module for processing and transforming data.
- data_output/: Module for outputting data to files or databases.
- utils/: Utility functions and classes used across the project.
- data/: Directory containing input data files like drugs.csv, pubmed.csv, and clinical_trials.csv.
- .pre-commit-config.yaml: Configuration file for pre-commit hooks.

## Data Ingestion
The data_ingestion module is responsible for loading data from drugs.csv, pubmed.csv, clinical_trials.csv, and pubmed.json. It ensures that all entries from the JSON file have a valid id, merging the content of pubmed.csv and pubmed.json into one DataFrame.

## Data Processing
The data_processing module processes the ingested data to create a graph structure that connects drugs to PubMed articles and clinical trials based on mentions.

## Data Output
The data_output module writes the processed graph data structure to an output JSON file.

## Utils
The utils module contains helper functions like log for logging messages to the console.


## Acknowledgments
- Hydra for configuration management.
- Pre-commit for automated code quality checks.
- Poetry for Python packaging and dependency management