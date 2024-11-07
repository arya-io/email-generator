# Import the regular expression library to perform text manipulation and cleaning operations
import re  

# Define the clean_text function that performs various cleaning operations on the input text
def clean_text(text):
    """
    A utility function that cleans the input text by performing several text cleaning operations.
    It removes HTML tags, URLs, special characters, and extra spaces.

    :param text: The raw input text that needs to be cleaned.
    :return: The cleaned version of the input text.
    """

    # Remove HTML tags using a regular expression pattern
    # The pattern <[^>]*?> matches any HTML tags and removes them
    text = re.sub(r'<[^>]*?>', '', text)  # Removes HTML tags
    
    # Remove URLs from the text
    # The regular expression matches both http:// and https:// URLs
    # It ensures that any link present in the text is removed
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)  # Removes URLs
    
    # Remove special characters from the text (keeping only alphanumeric characters and spaces)
    # This will remove characters like punctuation marks, symbols, etc.
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Removes special characters
    
    # Replace multiple consecutive spaces with a single space
    # This is useful to normalize the text and ensure no excess spaces between words
    text = re.sub(r'\s{2,}', ' ', text)  # Replaces multiple spaces with a single space
    
    # Remove leading and trailing spaces from the text
    # This ensures that the text starts and ends without unnecessary whitespace
    text = text.strip()  # Trims leading and trailing whitespace
    
    # Remove any extra whitespace between words (i.e., reduces all internal spaces to a single space)
    # It ensures the text is uniform and formatted correctly
    text = ' '.join(text.split())  # Joins words with a single space, removing extra spaces
    
    # Return the cleaned text
    return text
