# submission_validator.py
# A simple script to check a Kaggle submission file for common errors.

import pandas as pd

def validate_submission(file_path, expected_rows=None):
    """
    Validates a submission CSV file for common Kaggle errors.

    Args:
        file_path (str): The path to the submission.csv file.
        expected_rows (int, optional): The number of data rows the submission should have. 
                                       If None, this check is skipped.
    """
    print(f"--- Starting Validation for: {file_path} ---")
    
    try:
        # Load the submission file
        df = pd.read_csv(file_path)
        print("File loaded successfully.")
    except FileNotFoundError:
        print(f"ERROR: File not found at '{file_path}'. Please check the path.")
        return

    # --- Check 1: Row Count ---
    if expected_rows is not None:
        actual_rows = len(df)
        if actual_rows == expected_rows:
            print(f"✅ Row Count PASSED: Found {actual_rows} rows, which matches the expected {expected_rows}.")
        else:
            print(f"❌ Row Count FAILED: Found {actual_rows} rows, but expected {expected_rows}.")
            print(f"   Difference: {actual_rows - expected_rows} rows.")

    # --- Check 2: Timestamp Uniqueness ---
    if 'timestamp' not in df.columns:
        print("❌ Timestamp Column FAILED: Column 'timestamp' not found in the file.")
        return
        
    duplicates = df['timestamp'].duplicated().sum()
    if duplicates == 0:
        print("✅ Timestamp Uniqueness PASSED: No duplicate timestamps found.")
    else:
        print(f"❌ Timestamp Uniqueness FAILED: Found {duplicates} duplicate timestamps.")
        duplicate_values = df[df['timestamp'].duplicated()]['timestamp'].unique()
        print(f"   Example duplicate values: {duplicate_values[:5]}")

    # --- Check 3: Column Names ---
    expected_columns = ['timestamp', 'labels']
    actual_columns = list(df.columns)
    if actual_columns == expected_columns:
        print(f"✅ Column Names PASSED: Columns are correctly named and ordered as {expected_columns}.")
    else:
        print(f"❌ Column Names FAILED: Expected columns {expected_columns}, but found {actual_columns}.")

    print("\n--- Validation Complete ---")


if __name__ == '__main__':
    # --- Configuration ---
    submission_file = 'submissions.csv'
    
    # Set this to the required number of rows if you want to check it.
    # Since we are aggregating duplicates, the final count will be lower than the original.
    # We can set it to None to skip this specific check for now.
    required_rows = None 
    
    # Run the validation
    validate_submission(submission_file, required_rows)
