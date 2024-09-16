"""
This script fetches data from the web, processes it using Python collections,
and writes the results to different file types like CSV, JSON, and text files.
"""

# Standard library imports
import csv
import pathlib
import json

# External library imports
import requests
import openpyxl
import pandas as pd
from io import StringIO  # Needed for reading CSV content

# Define the current project path
project_path = pathlib.Path.cwd()

# Create a sub-directory in project_path to hold files
data_path = project_path.joinpath('data')
data_path.mkdir(exist_ok=True)

############
# Define Fetch Functions
############

def fetch_txt_data(url):
    """Fetches text data from the web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch text data: {response.status_code}")
        return None

def fetch_csv_data(url):
    """Fetches CSV data from the web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # CSV content is in plain text
    else:
        print(f"Failed to fetch CSV data: {response.status_code}")
        return None

def fetch_json_data(url):
    """Fetches JSON data from the web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # JSON data
    else:
        print(f"Failed to fetch JSON data: {response.status_code}")
        return None

def fetch_excel_data(url):
    """Fetches Excel data from the web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Binary content for Excel files
    else:
        print(f"Failed to fetch Excel data: {response.status_code}")
        return None

############
# Define Save Functions
############

def save_text(filename, content):
    """Saves text data to a file."""
    file_path = data_path.joinpath(f"{filename}")
    with file_path.open('w') as file:
        file.write(content)
    print(f"Text data saved to {file_path}")

def save_json(filename, content):
    """Saves JSON data to a file."""
    file_path = data_path.joinpath(f"{filename}")
    with file_path.open('w') as file:
        json.dump(content, file, indent=4)
    print(f"JSON data saved to {file_path}")

def save_csv(filename, content):
    """Saves CSV data to a file using pandas."""
    file_path = data_path.joinpath(f"{filename}")
    df = pd.read_csv(StringIO(content))  # Convert the plain text into a DataFrame
    df.to_csv(file_path, index=False)
    print(f"CSV data saved to {file_path}")

def save_excel(filename, content):
    """Saves Excel data to a file."""
    file_path = data_path.joinpath(f"{filename}")
    with open(file_path, 'wb') as file:
        file.write(content)  # Save binary content directly
    print(f"Excel data saved to {file_path}")

#########
# txt file process
#########

def process_text_data(folder_name, filename, processed_filename):
    """Processes text data to count total words, unique words, and frequency of each word."""
    input_file_path = pathlib.Path(folder_name) / filename
    output_file_path = pathlib.Path(folder_name) / processed_filename

    try:
        with open(input_file_path, 'r') as file:
            text = file.read()

        # List of all words
        words = text.split()
        
        # Set of unique words
        unique_words = set(words)
        
        # Dictionary to store word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        total_words = len(words)
        unique_word_count = len(unique_words)
        
        # Write results to the processed file
        with open(output_file_path, 'w') as file:
            file.write(f"Total words: {total_words}\n")
            file.write(f"Unique words: {unique_word_count}\n")
            file.write(f"Word frequencies:\n")
            for word, freq in word_freq.items():
                file.write(f"{word}: {freq}\n")
        
        print(f"Text data processed and saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing text data: {e}")


#########
# csv file process
#########

def process_csv_data(folder_name, filename, processed_filename):
    """Processes CSV data to compute statistics for numeric columns and save as tuples."""
    input_file_path = pathlib.Path(folder_name) / filename
    output_file_path = pathlib.Path(folder_name) / processed_filename

    try:
        df = pd.read_csv(input_file_path)

        # List of tuples for each row
        rows_as_tuples = [tuple(row) for row in df.to_numpy()]

        stats = {}
        for column in df.select_dtypes(include=['number']).columns:
            stats[column] = {
                'Mean': df[column].mean(),
                'Median': df[column].median(),
                'Standard Deviation': df[column].std(),
                'Max': df[column].max(),
                'Min': df[column].min()
            }
        
        with open(output_file_path, 'w') as file:
            file.write(f"Rows as tuples:\n")
            for row in rows_as_tuples:
                file.write(f"{row}\n")
            file.write("\nStatistics for numeric columns:\n")
            for column, metrics in stats.items():
                file.write(f"\n{column}:\n")
                for key, value in metrics.items():
                    file.write(f"{key}: {value}\n")

        print(f"CSV data processed and saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing CSV data: {e}")


#########
# json file process
#########

def process_json_data(folder_name, filename, processed_filename):
    """Processes JSON data to extract and summarize information."""
    input_file_path = pathlib.Path(folder_name) / filename
    output_file_path = pathlib.Path(folder_name) / processed_filename

    try:
        with open(input_file_path, 'r') as file:
            data = json.load(file)  # This is a dictionary

        # Example processing: Count items in the dictionary
        item_count = len(data)  # assuming the top-level is a dictionary or list

        with open(output_file_path, 'w') as file:
            file.write(f"Item count: {item_count}\n")
            file.write(f"JSON data summary:\n")
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
        
        print(f"JSON data processed and saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing JSON data: {e}")

#########
# excel file process
#########
def process_excel_data(folder_name, filename, processed_filename):
    """Processes Excel data to compute statistics for numeric columns."""
    input_file_path = pathlib.Path(folder_name) / filename
    output_file_path = pathlib.Path(folder_name) / processed_filename

    try:
        df = pd.read_excel(input_file_path)

        stats = {}
        for column in df.select_dtypes(include=['number']).columns:
            stats[column] = {
                'Mean': df[column].mean(),
                'Median': df[column].median(),
                'Standard Deviation': df[column].std(),
                'Max': df[column].max(),
                'Min': df[column].min()
            }

        with open(output_file_path, 'w') as file:
            for column, metrics in stats.items():
                file.write(f"Statistics for {column}:\n")
                for key, value in metrics.items():
                    file.write(f"{key}: {value}\n")
                
        print(f"Excel data processed and saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing Excel data: {e}")

#########
# Main Function
#########
def main():
    """Main function to demonstrate the module's capabilities."""

    # Ensure the data folder exists
    pathlib.Path('data').mkdir(exist_ok=True)

    # Define URLs
    txt_url = 'https://raw.githubusercontent.com/denisecase/datafun-03-spec/main/data.txt'
    csv_url = 'https://raw.githubusercontent.com/denisecase/datafun-03-spec/main/data.csv'
    excel_url = 'https://raw.githubusercontent.com/denisecase/datafun-03-spec/main/data.xls'
    json_url = 'https://raw.githubusercontent.com/denisecase/datafun-03-spec/main/data.json'

    # Define filenames
    txt_filename = 'data.txt'
    csv_filename = 'data.csv'
    excel_filename = 'data.xls'
    json_filename = 'data.json'

    # Fetch and save text data
    text_content = fetch_txt_data(txt_url)
    if text_content:
        save_text(txt_filename, text_content)
        process_text_data('data', txt_filename, 'processed_text.txt')

    # Fetch and save CSV data
    csv_content = fetch_csv_data(csv_url)
    if csv_content:
        save_csv(csv_filename, csv_content)
        process_csv_data('data', csv_filename, 'processed_csv.txt')

    # Fetch and save Excel data
    excel_content = fetch_excel_data(excel_url)
    if excel_content:
        save_excel(excel_filename, excel_content)
        process_excel_data('data', excel_filename, 'processed_excel.txt')

    # Fetch and save JSON data
    json_content = fetch_json_data(json_url)
    if json_content:
        save_json(json_filename, json_content)
        process_json_data('data', json_filename, 'processed_json.txt')

if __name__ == '__main__':
    main()
