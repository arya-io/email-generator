# Cold Email Generator

This project is a **Cold Email Generator** built using Groq Cloud, ChromaDB, Langchain, Llama3.1 LLM, and Streamlit. It helps software and AI services companies automatically generate personalized cold emails for job opportunities posted on websites. The system extracts relevant job details from a given URL and tailors the email using user input such as their name, designation, and company details.

## Features

- **Cold Email Generation**: Automatically generate personalized cold emails based on job listings.
- **Job Data Extraction**: Extract job roles, skills, and experience requirements from a provided job URL.
- **Portfolio Integration**: Showcase company portfolio based on extracted skills.
- **User Personalization**: Allow users to input their name, designation, and company details for a personalized email.

## Tech Stack

- **Groq Cloud**: LLM backend for powerful language model processing.
- **ChromaDB**: Vector database to store and query portfolio links.
- **Langchain**: A framework for building language model-powered applications.
- **Llama 3.1 LLM**: Language model for generating emails and processing job data.
- **Streamlit**: Frontend for user input and email output visualization.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cold-email-generator.git
   cd cold-email-generator
   
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up **Groq API Key**:
- Create an account on Groq Cloud and obtain an API key.
- Store the API key in `secrets.toml`:

  ```bash  
  groq_api_key = "your_groq_api_key"
  
4. Prepare your portfolio CSV file (`my_portfolio.csv`) containing the tech stack and portfolio links.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py

2. Open the app in your browser at `http://localhost:8501`.

3. Input the following:

- **Your Name**: Name of the person sending the email.
- **Designation**: Job title or role of the person.
- **Company Name**: The name of the company you are representing.
- **Job Listing URL**: The URL of the job listing you want to apply to.
4. Click **Submit** to generate the cold email tailored to the job listing.

## Code Structure
- app.py: Main entry point that initializes the Streamlit app and handles user inputs.
- chains.py: Contains the logic for interacting with the Groq Cloud LLM, extracting job data, and generating emails.
- portfolio.py: Manages the company portfolio and queries relevant links based on job skills.
- utils.py: Contains utility functions for cleaning and sanitizing input text.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
