import json
from collections import defaultdict

json_file_path = "/home/sami/servier_test/data-pipeline-project/data/drug_graph.json"


def load_json_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def find_journal_with_most_drug_mentions(data):
    journal_drug_mentions = defaultdict(set)

    # Update to accumulate mentions from both pubmed and clinical_trials
    for drug, details in data.items():
        for article in details.get("pubmed", []):
            journal = article["journal"]
            journal_drug_mentions[journal].add(drug)

        for trial in details.get("clinical_trials", []):
            journal = trial["journal"]
            journal_drug_mentions[journal].add(drug)

    # Count the number of unique drugs mentioned by each journal
    journal_counts = {
        journal: len(drugs) for journal, drugs in journal_drug_mentions.items()
    }
    print(journal_drug_mentions)

    # Identify the journal with the maximum count of unique drug mentions
    most_mentions_journal = max(journal_counts, key=journal_counts.get)
    print(most_mentions_journal)
    return most_mentions_journal, journal_counts[most_mentions_journal]


data = load_json_data(json_file_path)


journal, count = find_journal_with_most_drug_mentions(data)
print(
    f"The journal with the most different drug mentions is: {journal} with {count} mentions."
)
