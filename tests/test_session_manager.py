import pytest
import os
from unittest.mock import patch, MagicMock
from smartmailer.session_management.session_manager import SessionManager

class DummyRecipient:
    def __init__(self, h):
        self.hash_string = h

@patch("smartmailer.session_management.session_manager.DBOperator")
@patch("smartmailer.session_management.session_manager.os.path.exists", return_value=False)
@patch("smartmailer.session_management.session_manager.os.makedirs")
def test_folder_creation_triggered(mock_makedirs, mock_exists, mock_db_op):
    sm = SessionManager("new_session_test")
    mock_makedirs.assert_called_once()

@patch("smartmailer.session_management.session_manager.DBOperator")
@patch("smartmailer.session_management.session_manager.os.path.exists", return_value=True)
def test_existing_dbfile_skips_creation(mock_exists, mock_db_op):
    sm = SessionManager("existing_session")

@pytest.fixture
def dummy_recipients():
    return [DummyRecipient(f"hash{i}") for i in range(3)]


@pytest.fixture
def mock_db_op():
    with patch("smartmailer.session_management.session_manager.DBOperator") as mock_op_class:
        mock_op = MagicMock()
        mock_op_class.return_value = mock_op
        yield mock_op


@pytest.fixture
def session_manager(mock_db_op):
    sm = SessionManager("test session")
    return sm


def test_get_current_session_id(session_manager):
    session_id = session_manager.get_current_session_id()
    assert session_id.startswith("test_session")
    assert isinstance(session_id, str)


def test_add_recipient_adds_only_if_not_sent(session_manager, mock_db_op):
    recipient = DummyRecipient("abc123")
    mock_db_op.check_recipient_sent.return_value = False

    session_manager.add_recipient(recipient)

    mock_db_op.add_to_db.assert_called_once_with("abc123")


def test_add_recipient_skips_if_already_sent(session_manager, mock_db_op):
    recipient = DummyRecipient("abc123")
    mock_db_op.check_recipient_sent.return_value = True

    session_manager.add_recipient(recipient)

    mock_db_op.add_to_db.assert_not_called()


def test_get_sent_recipients_delegates_to_db(session_manager, mock_db_op):
    session_manager.get_sent_recipients()
    mock_db_op.get_sent_recipients.assert_called_once()


def test_filter_sent_recipients(session_manager, mock_db_op, dummy_recipients):
    # DB says hash1 and hash2 are sent
    mock_db_op.get_sent_recipients.return_value = [
        {"recipient_hash": "hash1"},
        {"recipient_hash": "hash2"}
    ]

    result = session_manager.filter_sent_recipients(dummy_recipients)
    result_hashes = [r.hash_string for r in result]

    assert set(result_hashes) == {"hash1", "hash2"}


def test__filter_unsent_recipients(session_manager, mock_db_op, dummy_recipients):
    # Simulate that only hash0 and hash2 are unsent
    mock_db_op.check_recipient_sent.side_effect = lambda h: h == "hash1"

    result = session_manager._filter_unsent_recipients(dummy_recipients)
    result_hashes = [r.hash_string for r in result]

    assert set(result_hashes) == {"hash0", "hash2"}