Lektor Shortcodes
=================

[![PyPI](https://img.shields.io/pypi/v/lektor-shortcodes.svg)](https://pypi.python.org/pypi/lektor-shortcodes)

The Lektor Shortcodes plugin allows you to use shortcodes (shortcodes are
something like custom tags) in your fields (not templates), so your content
doesn't have to have repetitive snippets over and over.

For example, my blog has some specific HTML that I add when I want an image with
a border and caption to be displayed.  The HTML looks like this:


~~~html
    <div class="alignright">
        <a href="image-large.jpg">
            <img src="image.jpg" />
            <span class="caption">The caption</span>
        </a>
    </div>
~~~

Copy-pasting this every time gets tedious, and I have to search and replace it
in all the content files every time I want to make a change.  With the
shortcodes plugin, this can be written as:

~~~
[% image align=right link="image-large.jpg" image=image.jpg caption="The caption" %]
~~~

Much easier, cleaner and less repetitive.


Installation
------------

### Using Lektor (Recommended)

To install the plugin, just add `lektor-shortcodes` to your plugins from the
command line:

~~~
lektor plugins add lektor-shortcodes
~~~

### Using pip

You can also install directly with pip:

~~~
pip install lektor-shortcodes
~~~

### Using uv (Development)

For development, you can use uv to manage dependencies:

~~~
uv pip install -e .[dev]
~~~


Usage
-----

Using the plugin is simple. Just create a config file called `shortcodes.ini` in
your `configs` directory and specify some shortcode templates. The templates are
full Jinja templates, although (due to some limitations of ini files) they need
to be on one line.

For instance, for the example above, the config file could be:

~~~ini
[global]
image = '<div class="align{{ align }}">{% if link %}<a href="{{ link }}"{% if not link.startswith("http") %} data-lightbox="gallery"{% endif %}>{% endif %}<img src="{{ image }}">{% if link %}</a>{% endif %}{% if caption %}<span class="caption">{{ caption }}</span>{% endif %}</div>'
~~~

This will allow you to use shortcodes with optional arguments, like so:

~~~
# An image with no caption or link:
[% image align=right image=hello.jpg %]


# An image with a link:
[% image align=right link=http://www.example.com image=hello.jpg %]

# Link and caption:
[% image align=right link=http://www.example.com image=hello.jpg caption="Hello!" %]
~~~

Shortcodes defined within the section named `global` will be processed
automatically inside any of your site’s Markdown content. It is also possible to
define shortcodes which are only expanded when the Jinja2 template for a page
explicitly requests it. Shortcodes defined in any section not named `global`
will only be applied when the template passed the content through a Jinja2
filter named `shortcode`. For example, if your HTML template references a field
called `body`, and your config has a section called `[special]`, you may request
expanding shortcodes defined within the `special` section like so:

~~~
{{ body|shortcodes(section="special") }}
~~~

This will enable all shortcodes from the specified section, in addition to all
globally defined shortcodes. If no section is specified, the filter defaults to
the section named `main` (so it will include shortcodes in `main` unless you
request a different section, and it will always include shortcodes in `global` no
matter what).


Development
-----------

This project uses modern Python tooling:

- **uv** for fast package management
- **hatch** for building and packaging
- **ruff** for linting and formatting
- **mypy** for type checking
- **pytest** for testing

### Setup Development Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e .[dev]

# Run all tests (unit + integration)
pytest

# Run only unit tests
pytest tests/test_shortcodes.py

# Run only integration tests
pytest tests/test_lektor_integration.py -m integration

# Run linting
ruff check .

# Run type checking
mypy lektor_shortcodes

# Format code
ruff format .

# Build package
hatch build
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pre-commit install
pre-commit run --all-files
```

Miscellanea
-----------

If you find a bug or have a feature request, please open an issue or file a PR.
Thanks!
