import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # User Inputs for name, designation, and company
    user_name = st.text_input("Enter your name:", value="Mohan")
    user_designation = st.text_input("Enter your designation:", value="BDE")
    user_company = st.text_input("Enter your company name:", value="AtliQ")
    
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43835?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load webpage content
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            
            # Load portfolio links
            portfolio.load_portfolio()

            # Extract jobs from the webpage
            jobs = llm.extract_jobs(data)
            
            # Process each job
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                
                # Generate the email using user inputs
                email = llm.write_mail(job, links, user_name, user_designation, user_company)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
