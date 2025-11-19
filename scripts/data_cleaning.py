from pathlib import Path
import pandas as pd
from sql_db import SqlDb

class DataCleaning:
    def __init__(self):
        self.path_data_dir = Path(__file__).parent.parent / "data"
        self.path_db = self.path_data_dir / "employee_data.db"
        self.sql_db = SqlDb()
        self.allowed_domains = ["edftrading.com", "jera.com"] # Add allowed domains here
    
    def validate_email_domain(self, email):
        return email.endswith(tuple(self.allowed_domains))
    
    def clean_user_emails(self):
        """
        Clean user emails
        - Convert None to a blank string
        - Trim whitespace from email strings
        - Convert all characters to lowercase
        - Replace internal spaces with dots
        - Validate the email domain against an allowed list (e.g., ['edftrading.com', 'jera.com'])
        Return a DataFrame containing the columns cleaned_email and is_valid_domain.
        """
        df = self.sql_db.sql_table_to_df("employee_data")
        # Convert None to a blank string
        df["email"] = df["email"].fillna("")
        df["cleaned_email"] = df["email"].str.strip()
        df["cleaned_email"] = df["cleaned_email"].str.lower()
        df["cleaned_email"] = df["cleaned_email"].str.replace(" ", ".")
        df["is_valid_domain"] = df["cleaned_email"].apply(self.validate_email_domain)
        # Write df to csv
        df.to_csv(self.path_data_dir / "script_output" / "cleaned_user_emails.csv", index=False)
        return df

if __name__ == "__main__":
    data_quality_eval = DataCleaning()
    data_quality_eval.clean_user_emails()
    pass