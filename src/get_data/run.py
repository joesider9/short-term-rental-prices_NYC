#!/usr/bin/env python
"""
This script download a URL to a local destination

Created on Fri Oct  14

@author: joesider
"""
import argparse
import logging
import os

import wandb

from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(parameters):
    run = wandb.init(job_type="download_file")
    run.config.update(parameters)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info(f"Returning sample {parameters.sample}")
    logger.info(f"Uploading {parameters.artifact_name} to Weights & Biases")
    log_artifact(
        parameters.artifact_name,
        parameters.artifact_type,
        parameters.artifact_description,
        os.path.join(os.path.dirname(__file__), "data", parameters.sample),
        run,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download the required data")

    parser.add_argument(
        "--sample",
        type=str,
        help="Name of the sample to download",
        required=True
    )

    parser.add_argument(
        "--artifact_name",
        type=str,
        help="Name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_type",
        type=str,
        help="Output artifact type.",
        required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="A brief description of this artifact",
        required=True
    )

    args = parser.parse_args()

    go(args)
