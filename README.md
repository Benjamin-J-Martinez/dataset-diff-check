# Dataset Comparison Tool

A user-friendly application for comparing two CSV datasets with flexible column mapping options.

## Features

- Upload and compare two CSV files
- Three comparison modes:
  - All columns (automatic matching)
  - Single column comparison
  - Custom column mapping
- Clear visualization of differences
- Download mismatched rows as CSV
- User-friendly interface

## How to Run

1. **Double-click** `run_app.bat` (Windows) or `run_app.command` (Mac) in this folder.

2. The script will:
   - Check if Streamlit and other requirements are installed. If not, it will install them automatically.
   - Launch the app in your default web browser.
   - Wait for you to type `exit` and press Enter in the terminal window to fully close the app and server.

3. **If you do not have Python or pip installed**, please install them first:
   - Download Python from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation.

4. Once requirements are installed, the app will open in your browser.

## Usage

1. Launch the application as described above.
2. Upload two CSV files using the file uploaders.
3. Select the comparison type:
   - All columns: Automatically compares all columns if they match exactly.
   - Single column: Compare one column from each dataset.
   - Custom columns: Select and map multiple columns between datasets.
4. Click "Compare Datasets" to see the results.
5. If differences are found, you can:
   - View a preview of mismatched rows.
   - Download the mismatched rows as a CSV file.

## Platform Notes

- **Windows:** No special considerations.
- **Mac:** After first run, you may need to run:
  ```bash
  xattr -d com.apple.quarantine run_app.command
  ``` 
- **Linux:** No special considerations.

## Requirements

- Python 3.8 or higher
- See requirements.txt for package dependencies