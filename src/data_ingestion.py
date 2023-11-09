import json
from typing import Tuple

import pandas as pd
from pandas import DataFrame


def load_csv_data(
    drugs_path: str,
    pubmed_csv_path: str,
    clinical_trials_path: str,
    pubmed_json_path: str,
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    drugs_data: DataFrame = pd.read_csv(drugs_path)

    # Load the PubMed CSV data
    pubmed_csv_data: DataFrame = pd.read_csv(pubmed_csv_path)

    # Load the PubMed JSON data
    with open(pubmed_json_path, "r") as file:
        pubmed_json_list = json.load(file)

    pubmed_json_data: DataFrame = pd.DataFrame(pubmed_json_list)

    # Concatenate the PubMed CSV and JSON data into one DataFrame, ensuring no ID conflicts
    pubmed_data: DataFrame = pd.concat(
        [pubmed_csv_data, pubmed_json_data], ignore_index=True
    )

    clinical_trials_data: DataFrame = pd.read_csv(clinical_trials_path)

    return drugs_data, pubmed_data, clinical_trials_data
