import logging
import pandas as pd
import data_cleaning
from pathlib import Path

class DataLineageLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)



    def log_lineage(self,df_before, df_after, step_name):
        """
        Log the lineage of a DataFrame transformation.

        df_before DataFrame: The DataFrame before the transformation.
        df_after DataFrame: The DataFrame after the transformation.
        step_name str: The name of the transformation step.

        Returns DataFrame: The DataFrame after the transformation.
        """
        rows_before, cols_before = df_before.shape
        rows_after, cols_after = df_after.shape

        columns_before = df_before.columns
        columns_after = df_after.columns

        added_cols = sorted(set(columns_after) - set(columns_before))
        removed_cols = sorted(set(columns_before) - set(columns_after))

        message = (f"Step '{step_name}': rows {rows_before} -> {rows_after}, "
        f"cols {cols_before} -> {cols_after}, added_cols={added_cols}, removed_cols={removed_cols}")

        self.logger.info(message)
        # Write log text to csv
        path_data_dir = Path(__file__).parent.parent / "data"
        path_script_output = path_data_dir / "script_output"
        with open(path_script_output / "lineage_log.log", "a") as f:
            f.write(message + "\n")
        return df_after


if __name__ == "__main__":
    data_lineage_logger = DataLineageLogger()
    data_cleaning = data_cleaning.DataCleaning()
    df_original = data_cleaning.sql_db.sql_table_to_df("employee_data")
    df_cleaned = data_cleaning.clean_user_emails()
    data_lineage_logger.log_lineage(df_original, df_cleaned, "clean_user_emails") 
