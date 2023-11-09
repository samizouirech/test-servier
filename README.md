# Data Pipeline Project

## Overview

This project is a Python-based data pipeline that processes datasets related to drugs, PubMed articles, and clinical trials. It loads data from CSV and JSON files, processes it to create a graph structure, and outputs the result in JSON format.

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for package management and dependency resolution.
- [Hydra](https://hydra.cc/) for configuration management.
- [Pre-commit](https://pre-commit.com/) for code quality checks.
- [Docker](https://www.docker.com/) for containerization and running Airflow.
- [Supervisor](http://supervisord.org/) for process control (if not using Docker and Airflow).


## Installation

To set up the project environment and install the necessary dependencies using Poetry, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/samizouirech/test-servier.git
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

### Using Python directly

To run the data pipeline, ensure you are within the Poetry virtual environment and then execute the main script:

```sh
python main.py
```
### Using Docker with Airflow
To run the pipeline using Airflow within Docker, follow these steps:

1. Build the Docker image:

```sh
docker build -t data-pipeline-airflow .
```
2. Run the Airflow webserver (this command also initializes the database if it's the first run):

```sh
docker run -p 8080:8080 data-pipeline-airflow
```
After the webserver starts, visit http://localhost:8080 in your browser to access the Airflow UI.

The Dockerfile should be set up to copy the DAG files into the container, install Airflow, and initialize the database.

### Using Supervisor
Run the pipeline managed by Supervisor, which will handle starting and stopping the Airflow webserver and scheduler:

```sh
supervisord -c supervisord.conf
```


## Project Structure
- main.py: Orchestrates the data pipeline execution.
- pyproject.toml: Defines Python dependencies and project metadata for Poetry.
- conf/: Contains configuration files managed by Hydra.
- dags/: Contains Airflow DAG files defining the pipeline workflows.
- src/: Source code for data ingestion, processing, and output modules.
- data/: Input datasets for the data pipeline.
- supervisord.conf: Configuration file for running the project with Supervisor.
- .github/workflows/: CI/CD workflows for GitHub Actions.
- .pre-commit-config.yaml: Configuration for pre-commit hooks.
- Dockerfile: Instructions for building the Docker image for this project.

## Continuous Integration and Deployment
The .github/workflows/ directory contains GitHub Actions workflows for continuous integration and deployment. These workflows automate testing, building, and deploying the project.

## Acknowledgments
Hydra for configuration management.
Pre-commit for automated code quality checks.
Poetry for Python packaging and dependency management.