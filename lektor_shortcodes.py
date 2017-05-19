# -*- coding: utf-8 -*-
from jinja2 import Template
from lektor.pluginsystem import Plugin
from lektor.markdown import Markdown
import scodes


def shortcode_factory(config):
    def shortcodes(text, **options):
        section = options.get("section", "main")

        for item, conf in config.section_as_dict(section).items():
            @scodes.register(item)
            def handler(context, content, pargs, kwargs):
                return Template(conf).render(kwargs)

        parser = scodes.Parser()
        if isinstance(text, Markdown):
            text.source = parser.parse(text.source)
        else:
            text = parser.parse(text.source)
        return text
    return shortcodes


class ShortcodesPlugin(Plugin):
    name = u'lektor-shortcodes'
    description = u'Shortcodes for Lektor.'

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters['shortcodes'] = shortcode_factory(self.get_config())
