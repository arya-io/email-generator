# Import necessary libraries
import os  # Standard library for interacting with the operating system, though not actively used here
import streamlit as st  # Streamlit library, for web app integration (not directly used in this file)
from langchain_groq import ChatGroq  # langchain_groq provides an interface to interact with Groq, the LLM provider
from langchain_core.prompts import PromptTemplate  # Used to create prompts to interact with the LLM
from langchain_core.output_parsers import JsonOutputParser  # Parses output from the LLM in JSON format
from langchain_core.exceptions import OutputParserException  # Handles exceptions when parsing LLM output

# Define the Chain class that will interact with the language model (Groq)
class Chain:
    def __init__(self):
        # Initialize the Chain class with a Groq model instance
        self.llm = ChatGroq(temperature=0, groq_api_key=st.secrets["groq_api_key"], model_name="llama-3.1-70b-versatile")
        # Groq API key is fetched from Streamlit secrets for security
        # model_name specifies the LLM version (Llama 3.1 70B versatile model)

    def extract_jobs(self, cleaned_text):
        # Define the function to extract job listings from cleaned text using LLM
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        # Create a prompt template for job extraction. The template defines the task for the model, and it expects a structured JSON response.
        chain_extract = prompt_extract | self.llm  # Combine the prompt with the language model (LLM) using the 'pipe' operator
        res = chain_extract.invoke(input={"page_data": cleaned_text})  # Invoke the model with the cleaned text as input

        try:
            # Parse the model's output into JSON format
            json_parser = JsonOutputParser()  # Initialize the JSON parser
            res = json_parser.parse(res.content)  # Parse the model response into a Python list or dict
        except OutputParserException:
            # If there is an error during parsing, raise an exception indicating the context is too large
            raise OutputParserException("Context too big. Unable to parse jobs.")
        
        # Return the parsed response, ensure it's a list of jobs (in case there's only one job returned)
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, user_name, user_designation, user_company):
        # Define the function to generate a cold email using the job description and portfolio links
        prompt_email = PromptTemplate.from_template(
            f"""
            ### JOB DESCRIPTION:
            {{job_description}}

            ### INSTRUCTION:
            You are {user_name}, a {user_designation} at {user_company}. {user_company} is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of {user_company} 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase {user_company}'s portfolio: {{link_list}}
            Remember you are {user_name}, {user_designation} at {user_company}. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        # The prompt template is used to generate a personalized cold email by providing job description and portfolio links as input
        chain_email = prompt_email | self.llm  # Combine the prompt with the language model using the 'pipe' operator
        res = chain_email.invoke({"job_description": str(job), "link_list": links})  # Invoke the model with the job description and links

        return res.content  # Return the generated email as the response
