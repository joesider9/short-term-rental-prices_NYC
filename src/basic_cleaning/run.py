#!/usr/bin/env python
"""
This is the script that run on basic_cleaning step
It reads the sample.csv Weights and Biases and removes the rows which has prices outside the interval
[min_price, max_price]
Inputs:  --input_artifact, str, the name of the input artifact
         --output_artifact, str, the name of the output file
         --output_type, str, the type of the output
         --output_description, str, the description of the output artifact
         --min_price, float, the value of minimum price
         --max_price, float, the value of the maximum price
Output: the file clean_sample.csv that is uploaded to Weights and Biases

Date: 14 Oct 2022

Author: joesider
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(parameters):
    """
    this is the main function that clean the data.
    Inputs:
            args: ArgumentParser, contains input_artifact, output_artifact, output_type, output_description, min_price,
                  max_price
    Outputs:
            clean_sample.csv
    """
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(parameters)

    logger.info("Downloading artifact")
    artifact = run.use_artifact(parameters.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_csv(artifact_path)
    logger.info(f'Basic_cleaning starts...')
    # Drop outliers
    min_price = parameters.min_price
    max_price = parameters.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info(f'Basic_cleaning performed succesfully')

    # Write dataframe to csv
    df.to_csv(parameters.output_artifact, index=False)

    # Upload output artifact to Weights and Biases

    artifact = wandb.Artifact(
        parameters.output_artifact,
        type=parameters.output_type,
        description=parameters.output_description,
    )

    artifact.add_file(parameters.output_artifact)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Performs basic cleaning on the data and save the results in Weights & Biases")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help='the csv file saved on W&B as sample.csv',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='the name of the output file namely clean_sample.csv',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='The output should be a pandas dataframe (pd.Dataframe)',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help='The output is a dataframe with prices between min_price and max_price',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='The lower limit of prices',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='The upper limit of prices',
        required=True
    )


    args = parser.parse_args()

    go(args)
