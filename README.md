# Assignment fot the short-term-rental-prices dataset
This is my contribution for the Udacity assignment 2 at the frame 
of the lessons BUILDING A REPRODUCIBLE MODEL WORKFLOW. The project
apply mlflow pipeline that performs loading dataset, checking data,
split data to training and testing sets, running hyper-parameter
optimization using hydra and evaluating the best model. Also, it
saves all step outputs on  Weights and Biases

# Links:
link for W&B:
https://wandb.ai/joesider9/nyc_airbnb?workspace=user-joesider9

link for github:
https://github.com/joesider9/short-term-rental-prices_NYC

# How to use:
Anaconda or miniconda should be installed before.

You should have an account to Weights and Biases:
Then

> wandb login [your API key]

Install the required libraries
> conda env create -f environment.yml
> 
> conda activate nyc_airbnb_dev

Then run:
> mlflow run .
> 
