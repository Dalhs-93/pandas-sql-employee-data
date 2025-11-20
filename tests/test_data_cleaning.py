import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.data_cleaning import DataCleaning



class TestDataCleaning:
    
    def test_validate_email_domain(self):
        """Test email domain validation."""
        # patch allows us to mock the SqlDb class
        with patch('scripts.data_cleaning.SqlDb'):
            dc = DataCleaning()
            assert dc.validate_email_domain("user@edftrading.com") is True
            assert dc.validate_email_domain("user@jera.com") is True
            assert dc.validate_email_domain("user@invalid.com") is False
    
    def test_clean_user_emails(self, tmp_path):
        """Test email cleaning pipeline."""
        with patch('scripts.data_cleaning.SqlDb') as mock_sql:
            dc = DataCleaning()
            dc.path_data_dir = tmp_path / "data"
            dc.path_data_dir.mkdir()
            (dc.path_data_dir / "script_output").mkdir()
            
            test_data = pd.DataFrame({
                'user_id': [1, 2],
                'name': ['Alice', 'Bob'],
                'email': [' ALICE@EDFTRADING.COM ', 'bob smith@jera.com'],
                'department': ['HR', 'IT']
            })
            dc.sql_db = Mock()
            dc.sql_db.sql_table_to_df.return_value = test_data
            
            result = dc.clean_user_emails()
            
            assert result['cleaned_email'].tolist() == ['alice@edftrading.com', 'bob.smith@jera.com']
            assert result['is_valid_domain'].tolist() == [True, True]
