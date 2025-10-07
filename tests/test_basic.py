"""Basic tests that don't require Lektor imports."""


def test_basic_functionality():
    """Test basic Python functionality."""
    assert 1 + 1 == 2
    assert "hello" == "hello"


def test_import_works():
    """Test that we can import basic modules."""
    import sys
    import os

    assert sys.version_info.major >= 3
    assert os.path.exists(".")
