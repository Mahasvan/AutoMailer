import re
import pytest
from automailer.utils.strings import sanitize_name, get_hash, get_os_safe_name

def test_sanitize_name_invalid():
    assert sanitize_name("Invalid File@Name!.txt") == "invalid_filenametxt"
    assert sanitize_name(r"test/File\Name") == "testfilename"
    assert sanitize_name(r"test/File\\Name") == "testfilename"
    assert sanitize_name("My file 123") == "my_file_123"

def test_sanitize_name_valid():
    assert sanitize_name("hello-world_123") == "hello-world_123"

def test_get_hash():
    s = "collision"
    hash1 = get_hash(s)
    hash2 = get_hash(s)
    assert hash1 == hash2
    assert re.fullmatch(r"[a-f0-9]{64}", hash1)

def test_get_hash_collision():
    h1 = get_hash("test1")
    h2 = get_hash("test2")
    assert h1 != h2

def test_os_safe_name_format():
    name = "My Automail Log File!"
    os_safe = get_os_safe_name(name)
    base, hash_part = os_safe.rsplit('-', 1)
    assert base == sanitize_name(name)
    assert hash_part == get_hash(name)

def test_os_safe_name():
    with pytest.raises(ValueError):
        get_os_safe_name("")