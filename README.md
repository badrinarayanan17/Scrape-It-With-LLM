# Universal Web Scraping Agent using LLMs

This project demonstrates a universal web scraping agent that uses the Firecrawl framework to scrape data from the web and utilizes a large language model (LLM) to format the data into a JSON response. This project was demonstrated during a peer learning session to illustrate web scraping techniques and data extraction.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Contributing](#contributions)
- [Contact](#contact)

## Introduction

The universal web scraping agent is designed to scrape data from any web page using the Firecrawl framework and format the scraped data using a large language model (LLM) provided by Groq. The output is a JSON object containing the structured data extracted from the web page.

## Features

- Scrapes data from any web page using the Firecrawl framework.
- Formats the scraped data into a structured JSON object using Groq's LLM.
- Saves the raw scraped data in markdown format.
- Saves the formatted data in both JSON and Excel formats.

## Installation

To get started with this project, clone the repository and install the required dependencies.

git clone https://github.com/badrinarayanan17/Scrape-It-With-LLM.git
cd Scrape-It-With-LLM
pip install -r requirements.txt

## Usage

1) Create a .env file in the project directory and add your API keys for Firecrawl and Groq.

   FIRECRAWL_API_KEY=your_firecrawl_api_key
   
   GROQ_API_KEY=your_groq_api_key

3) Run the script to scrape data from a specified URL and format it.

   python app.py

4) The raw and formatted data will be saved in the output folder.

## Project Structure

   Scrape-It-With-LLM/
   
   ├── main.py
   
   ├── requirements.txt
   
   ├── .env
   
   ├── output/
   
   │ ├── rawData_<timestamp>.md
   
   │ ├── sorted_data_<timestamp>.json
   
   │ ├── sorted_data_<timestamp>.xlsx
   
   └── README.md
   
## Requirements

firecrawl-py

pandas

openpyxl

py-dotenv

groq

## Contributions

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

Name: BadriNarayanan S

Email: badrisrp3836@gmail.com

LinkedIn: [BadriNarayanan S](https://www.linkedin.com/in/badrinarayanan-s-43629522a/)









