import pandas as pd

def load_and_process_csv(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv("user_data.csv")

    # Print the columns to see what is actually present
    print("Columns in the DataFrame:", df.columns.tolist())

    # Strip whitespace from column names and convert to lowercase for comparison
    df.columns = df.columns.str.strip().str.lower()

    # Define the expected column names, also stripped and lowercased
    expected_columns = ['creditscore', 'creditlines', 'subscriptionprice']

    # Check if the expected columns are present in the DataFrame
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print("Missing columns:", missing_columns)
    else:
        # Proceed with processing
        df = df[expected_columns]
        print("DataFrame with selected columns:")
        print(df.head())

if __name__ == "__main__":
    csv_file_path = "users.csv"
    load_and_process_csv(csv_file_path)
