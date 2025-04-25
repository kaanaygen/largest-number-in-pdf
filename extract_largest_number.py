import sys, os 
import pymupdf #import PyMuPDF for reading and parsing PDF file.

# Define characters that are allowed to mark the start and end of a valid numeric token.
VALID_START = "+-0123456789."
VALID_END   = "0123456789."

def preproc(token: str) -> str:
    """
    Cleans up (preprocesses) the raw extracted tokens found inside the text of the PDF;
    returns the cleaned up token, or None if the cleaned up token does not contain any numerical values.

    1 - Strip the token of potential wrapping parentheses, i.e. "(1)" -> "1" 
    2 - Iterate from start of the token to the end until a valid character is found, i.e. "+-0123456789."
    3 - Iterate from the end of the token until (at most) the identified start until a valid character is found, i.e. "+-0123456789."
    4 - Remove all characters outside the identified bounds of the token; 
        return None if no valid numeric characters are identified in the current token, that is when, token = token[i: j + 1] = ""
    5 - If the identified numeric token ends with '.', remove it.
    6 - Remove any thousand commas.
    7 - Return the preprocessed / cleaned up numeric token. 
    """
    
    # Remove parentheses at the start of a token, if it exists
    if token.startswith("("):
        token = token[1:]
   
    # Remove parentheses at the end of a token, if it exists
    if token.endswith(")"):
        token = token[:-1]
    
    # Initialize two pointers, i pointing to the start of the token, and j pointing to the end of the token.
    i, j = 0, len(token) - 1

    # Identify the start of the valid numerical sub-token
    while i <= len(token) - 1 and token[i] not in VALID_START:
        i += 1
    
    # Identify the end of the valid numerical sub-token
    while j > i and token[j] not in VALID_END:
        j -= 1
    
    # Extract the identified numerical body within the token
    token = token[i: j + 1]

    # If no valid numerical body exists within the token, i.e. token = "", return None.
    if not token:
        return None
    
    # If there is a trailing '.' at the end of the numerical token, strip it.
    if token.endswith('.'):
        token = token[:-1]
    
    # Remove the thousand commas inside the numerical token.
    token = token.replace(",", "")

    # Return the numerical token after preprocessing is done.
    return token

def find_largest_number(document: pymupdf.Document) -> int:
    """
    Iterate through every page of the .pdf document, parse all whitespace seperated tokens. 
    Pass all raw tokens into preproc() one by one, which cleans and returns a numeric value if a numeric sub-token
    exists within the raw token, and None otherwise. If a numeric value is identified and returned by 
    preproc(), cast it to a float(), compare it with the maximum numeric value identified so far. 
    Update the maximum value if the current numeric value returned by preproc() is larger than the so-far maximum.
    """

    # Initalize the maximum value identified to negative infinity.
    max_value = float('-inf')

    # Iterate through every page of the document.
    for page in document:

        # Extract all the text in the current page.
        text = page.get_text("text")

        # Split the extracted text on whitespace; iterate over the raw tokens.
        for raw_token in text.split():

            # Clean up the raw token
            preproc_token = preproc(raw_token)

            # If no numerical value is identified inside the current cleaned up token, continue onto the next candidate token.
            if not preproc_token:
                continue
            
            # Safety check; the identified cleaned-up numerical token must start with a digit or '+', or '-'.
            if preproc_token[0] in VALID_START:
                
                # Try to parse the identified numerical token as a float.
                try:
                    value = float(preproc_token)
                
                # Catch if an error arises in parsing the candidate numerical token as float; ignore it; continue on to the next raw token.
                except ValueError:
                    continue
                
                # If the cleaned-up float is larger than the so-far maximum, update the maximum. 
                if value > max_value:
                    max_value = value
   
    # If there was no numerical value identified within the document, return None; otherwise, return the identified maximum.
    return None if max_value == -float("inf") else max_value

if __name__ == "__main__":

    # Ensure the user runs the script on the command line providing exactly one command line argument: the path to the PDF file.
    # Otherwise, print the use message explaining the correct command line arguments and exit.

    if len(sys.argv) != 2:
        print("Use: python3 extract_largest_number.py <file.pdf>", file=sys.stderr)
        sys.exit(1)
    
    # Parse the path to the PDF file (command line argument).
    pdf_path = sys.argv[1]

    # Ensure a valid PDF file exists at the specified path. 
    # Otherwise, abort reading the PDF, show an error message explaining a PDF file is not found at the specified path.
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"'{pdf_path}' not found")
    
    # Open the PDF with pyMuPDF, search for the largest numerical value within, close the document.
    document = pymupdf.open(pdf_path)
    largest_number = find_largest_number(document)
    document.close()
    
    # If no numerical value identified within the PDF, print an explanatory message.
    if not largest_number:
        print("No numerical value found in the document.")
    
    # If the largest numerical value found within the PDF is an integer, drop the ".0" at the end, add thousand commas, print the number.
    if largest_number.is_integer():
        print(f"Largest number found: {int(largest_number):,}")
    
    # If the largest numerical value found within the PDF is a float, add thousand commas, print the number.
    else:
        print(f"Largest number found: {largest_number:,}")
    