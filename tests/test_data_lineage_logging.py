import pytest
import pandas as pd
import logging

from scripts.data_lineage_logging import DataLineageLogger


class TestDataLineageLogger:
    
    def test_log_lineage_tracks_changes(self, caplog):
        """Test that log_lineage tracks DataFrame changes."""
        logger = DataLineageLogger()
        df_before = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
        df_after = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob'], 'email': ['a@x.com', 'b@x.com']})
        
        with caplog.at_level(logging.INFO):
            result = logger.log_lineage(df_before, df_after, "add_email")
        
        assert "Step 'add_email'" in caplog.text
        assert "rows 2 -> 2" in caplog.text
        assert "cols 2 -> 3" in caplog.text
        pd.testing.assert_frame_equal(result, df_after)
