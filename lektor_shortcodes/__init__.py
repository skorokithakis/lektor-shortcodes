# -*- coding: utf-8 -*-
from jinja2 import Template
from lektor.pluginsystem import Plugin
from lektor.markdown import Markdown
from markupsafe import Markup

import scodes


def shortcode_factory(config):
    def shortcodes(text, **options):
        section = options.get("section", "main")

        parser = scodes.Parser()
        for item, conf in config.section_as_dict(section).items():
            # Make a closure so the correct config object passes through.
            def handler_closure(cconf):
                def handler(context, content, pargs, kwargs):
                    return Template(cconf).render(kwargs)
                return handler
            parser.register(handler_closure(conf), item)

        if isinstance(text, Markdown):
            text.source = parser.parse(text.source)
        elif isinstance(text, Markup):
            text = Markup(parser.parse(text))
        else:
            text = parser.parse(text)
        return text
    return shortcodes


class ShortcodesPlugin(Plugin):
    name = u'lektor-shortcodes'
    description = u'Shortcodes for Lektor.'

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters['shortcodes'] = shortcode_factory(self.get_config())
