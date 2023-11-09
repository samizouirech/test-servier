FROM apache/airflow:2.1.0

# Set the working directory in the container
WORKDIR /opt/airflow

# Install any system dependencies
USER root
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to the Airflow user
USER airflow

# Install additional Python dependencies (if any)
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy your DAG files to the container
COPY dags/ ./dags/

# Copy your Python modules
COPY src/ ./src/


# Copy your data files
COPY data/ ./data/

# Copy your Hydra configuration files
COPY conf/ ./conf/

# Copy other necessary files like .pre-commit-config.yaml if needed
COPY .pre-commit-config.yaml .


# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# The command to run when the container starts
CMD ["airflow", "webserver"]
