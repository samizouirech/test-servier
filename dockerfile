FROM python:3.11.4-slim as build

# Set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2

WORKDIR /app
COPY pyproject.toml ./

# Install Poetry and dependencies
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt --without-hashes \
    && sed 's/;.*//' requirements.txt > clean_requirements.txt \
    && rm requirements.txt \
    && mv clean_requirements.txt requirements.txt


### Final stage
FROM python:3.11.4-slim as final

# Set work directory
ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

# Copy the requirements.txt from the build stage
COPY --from=build /app/requirements.txt .

# Install Airflow and other dependencies from the requirements file
RUN set -ex \
    # Create a non-root user and group
    && addgroup --system --gid 1001 airflowgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home airflowuser \
    # Upgrade the package index and install security upgrades
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y supervisor \
    && pip install -r requirements.txt --ignore-installed \
    # Install Airflow with the specified version and constraints
    && pip install "apache-airflow[celery]==2.7.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.8.txt" \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R airflowuser:airflowgroup /opt/airflow

# Create data_output directory and give write access to airflowuser
RUN mkdir -p $AIRFLOW_HOME/data_output && \
    chown -R airflowuser:airflowgroup $AIRFLOW_HOME/data_output
# Switch to the new user
USER airflowuser

# Add the local bin to the PATH for the non-root user
ENV PATH="${PATH}:/home/airflowuser/.local/bin"

# Copy your DAGs, modules, data files, configuration files, and other necessary files
COPY dags/ $AIRFLOW_HOME/dags/
COPY src/ $AIRFLOW_HOME/src/
COPY data/ $AIRFLOW_HOME/data/

# Add the dags folder to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:$AIRFLOW_HOME/"

# Add supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Initialize the Airflow database and create a user
RUN airflow db init && \
    airflow users create \
    --username admin \
    --password admin \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email admin@example.com 

# The command to run supervisord when the container starts
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]