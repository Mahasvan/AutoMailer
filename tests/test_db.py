import pytest
from smartmailer.session_management.db import Database


@pytest.fixture
def db_instance():
    db = Database(":memory:")
    yield db
    db.close()


def test_insert_and_check_recipient(db_instance):
    recipient_hash = "abc123"
    assert not db_instance.check_recipient_sent(recipient_hash)

    db_instance.insert_recipient(recipient_hash)
    assert db_instance.check_recipient_sent(recipient_hash)


def test_get_sent_recipients(db_instance):
    hashes = ["hash1", "hash2", "hash3"]
    for h in hashes:
        db_instance.insert_recipient(h)

    results = db_instance.get_sent_recipients()
    returned_hashes = [entry["recipient_hash"] for entry in results]

    assert set(returned_hashes) == set(hashes)
    for entry in results:
        assert "recipient_hash" in entry
        assert "sent_time" in entry


def test_delete_recipient(db_instance):
    recipient_hash = "to_delete"
    db_instance.insert_recipient(recipient_hash)

    assert db_instance.check_recipient_sent(recipient_hash)
    db_instance.delete_recipient(recipient_hash)
    assert not db_instance.check_recipient_sent(recipient_hash)


def test_delete_nonexistent_recipient_raises(db_instance):
    with pytest.raises(ValueError, match="Recipient with hash .* not found"):
        db_instance.delete_recipient("does_not_exist")


def test_clear_database(db_instance):
    db_instance.insert_recipient("clear1")
    db_instance.insert_recipient("clear2")

    assert len(db_instance.get_sent_recipients()) == 2
    db_instance.clear_database()
    assert db_instance.get_sent_recipients() == []


def test_singleton_behavior():
    db1 = Database(":memory:")
    db2 = Database("should_be_ignored.db")
    assert db1 is db2

    db1.insert_recipient("singleton_test")
    assert db2.check_recipient_sent("singleton_test")

    db1.close()