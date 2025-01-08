import os
import argparse
from io import BytesIO
from PyPDF2 import PdfReader
import urllib
import requests
import pickle
from words import words  # Import words from words.py

def save_data(filepath, data):
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        print(f'[ERROR]: Could not save data to {filepath}. {e}')

def search_papers(start, end, filepath):
    items = {word: [] for word in words}

    while start < end:
        # Construct the URL for the PDF file
        url = f'https://www.nber.org/system/files/working_papers/w{start}/w{start}.pdf'
        try:
            # Open the URL and read the PDF file
            print(f'[OPENING URL]: {url}')
            wFile = urllib.request.urlopen(url)
            bytes_stream = BytesIO(wFile.read())
            reader = PdfReader(bytes_stream)
            all_text = ""
            # Extract text from each page of the PDF
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text:
                        all_text += page.extract_text().lower()  # Convert text to lowercase
                except ValueError as e:
                    print(f'[ERROR EXTRACTING TEXT FROM PAGE]: {e}')
                    
            # Search for each word in the extracted text
            print(f'[SEARCHING \U0001F50D]')
            for word in words:
                if word.lower() in all_text and start not in items[word]:
                    items[word].append(start)
                    print(f'[FOUND \U0001F60D]')
                    save_data(filepath, items)

        except urllib.error.HTTPError as e:
            print(f'[ERROR]: {e}')
        start += 1

def main():
    # Parse command-line arguments and initiate the search
    parser = argparse.ArgumentParser(description='Search for words in NBER working papers.')
    parser.add_argument('start', type=int, help='Start paper number')
    parser.add_argument('end', type=int, help='End paper number')
    parser.add_argument('--filepath', default='pdfsearch_results.pkl', help='Filepath to save search results')
    args = parser.parse_args()

    search_papers(args.start, args.end, args.filepath)

if __name__ == '__main__':
    main()
