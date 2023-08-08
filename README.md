# Scribe (base)

## Instructions

- Setup a virtual environment and install all the required libraries from the Pipfile. Preferably `pipenv`, you can install it using `pip install pipenv` (make sure you don't mess up between pip/pip3).
- After installing the required dependencies, setup your Google Cloud API credentials by exporting the JSON file from GCP platform (more info on how to export your service account key could be found here: https://stackoverflow.com/a/46290808). Alternatively, you could also setup your API keys using the Google Cloud CLI or other options available on their docs.
- Setup a `.env` file with all the API keys. Have a look at `.env.sample` file for reference.
- Activate the virtual environment (if using `pipenv`, you could do that by entering `pipenv shell` into your terminal).
- To generate OCR outputs for images in a folder, run `python ocr.py [folder name where the files are] [folder name where you want to export the files to (could be the same folder)]`. If your Google Cloud configuration is correct, you'll see the text files in the output folder.
- To run the parser on the said files, run `python main.py [folder where the OCR generated text files are] [name of the output file]` and the program will generate a CSV file containing the parsed info.

## Example

An example of how the parser works.

```
python base.py files/january_data <filename>

```

This will generate two files, a `<filename>.jsonl` and an `unparseable.jsonl`. The latter contains info on unparseable files that were either corrupt or simply couldn't be parsed due to a number of errors.

Later, you can convert the jsonl to CSV by running the `main.py` script like this:

```
python main.py <filename>.json <output.csv>
```

This will generate the CSV file which you can then perform various actions on.

An example of how the OCR works.

```
python ocr.py files/january_images files/january_data
```

Thank you!
