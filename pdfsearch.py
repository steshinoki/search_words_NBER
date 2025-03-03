"""
Script to scrape NBER papers and search for words.
Author: Stéphanie T. Shinoki

Modules:
    os, argparse, io.BytesIO, PyPDF2.PdfReader, urllib, pickle

Functions:
    save_data(filepath, data): Saves data to a file using pickle.
    search_papers(start, end, words_to_search, filepath): Searches for words in NBER papers.
    main(): Parses command-line arguments and starts the search.

Usage:
    python pdfsearch.py <start> <end> [--words <word1> <word2> ...] [--filepath <filepath>]

Arguments:
    start: Start paper number (int).
    end: End paper number (int).
    --words: Words to search (default: from words.py).
    --filepath: Filepath to save results (default: 'pdfsearch_results.pkl').
"""
import os
import urllib
import pickle
import argparse
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader

try:
    from words import words  # Try to import words from words.py
except ImportError:
    words = None  # If words.py does not exist, set words to None

def save_data(filepath, data):
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        print(f'[ERROR]: Could not save data to {filepath}. {e}')

def search_papers(start, end, words_to_search, filepath):
    items = {word: [] for word in words_to_search}

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
            for word in words_to_search:
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
    parser.add_argument('--words', nargs='+', default=words, help='List of words to search in the papers')
    parser.add_argument('--filepath', default='pdfsearch_results.pkl', help='Filepath to save search results')
    args = parser.parse_args()

    if args.words is None:
        raise ValueError("Error: words.py not found and no words provided in command line.")

    search_papers(args.start, args.end, args.words, args.filepath)

if __name__ == '__main__':
    main()
