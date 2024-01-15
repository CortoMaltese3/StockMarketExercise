# Example Assignment – Super Simple Stock Market

Assignment to create a Super Simple Stock Market Python application

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Automated Testing with GitHub Actions](#automated-testing-with-github-actions)

## Getting Started

### Prerequisites

Prerequisites required to run the project.

- black
- pandas
- python
- pytest

### Installation

Step-by-step instructions on how to install and set up the project.

#### Using Conda

1. Clone the repository from https://github.com/CortoMaltese3/StockMarketExercise
2. Change to the project directory: `cd StockMarketExercise`
3. Create a conda environment to work with: `conda env create -f environment.yml`
4. Activate the environment: `conda activate jpm`

#### Using Pip

1. Clone the repository from https://github.com/CortoMaltese3/StockMarketExercise
2. Change to the project directory: `cd StockMarketExercise`
3. Install the dependencies: `pip install -r requirements.txt`

## Usage

1. Change to the project directory: `cd StockMarketExercise`
2. Execute the main script: `python main.py`

## Running Tests

1. Change to the project directory: `cd StockMarketExercise`
2. Run all tests: `pytest tests`

## Automated Testing with GitHub Actions

Pushing code to the main branch or creating a pull request against it will automatically trigger the GitHub Actions workflow. This workflow runs the tests with pytest to ensure code changes do not break existing functionality.
