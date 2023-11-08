from collections import defaultdict
from typing import Dict, List

from pandas import DataFrame


def create_drug_graph(
    drugs_data: DataFrame, pubmed_data: DataFrame, clinical_trials_data: DataFrame
) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    graph: Dict[str, Dict[str, List[Dict[str, str]]]] = defaultdict(
        lambda: {"pubmed": [], "clinical_trials": []}
    )

    for _, drug_row in drugs_data.iterrows():
        drug_atccode: str = drug_row["atccode"]
        drug_name: str = drug_row["drug"]

        related_pubmed: DataFrame = pubmed_data[
            pubmed_data["title"].str.contains(drug_name, case=False)
        ]
        for _, article in related_pubmed.iterrows():
            graph[drug_atccode]["pubmed"].append(
                {
                    "id": str(article["id"]),
                    "title": article["title"],
                    "date": article["date"],
                    "journal": article["journal"],
                }
            )

        related_trials: DataFrame = clinical_trials_data[
            clinical_trials_data["scientific_title"].str.contains(drug_name, case=False)
        ]
        for _, trial in related_trials.iterrows():
            graph[drug_atccode]["clinical_trials"].append(
                {
                    "id": str(trial["id"]),
                    "title": trial["scientific_title"],
                    "date": trial["date"],
                    "journal": trial["journal"],
                }
            )

    return graph
