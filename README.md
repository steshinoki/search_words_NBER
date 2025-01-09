# NBER Working Papers Word Search

This project searches for specific words in NBER working papers and saves the results.

## Files

- `words.py`: Contains the list of words to search for.
- `pdfsearch.py`: Contains the main logic for downloading and searching the PDFs.

## Requirements

- Python 3.x
- PyPDF2
- requests

You can install the required packages using:

```bash
pip install PyPDF2 requests
```

## Usage

To run the search, use the following command:

```bash
python pdfsearch.py <start_paper_number> <end_paper_number> [--filepath <output_filepath>]
```

- `<start_paper_number>`: The starting paper number to search.
- `<end_paper_number>`: The ending paper number to search.
- `--filepath <output_filepath>`: (Optional) The file path to save the search results. Default is `pdfsearch_results.pkl`.

Example:

```bash
python pdfsearch.py 10000 10100 --filepath pdfsearch_results.pkl
```

## Output

The results are saved in a pickle file specified by the `--filepath` argument. The file contains a dictionary where keys are the words and values are lists of paper numbers where the words were found.

## Known Limitations

- The code ignores any PDF pages that have characters not recognized during text extraction. This may result in incomplete search results for some papers.

## License

This project is licensed under the MIT License.
