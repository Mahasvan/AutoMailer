import os
import logging
import importlib
from unittest.mock import patch, MagicMock


@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
@patch("logging.FileHandler")
@patch("logging.StreamHandler")
def test_logger_configuration(mock_stream_handler, mock_file_handler, mock_exists, mock_makedirs):
    # Reload the logger module to re-trigger setup
    import automailer.utils.logger
    importlib.reload(automailer.utils.logger)

    logger = automailer.utils.logger.logger

    # Basic logger properties
    assert logger.name == "AutoMailerLogger"
    assert logger.level == logging.DEBUG

    # Check if both handlers were created
    mock_file_handler.assert_called_once()
    mock_stream_handler.assert_called_once()
    assert len(logger.handlers) == 2

    # Check formatter set on both handlers
    for h in logger.handlers:
        assert h.setFormatter.call_count == 1

    # Folder creation check
    mock_makedirs.assert_called_once_with("logs")


@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
def test_log_dir_created(mock_exists, mock_makedirs):
    # Reload the logger module to re-trigger setup
    import automailer.utils.logger
    importlib.reload(automailer.utils.logger)

    mock_makedirs.assert_called_once_with("logs")
