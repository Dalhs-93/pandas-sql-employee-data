import pytest
import pandas as pd
import sqlite3
from pathlib import Path

from scripts.sql_db import SqlDb


class TestSqlDb:
    
    def test_load_and_read_csv_to_sqlite(self, tmp_path):
        """Test loading CSV to SQLite and reading it back."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create test CSV
        df_test = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
        df_test.to_csv(data_dir / "test.csv", index=False)
        
        # Load to SQLite
        sql_db = SqlDb()
        sql_db.path_data_dir = data_dir
        sql_db.path_db = data_dir / "employee_data.db"
        sql_db.load_csvs_to_sqlite()
        
        # Read back
        df_result = sql_db.sql_table_to_df("test")
        pd.testing.assert_frame_equal(df_result, df_test)
