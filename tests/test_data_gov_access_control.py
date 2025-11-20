import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.data_gov_access_control import DataGovAccessControl


class TestDataGovAccessControl:
    
    def test_determine_response(self):
        """Test access control decision logic."""
        with patch('scripts.data_gov_access_control.SqlDb'):
            dgac = DataGovAccessControl()
            
            # Test granted (equal levels)
            row = pd.Series({'requested_level': 'restricted', 'allowed_level': 'restricted'})
            assert dgac.determine_response(row) == "granted"
            
            # Test granted (lower request)
            row = pd.Series({'requested_level': 'confidential', 'allowed_level': 'sensitive'})
            assert dgac.determine_response(row) == "granted"
            
            # Test denied (higher request)
            row = pd.Series({'requested_level': 'sensitive', 'allowed_level': 'confidential'})
            assert dgac.determine_response(row) == "denied"
