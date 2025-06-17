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

## Installation

### Option 1: Run from Source

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run dataset_comparison_app.py
   ```

### Option 2: Run as Executable

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create executable:
   ```bash
   pyinstaller --onefile --add-data "streamlit:streamlit" dataset_comparison_app.py
   ```
4. Run the executable from the `dist` directory

## Usage

1. Launch the application
2. Upload two CSV files using the file uploaders
3. Select the comparison type:
   - All columns: Automatically compares all columns if they match exactly
   - Single column: Compare one column from each dataset
   - Custom columns: Select and map multiple columns between datasets
4. Click "Compare Datasets" to see the results
5. If differences are found, you can:
   - View a preview of mismatched rows
   - Download the mismatched rows as a CSV file

## Platform Notes

- Windows: No special considerations
- Mac: After first run, you may need to run:
  ```bash
  xattr -d com.apple.quarantine dataset_comparison_app
  ```
- Linux: No special considerations

## Requirements

- Python 3.8 or higher
- See requirements.txt for package dependencies 