import os
import argparse
from generators.cortex_scenario import generate_cortex_scenario
from utils.loader import load_nodes
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    logger.info("Starting scenario generation...")
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlapping", type=str, default="false")
    parser.add_argument("--signal_duration", type=float, default=60.0)
    args = parser.parse_args()

    os.makedirs("scenarios", exist_ok=True)

    try:
        nodes = load_nodes("configs/nodes.yaml")
        logger.info(f"Loaded {len(nodes)} nodes: {nodes}")
    except Exception as e:
        logger.error(f"Failed to load nodes: {e}")
        raise


    generate_cortex_scenario(nodes=nodes,
                            duration=6000,
                            image="ghcr.io/andreaj42/cortexforge:latest",
                            command='python3 /cortexlab/homes/andrea_joly/CorteXForge/forge/main.py',
                            description="Dataset Generator",
                            output_path="scenarios/scenario.yaml",
    )

    logger.info("Scenario generation completed.")

if __name__ == "__main__":
    main()
