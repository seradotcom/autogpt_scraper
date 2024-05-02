# Web Scraper for AI Tools

This project is a Python-based web scraper designed to extract information about AI tools from a specific website and store it in a MySQL database.

## Features
- Scrapes tool names, descriptions, licensing, subscription models, and other relevant information.
- Utilizes Google Search API for additional context and insights.
- Leverages OpenAI's GPT-3 model for intelligent classification and description generation.
- Stores scraped data efficiently in a MySQL database.

## Requirements
- Python 3.7+
- aiohttp
- beautifulsoup4
- langchain
- mysql-connector-python
- openai
- python-dotenv
- selenium
- webdriver_manager

## Environment Variables
Create a file named `.env` in the project's root directory and add the following environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key.
- `SERPER_API_KEY`: Your Google Serper API key.


## Installation
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Configure the database connection details in `db_connection.py`.
2. Run the scraper:
   ```bash
   python main.py
   ```
3. The scraped data will be stored in the MySQL database.


## Notes
- The target website and specific HTML elements might require adjustments in the `scraper.py` file depending on the structure of the site.
- The prompts in `prompt_repo.py` can be customized to improve the accuracy and quality of the generated descriptions and classifications.
- Consider implementing error handling and logging for more robust operation.
```
