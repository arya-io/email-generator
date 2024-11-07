# Import necessary libraries
import streamlit as st  # Streamlit is used to build the web interface for the app.
from langchain_community.document_loaders import WebBaseLoader  # Used to scrape data from a URL (job listing page).
from chains import Chain  # Importing the Chain class that interacts with the language model for generating emails and extracting jobs.
from portfolio import Portfolio  # Importing the Portfolio class to manage and query the user's portfolio.
from utils import clean_text  # Importing the clean_text function to clean the scraped data from the web.

# Function to create and configure the Streamlit app
def create_streamlit_app(llm, portfolio, clean_text):
    # Set the title of the app
    st.title("📧 Cold Mail Generator")

    # Display a description of what the app does
    st.markdown("""
    This app is a **Cold Email Generator** designed to help business professionals quickly generate personalized cold emails for job opportunities 
    listed on websites. It allows users to input a URL for a job listing, then extracts relevant job details (such as role, skills, and experience) 
    from the page using AI. The user can also input their name, designation, and company details, which are then used to automatically craft a professional 
    cold email tailored to the job description. The app also integrates the user’s company portfolio links to showcase relevant work.
    """)

    # Create input fields for user to provide personal details like name, designation, and company
    user_name = st.text_input("Enter your name:", placeholder="Your Name")  # Input field for the user's name
    user_designation = st.text_input("Enter your designation:", placeholder="Your Designation in the Company")  # Input for job designation
    user_company = st.text_input("Enter your company name:", placeholder="Your Company Name")  # Input for the company name
    
    # Create an input field for the user to provide a URL (job listing URL)
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43835?from=job%20search%20funnel")  # Default URL for the job listing
    submit_button = st.button("Submit")  # Submit button to initiate processing

    # When the submit button is clicked, execute the following logic
    if submit_button:
        try:
            # Step 1: Scrape job listing data from the URL using WebBaseLoader
            loader = WebBaseLoader([url_input])  # Initialize WebBaseLoader with the URL provided by the user
            data = clean_text(loader.load().pop().page_content)  # Scrape and clean the page content using clean_text function

            # Step 2: Load the portfolio data
            portfolio.load_portfolio()  # Load portfolio data (if not already loaded)

            # Step 3: Extract job details using the language model
            jobs = llm.extract_jobs(data)  # Extract job data from the cleaned content using the language model (LLM)

            # Step 4: Process each job posting
            for job in jobs:
                skills = job.get('skills', [])  # Extract the skills required for the job (default to empty list if not found)
                
                # Step 5: Query portfolio for relevant links based on the job's required skills
                links = portfolio.query_links(skills)  # Query portfolio using the extracted skills to find relevant links
                
                # Step 6: Generate a personalized cold email using the extracted job data, portfolio links, and user inputs
                email = llm.write_mail(job, links, user_name, user_designation, user_company)  # Call the LLM to generate the email
                
                # Step 7: Display the generated email in the app (in Markdown format)
                st.code(email, language='markdown')  # Display the email in a formatted block of code

        except Exception as e:
            # Step 8: If any error occurs during the process, display an error message
            st.error(f"An Error Occurred: {e}")  # Show the error message to the user if something goes wrong

# Main function to initialize and run the app
if __name__ == "__main__":
    # Initialize instances of Chain and Portfolio classes
    chain = Chain()  # Create an instance of the Chain class (used for job extraction and email generation)
    portfolio = Portfolio()  # Create an instance of the Portfolio class (used to manage and query the user's portfolio)
    
    # Configure the layout and appearance of the Streamlit app
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")  # Set the page layout and title
    
    # Call the function to create and run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)  # Pass the instances of chain, portfolio, and clean_text to the function
