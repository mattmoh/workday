# Workday

Here is a space where I am building scripts to interact with your Workday tenant.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

### orchestrator

This script prompts the user for which script(s) they want to run. 

### workday_get_workers

This script sends a SOAP request to your tenant to retrieve an employee's record. The response is written to an output directory. If you are set up with a GMS tenant, by default if no Employee ID is given, Logan McNeil's data is returned.

### workday_put_accounting_center_batch

This script send a SOAP request to submit an Accounting Center Batch. You must know the Accounting Source Reference ID.

### clean_output_dir

This script deletes all files in the directory "output".

## Installation

To install the Workday Project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/workday.git
    ```
2. Navigate to the project directory:
    ```bash
    cd workday
    ```
3. Create an `.env` file and include the following:
    ```bash
    WORKDAY_USERNAME=username
    WORKDAY_PASSWORD=password
    WORKDAY_TENANT=tenant
    ACCOUNTING_SOURCE=accounting_source
    ```

## Usage

To start the application, run the docker container:

    docker-compose run --rm workday_api
    
Then, follow prompts from the Terminal.
    