import json
from typing import Any, Dict


def write_graph_to_json(graph: Dict[str, Any], output_path: str) -> None:
    with open(output_path, "w") as json_file:
        json.dump(graph, json_file, indent=4)
