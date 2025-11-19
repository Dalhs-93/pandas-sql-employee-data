from pathlib import Path
import sqlite3
import pandas as pd

class SqlDb:
    def __init__(self):
        self.path_data_dir = Path(__file__).parent.parent / "data"
        self.path_db = self.path_data_dir / "employee_data.db"


    def load_csvs_to_sqlite(self) -> None:
        """
        Load all employee data CSV files from the data directory into a single SQLite database.

        This function:
        - Looks for all `.csv` files in the data directory next to this script.
        - Uses each CSV file's basename (e.g. [employee_data.csv] as the table name
        - Creates (or opens) an SQLite database at `employee_data.db`
        - Writes each CSV into its corresponding table, replacing the table if it
        already exists.
        """
        # Ensure the data directory exists
        self.path_data_dir.mkdir(parents=True, exist_ok=True)

        # Connect to (or create) the SQLite database
        conn = sqlite3.connect(self.path_db)

        try:
            for csv_path in self.path_data_dir.glob("*.csv"):
                table_name = csv_path.stem  # e.g. "employee_data.csv" -> "employee_data"

                print(f"Loading {csv_path.name} into table '{table_name}' in {self.path_db.name}")

                df = pd.read_csv(csv_path)

                # Overwrite the table if it already exists
                df.to_sql(table_name, conn, if_exists="replace", index=False)

            print(f"All CSV files in {self.path_data_dir} loaded into {self.path_db}")
        finally:
            conn.close()

    def sql_table_to_df(self, table_name: str) -> pd.DataFrame:
        """
        Load a single table from the SQLite database into a pandas DataFrame.

        table_name (str): The name of the table to load.

        returns pd.DataFrame: The table as a pandas DataFrame.
        """
        conn = sqlite3.connect(self.path_db)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df


if __name__ == "__main__":
    # Load all CSV files into the SQLite database
    setup_sql_db = SqlDb()
    setup_sql_db.load_csvs_to_sqlite()
    