import streamlit as st
from langchain_community.document_loaders import WebBaseLoader  # Used to scrape data from a URL (job listing page).
from chains import Chain  # Importing the Chain class that interacts with the language model for extracting jobs and generating emails.
from portfolio import Portfolio  # Importing the Portfolio class to manage and query the user's portfolio.
from utils import clean_text  # Importing the clean_text function to clean the scraped data from the web.

# Function to create and configure the Streamlit app
def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # A description of what the app does
    st.markdown("""
    This app is a **Cold Email Generator** that helps business professionals create personalized cold emails for job opportunities. 
    Users can input a job listing URL, and the AI extracts key details (role, skills, experience). 
    By providing their name, designation, and company, users receive a tailored cold email, complete with portfolio links to highlight relevant work.
    """)

    # Creating input fields for user to provide personal details like name, designation, and company
    user_name = st.text_input("Enter your name:", placeholder="Your Name")
    user_designation = st.text_input("Enter your designation:", placeholder="Your Designation in the Company")
    user_company = st.text_input("Enter your company name:", placeholder="Your Company Name")
    
    # Creating an input field for the user to provide a URL (job listing URL)
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43835?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    # When the submit button is clicked, the following logic will get executed
    if submit_button:
        try:
            # Step 1: Scraping job listing data from the URL using WebBaseLoader
            loader = WebBaseLoader([url_input])  # Initializing WebBaseLoader with the URL provided by the user
            data = clean_text(loader.load().pop().page_content)  # Scraping and cleaning the page content using clean_text function

            # Step 2: Loading the portfolio data
            portfolio.load_portfolio()  # Loading portfolio data (if not already loaded)

            # Step 3: Extracting job details using the language model
            jobs = llm.extract_jobs(data)  # Extracting job data from the cleaned content using the language model (LLM)

            # Step 4: Processing each job posting
            for job in jobs:
                skills = job.get('skills', [])  # Extracting the skills required for the job (default to empty list if not found)
                
                # Step 5: Querying portfolio for relevant links based on the job's required skills
                links = portfolio.query_links(skills)  # Querying portfolio using the extracted skills to find relevant links
                
                # Step 6: Generating a personalized cold email using the extracted job data, portfolio links, and user inputs
                email = llm.write_mail(job, links, user_name, user_designation, user_company)  # Calling the LLM to generate the email
                
                # Step 7: Displaying the generated email in the app (in Markdown format)
                st.code(email, language='markdown')  # Displaying the email in a formatted block of code

        except Exception as e:
            # Step 8: If any error occurs during the process, display an error message
            st.error(f"An Error Occurred: {e}")  # Show the error message to the user if something goes wrong

# Main function to initialize and run the app
if __name__ == "__main__":
   
    chain = Chain()  # Create an instance of the Chain class
    portfolio = Portfolio()  # Create an instance of the Portfolio class
    
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")  # Set the page layout and title
    
    # Call the function to create and run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)  # Pass the instances of chain, portfolio, and clean_text to the function
