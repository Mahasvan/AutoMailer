import os
import re
import importlib
import logging
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


@pytest.fixture(autouse=True)
def clean_logger_state():
    import automailer.utils.logger as logger_module

    logger = logger_module.logger

    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

    logging.shutdown()

    # Unload logger module to force re-evaluation on next import
    module_name = "automailer.utils.logger"
    if module_name in importlib.sys.modules:
        del importlib.sys.modules[module_name]

    yield

    # Clean up generated log files
    log_dir = Path("logs")
    if log_dir.exists():
        for f in log_dir.glob("log_*.log"):
            try:
                f.unlink()
            except PermissionError:
                print(f"Could not delete {f}, still in use.")
        if not any(log_dir.iterdir()):
            log_dir.rmdir()


def test_log_directory_created():
    with patch("automailer.utils.logger.os.path.exists", return_value=False), \
         patch("automailer.utils.logger.os.makedirs") as mock_makedirs:
        import automailer.utils.logger
        importlib.reload(automailer.utils.logger)
        mock_makedirs.assert_called_once_with("logs")


def test_logger_handlers_and_formatting():
    import automailer.utils.logger
    importlib.reload(automailer.utils.logger)
    logger = automailer.utils.logger.logger

    assert logger.name == "AutoMailerLogger"
    assert logger.level == logging.DEBUG

    handler_types = [type(h) for h in logger.handlers]
    assert logging.FileHandler in handler_types
    assert logging.StreamHandler in handler_types

    for h in logger.handlers:
        assert isinstance(h.formatter, logging.Formatter)


def test_log_file_is_written():
    import automailer.utils.logger
    importlib.reload(automailer.utils.logger)
    logger = automailer.utils.logger.logger

    logger.debug("debug test")
    logger.info("info test")

    file_handler = next(h for h in logger.handlers if isinstance(h, logging.FileHandler))
    file_handler.flush()

    with open(file_handler.baseFilename, "r") as f:
        contents = f.read()

    assert "debug test" in contents
    assert "info test" in contents
    assert re.search(r"\[.*\] \[DEBUG\] debug test", contents)


def test_log_filename_format():
    import automailer.utils.logger
    importlib.reload(automailer.utils.logger)
    file_handler = next(h for h in automailer.utils.logger.logger.handlers if isinstance(h, logging.FileHandler))
    filename = os.path.basename(file_handler.baseFilename)

    assert re.match(r"log_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.log", filename)