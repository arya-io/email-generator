import pandas as pd  # For handling data in tabular form, such as reading CSV files
import uuid  # For generating unique IDs for portfolio entries

# Importing pysqlite3 and reassigning it to 'sqlite3' for compatibility with Chroma
__import__('pysqlite3')  
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Importing the chromadb library to work with the Chroma vector database
import chromadb  

# Define the Portfolio class which handles portfolio data and Chroma database interactions
class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        """
        Initialize the Portfolio object with the given file path to the portfolio CSV.
        
        :param file_path: The path to the CSV file containing portfolio data.
        """
        self.file_path = file_path  # Assign the file path to an instance variable
        self.data = pd.read_csv(file_path)  # Load the CSV file data into a pandas DataFrame
        self.chroma_client = chromadb.PersistentClient('vectorstore')  # Initialize Chroma client for persistent storage
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")  # Get or create the 'portfolio' collection in Chroma

    def load_portfolio(self):
        """
        Load portfolio data into the Chroma vector database, if it's not already loaded.
        It adds documents to the Chroma database with tech stack and portfolio links.
        """
        # Check if the Chroma collection is empty
        if not self.collection.count():  
            # Iterate over each row in the loaded DataFrame to add portfolio data to Chroma
            for _, row in self.data.iterrows():
                # Add each portfolio entry to the collection
                self.collection.add(
                    documents=row["Techstack"],  # The 'Techstack' column is the document content
                    metadatas={"links": row["Links"]},  # The 'Links' column is stored as metadata
                    ids=[str(uuid.uuid4())]  # Generate a unique ID for each portfolio entry using UUID
                )

    def query_links(self, skills):
        """
        Query the Chroma database to find portfolio entries that match the provided skills.
        
        :param skills: A list or string of skills to search for in the portfolio data.
        :return: A list of metadata containing the matching portfolio links.
        """
        # Perform the query on the Chroma collection using the provided skills and return the top 2 results
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])  # Get metadata (links) of the matching results
