from pathlib import Path
import pandas as pd
from sql_db import SqlDb

class DataQualityEval:
    def __init__(self):
        self.path_data_dir = Path(__file__).parent.parent / "data"
        self.path_db = self.path_data_dir / "employee_data.db"
        self.sql_db = SqlDb()

    def evaluate_email_data_quality(self, row):
        """
        Check if each email has a duplicate, if so mark issue_type as "potential_duplicate"
        otherwise mark issue_type as "unique"
        Also check if the email has:
        Leading or trailing spaces,
        Spaces in the email
        No @ symbol
        No . symbol
        if so mark issue_type as "malformed email address" and an appropriate reason
        """
 
        series_data_quality = pd.Series()
        series_data_quality["user_id"] = row["user_id"]
        series_data_quality["email"] = row["email"]
        series_data_quality["issue_type"] = ""
        series_data_quality["reason"] = ""
        if row["potential_duplicate"] == True:
            series_data_quality["issue_type"] = "potential_duplicate"
            series_data_quality["reason"] += f"Email {row['email']} was found more than once "
        if row["email"] is None:
            series_data_quality["issue_type"] = "malformed_email_address"
            series_data_quality["reason"] += "Email is empty "
        else:
            if len(row["email"]) != len(row["email"].strip()):
                series_data_quality["issue_type"] = "malformed_email_address"
                series_data_quality["reason"] += "Leading or trailing spaces "
            
            if " " in row["email"].strip():
                series_data_quality["issue_type"] = "malformed_email_address"
                series_data_quality["reason"] += "Spaces in the email "
        
            if "@" not in row["email"]:
                series_data_quality["issue_type"] = "malformed_email_address"
                series_data_quality["reason"] += "No @ symbol "
            
            if "." not in row["email"]:
                series_data_quality["issue_type"] = "malformed_email_address"
                series_data_quality["reason"] += "No . symbol "
        
        return series_data_quality
        

    def create_data_quality_report(self):
        """
        Create a csv file with the data quality report
        """
        df_employee_data = self.sql_db.sql_table_to_df("employee_data")
        # Add a new series potential_duplicate with boolean values if more than one occurrence of the email
        df_employee_data["potential_duplicate"] = df_employee_data.duplicated(subset="email", keep=False)
        

        df_data_quality = df_employee_data.apply(
            self.evaluate_email_data_quality,
            axis=1,
        )
        df_data_quality.to_csv(self.path_data_dir / "script_output" / "data_quality_report.csv", index=False)

                

if __name__ == "__main__":
    data_quality_eval = DataQualityEval()
    data_quality_eval.create_data_quality_report()
    pass
    