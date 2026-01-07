"""Tests for the shortcodes functionality."""

# Test the scodes module directly without importing the main package
import os
import sys

# Add the package root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import the scodes module directly
from lektor_shortcodes.scodes import Parser


def test_parser_initialization():
    """Test that parser initializes correctly."""
    parser = Parser()
    assert parser.start == "[%"
    assert parser.ends == []  # ends starts empty
    assert parser.esc_start == "\\[%"  # Check the escape start pattern


def test_register_handler():
    """Test registering a shortcode handler."""
    parser = Parser()

    def test_handler(context, content, pargs, kwargs):
        return f"<div>{content or 'no content'}</div>"

    parser.register(test_handler, "test")
    assert "test" in parser.tags
    assert parser.tags["test"]["func"] == test_handler


def test_parse_simple_shortcode():
    """Test parsing a simple shortcode."""
    parser = Parser()

    def test_handler(context, content, pargs, kwargs):
        return f"<div>Hello {kwargs.get('name', 'World')}</div>"

    parser.register(test_handler, "hello")
    result = parser.parse("[% hello name=Test %]")
    assert "Hello Test" in result


def test_parse_shortcode_with_content():
    """Test parsing a shortcode with content."""
    parser = Parser()

    def test_handler(context, content, pargs, kwargs):
        return f"<div class='{kwargs.get('class', 'default')}'>{content}</div>"

    parser.register(test_handler, "div", "enddiv")
    result = parser.parse("[% div class=highlight %]This is content[% enddiv %]")
    assert "class='highlight'" in result
    assert "This is content" in result
