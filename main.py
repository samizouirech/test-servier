import hydra
from omegaconf import DictConfig

from src.data_ingestion import load_csv_data
from src.data_output import write_graph_to_json
from src.data_processing import create_drug_graph
from src.utils import log


# Specify the version_base parameter and set hydra.job.chdir to False
@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    # Hydra changes the working directory, so use the original working directory
    original_cwd = hydra.utils.get_original_cwd()
    log("Starting data ingestion...")
    drugs_data, pubmed_data, clinical_trials_data = load_csv_data(
        f"{original_cwd}/{cfg.drugs_path}",
        f"{original_cwd}/{cfg.pubmed_path}",
        f"{original_cwd}/{cfg.clinical_trials_path}",
        f"{original_cwd}/{cfg.pubmed_json_path}",
    )

    log("Starting data processing...")
    graph = create_drug_graph(drugs_data, pubmed_data, clinical_trials_data)

    log("Starting data output...")
    write_graph_to_json(graph, f"{original_cwd}/{cfg.output_json_path}")

    log(
        f"Data pipeline completed successfully. Output saved to: {cfg.output_json_path}"
    )


if __name__ == "__main__":
    main()
