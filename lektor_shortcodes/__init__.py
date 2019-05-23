# -*- coding: utf-8 -*-
import itertools
import re

from jinja2 import Template, Environment
from markupsafe import Markup
from mistune import BlockLexer

from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin

from . import scodes


class ShortcodeLexer(BlockLexer):
    def __init__(self, config, *, env=None):
        BlockLexer.__init__(self)
        if env is None:
            env = Environment
        self._init_shortcodes_compiler(config, env)
        self._init_shortcodes_lexer()

    def _init_shortcodes_lexer(self):
        self.rules.shortcode = re.compile(r"(\[% .+? %\])")
        self.default_rules.insert(1, "shortcode")

    def _init_shortcodes_compiler(self, config, env):
        self.compile = shortcode_factory(config, env=env)

    def parse_shortcode(self, match):
        text = match.group(1)
        self.tokens.append({"type": "close_html", "text": self.compile(text, context=self._current_context)})


def shortcode_factory(config, *, ctx=None, env=None):
    """
    Return a new shortcode factory.

    ctx is the original context (containing `this`, `site`, etc), and `config`
    is the configuration from the config ini file.
    """

    if ctx is None:
        ctx = {}

    def shortcodes(text, *, context=None, **options):
        if context is not None:
            ctx.update(context)
        if env is None:
            template = Template
        else:
            template = env.from_string
        sections = ("global", options.get("section", "main"))
        shortcodes = itertools.chain(*(config.section_as_dict(section).items() for section in sections))

        parser = scodes.Parser()
        for item, conf in shortcodes:
            # Make a closure so the correct config object passes through.
            def handler_closure(cconf):
                def handler(context, content, pargs, kwargs):
                    kwargs.update(ctx)
                    return template(cconf).render(kwargs)

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
    name = u"lektor-shortcodes"
    description = u"Shortcodes for Lektor."

    def on_process_template_context(self, context, **extra):
        if "shortcodes" not in self.env.jinja_env.filters:
            self.env.jinja_env.filters["shortcodes"] = shortcode_factory(
                self.get_config(), ctx=context, env=self.env.jinja_env
            )

    def on_markdown_config(self, config, **extra):
        shortcodes_config = self.get_config()
        if not shortcodes_config.section_as_dict("global"):
            return
        self.lexer = ShortcodeLexer(shortcodes_config, env=self.env.jinja_env)
        config.options["block"] = self.lexer

    def on_markdown_meta_init(self, meta, **extra):
        self.lexer._current_context = {"this": extra["record"], "site": extra["record"].pad}
