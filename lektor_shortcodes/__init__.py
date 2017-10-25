# -*- coding: utf-8 -*-
import re
import itertools

from jinja2 import Template
from lektor.pluginsystem import Plugin
from lektor.markdown import Markdown
from markupsafe import Markup
from mistune import BlockLexer, BlockGrammar

from . import scodes


class ShortcodeLexer(BlockLexer):

    def __init__(self, config):
        BlockLexer.__init__(self)
        self._init_shortcodes_compiler(config)
        self._init_shortcodes_lexer()

    def _init_shortcodes_lexer(self):
        self.rules.shortcode = re.compile(r'(\[% .+? %\])')
        self.default_rules.insert(1, 'shortcode')

    def _init_shortcodes_compiler(self, config):
        self.compile = shortcode_factory(config)

    def parse_shortcode(self, match):
        text = match.group(1)
        self.tokens.append({
            'type': 'close_html',
            'text': self.compile(text)
        })


def shortcode_factory(config):

    def shortcodes(text, **options):
        sections = ("global", options.get("section", "main"))
        shortcodes =  itertools.chain(*(
            config.section_as_dict(section).items()
            for section in sections
        ))

        parser = scodes.Parser()
        for item, conf in shortcodes:
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

    def on_markdown_config(self, config):
        shortcodes_config = self.get_config()
        if not shortcodes_config.section_as_dict('global'):
            return
        lexer = ShortcodeLexer(shortcodes_config)
        config.options['block'] = lexer

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters['shortcodes'] = shortcode_factory(self.get_config())
