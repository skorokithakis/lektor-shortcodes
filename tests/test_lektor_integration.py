"""Integration tests for lektor-shortcodes plugin with Lektor."""

from pathlib import Path

import pytest
from lektor.builder import Builder
from lektor.environment import Environment
from lektor.project import Project


@pytest.fixture(scope="module")
def demo_site_path() -> Path:
    """Return the path to the demo site fixture."""
    return Path(__file__).parent / "fixtures" / "demo-site"


@pytest.fixture(scope="module")
def lektor_project(demo_site_path: Path) -> Project:
    """Create a Lektor project for testing."""
    return Project.from_path(str(demo_site_path))


@pytest.fixture(scope="module")
def lektor_env(lektor_project: Project) -> Environment:
    """Create a Lektor environment with the shortcodes plugin loaded."""
    env = Environment(lektor_project)
    # The plugin is automatically discovered and loaded via entry points
    return env


def test_plugin_loads(lektor_env: Environment) -> None:
    """Test that the shortcodes plugin loads successfully."""
    assert lektor_env.plugin_controller is not None
    # Verify the environment was created successfully
    assert lektor_env.jinja_env is not None


@pytest.mark.integration
def test_build_with_shortcodes(lektor_env: Environment, tmp_path: Path) -> None:
    """Test building a Lektor site with shortcodes.

    This test verifies that:
    1. The plugin loads successfully
    2. A Lektor site can be built
    3. The output HTML is generated

    Note: The shortcode processing functionality itself is tested in test_shortcodes.py
    via the Parser class. This integration test ensures the plugin works within
    the Lektor environment.
    """
    output_path = tmp_path / "output"
    output_path.mkdir()

    pad = lektor_env.new_pad()
    builder = Builder(pad, str(output_path))

    # Build the root page
    root = pad.root
    builder.build(root)

    # Check that the output HTML file was created
    index_html = output_path / "index.html"
    assert index_html.exists()

    # Verify basic content is present
    html_content = index_html.read_text()
    assert "Test Page" in html_content
    assert "Hello from shortcode!" in html_content
