from pathlib import Path
import pandas as pd
from scripts.sql_db import SqlDb

class DataGovAccessControl:
    def __init__(self):
        self.path_data_dir = Path(__file__).parent.parent / "data"
        self.path_db = self.path_data_dir / "employee_data.db"
        self.sql_db = SqlDb()
        self.level_order = {"confidential": 1, "restricted": 2, "sensitive": 3}
    
    def determine_response_to_access_request(self):
        """
        Determine the response to an access request based on the user's department and the dataset's access policy
        """
        df_data_access_policies = self.sql_db.sql_table_to_df("data_access_policies")
        df_access_requests = self.sql_db.sql_table_to_df("access_requests")
        df_employee_data = self.sql_db.sql_table_to_df("employee_data")
        df_merged = pd.merge(df_access_requests, df_employee_data, on="user_id")
        df_merged = pd.merge(df_merged, df_data_access_policies, on="department")
        df_user_access = df_merged[["user_id", "department", "requested_level", "allowed_level"]].copy()
        # If requested_level is less than or equal to allowed_level, grant access
        df_user_access["response"] = df_user_access.apply(self.determine_response, axis=1)
        # Write df_user_access to a csv file
        df_user_access.to_csv(self.path_data_dir / "script_output" / "user_access.csv", index=False)
        return df_user_access

    def determine_response(self, row):
        """
        Determine the response to an access request based on the user's department and the dataset's access policy
        The descending order of levels is confidential, restricted, sensitive.
        """
        access_request_number = self.level_order[row["requested_level"]]
        access_allowed_number = self.level_order[row["allowed_level"]]
        if access_request_number <= access_allowed_number:
            return "granted"
        else:
            return "denied"
        



if __name__ == "__main__":
    data_gov_access_control = DataGovAccessControl()
    data_gov_access_control.determine_response_to_access_request()
    pass