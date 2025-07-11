import pytest
import os
from unittest.mock import patch
from automailer.session_management.session_manager import SessionManager
from automailer.core.template import TemplateModel
from automailer.config import DB_FOLDER


class DummyTemplate(TemplateModel):
    email: str

@pytest.fixture
def mock_os_safe_name():
    with patch("automailer.session_management.session_manager.get_os_safe_name", return_value="safe_name"):
        yield

@pytest.fixture
def mock_db():
    with patch("automailer.session_management.session_manager.Database") as mock:
        yield mock

@pytest.fixture
def session(mock_os_safe_name, mock_db):
    return SessionManager("My Test Session")

def test_initialization_creates_db_path(session, mock_db):
    expected_path = os.path.join(os.getcwd(), DB_FOLDER, "safe_name.db")
    assert session.dbfile_path == expected_path
    mock_db.assert_called_once_with(expected_path)

def test_add_recipient_only_once(session):
    recipient = DummyTemplate(email="user@example.com")
    session.db.check_recipient_sent.return_value = False

    session.add_recipient(recipient)
    session.db.insert_recipient.assert_called_once_with(recipient.hash_string)

def test_add_recipient_skips_if_already_sent(session):
    recipient = DummyTemplate(email="user@example.com")
    session.db.check_recipient_sent.return_value = True

    session.add_recipient(recipient)
    session.db.insert_recipient.assert_not_called()

def test_get_current_session_id(session):
    assert session.get_current_session_id() == "safe_name"

def test_get_sent_recipients_calls_db(session):
    session.get_sent_recipients()
    session.db.get_sent_recipients.assert_called_once()

def test_filter_unsent_recipients(session):
    r1 = DummyTemplate(email="a@a.com")
    r2 = DummyTemplate(email="b@b.com")

    session.db.check_recipient_sent.side_effect = [False, True]

    result = session._filter_unsent_recipients([r1, r2])
    assert result == [r1]

def test_filter_sent_recipients(session):
    r1 = DummyTemplate(email="x@x.com")
    r2 = DummyTemplate(email="y@y.com")
    
    sent_hashes = [r2.hash_string]
    session.db.get_sent_recipients.return_value = [{'recipient_hash': r2.hash_string}]
    
    result = session.filter_sent_recipients([r1, r2])
    assert result == [r2]