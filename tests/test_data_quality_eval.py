import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.data_quality_eval import DataQualityEval


class TestDataQualityEval:
    
    def test_evaluate_email_data_quality(self):
        """Test email quality evaluation."""
        with patch('scripts.data_quality_eval.SqlDb'):
            dqe = DataQualityEval()
            
            # Test valid email
            row = pd.Series({'user_id': 1, 'email': 'user@example.com', 'potential_duplicate': False})
            result = dqe.evaluate_email_data_quality(row)
            assert result['issue_type'] == ""
            
            # Test duplicate
            row = pd.Series({'user_id': 2, 'email': 'dup@example.com', 'potential_duplicate': True})
            result = dqe.evaluate_email_data_quality(row)
            assert result['issue_type'] == "potential_duplicate"
            
            # Test malformed (no @)
            row = pd.Series({'user_id': 3, 'email': 'badexample.com', 'potential_duplicate': False})
            result = dqe.evaluate_email_data_quality(row)
            assert result['issue_type'] == "malformed_email_address"
            assert "No @ symbol" in result['reason']
