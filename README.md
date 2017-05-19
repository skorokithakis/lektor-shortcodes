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

To install the plugin, just add `lektor-shortcodes` to your plugins from the
command line:

~~~
lektor plugins add lektor-shortcodes
~~~


Usage
-----

Using the plugin is simple. Just create a config file called `shortcodes.ini` in
your `configs` directory and specify some shortcode templates. The templates are
full Jinja templates, although (due to some limitations of ini files) they need
to be on one line.

For instance, for the example above, the config file could be:

~~~ini
[main]
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

To actually make the above work, you need to use the `shortcode` filter in your
template. For example, if the field is called `body`, in your html template
that you reference the `body` field you'd add:

~~~
{{ body|shortcodes }}
~~~

This will use the default section, `main`. If you want, you can specify the
section too:

~~~
{{ body|shortcodes(section="post-codes") }}
~~~

And this would look for a section called `post-codes` in the ini file.


Miscellanea
-----------

If you find a bug or have a feature request, please open an issue or file a PR.
Thanks!
