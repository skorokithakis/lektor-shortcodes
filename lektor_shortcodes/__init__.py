"""Lektor Shortcodes plugin for custom shortcode support."""

import itertools
import re
from typing import Any, Dict, Optional, Union

from jinja2 import Environment, Template
from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin
from markupsafe import Markup
from mistune import BlockLexer

from . import scodes


class ShortcodeLexer(BlockLexer):
    """Custom lexer for processing shortcodes in markdown."""

    def __init__(self, config: Any, *, env: Optional[Environment] = None) -> None:
        super().__init__()
        if env is None:
            env = Environment
        self._init_shortcodes_compiler(config, env)
        self._init_shortcodes_lexer()

    def _init_shortcodes_lexer(self) -> None:
        """Initialize the shortcode lexer rules."""
        self.rules.shortcode = re.compile(r"(\[% .+? %\])")
        self.default_rules.insert(1, "shortcode")

    def _init_shortcodes_compiler(self, config: Any, env: Environment) -> None:
        """Initialize the shortcode compiler."""
        self.compile = shortcode_factory(config, env=env)

    def parse_shortcode(self, match: re.Match[str]) -> None:
        """Parse a shortcode match and add it to tokens."""
        text = match.group(1)
        self.tokens.append(
            {
                "type": "close_html",
                "text": self.compile(text, context=self._current_context),
            }
        )


def shortcode_factory(
    config: Any,
    *,
    ctx: Optional[Dict[str, Any]] = None,
    env: Optional[Environment] = None,
) -> Any:
    """
    Return a new shortcode factory.

    Args:
        config: The configuration from the config ini file
        ctx: The original context (containing `this`, `site`, etc)
        env: Jinja2 environment for template rendering

    Returns:
        A shortcode processing function
    """
    if ctx is None:
        ctx = {}

    def shortcodes(
        text: Union[str, Markdown, Markup],
        *,
        context: Optional[Dict[str, Any]] = None,
        **options: Any,
    ) -> Union[str, Markdown, Markup]:
        """Process shortcodes in the given text."""
        if context is not None:
            ctx.update(context)
        if env is None:
            template = Template
        else:
            template = env.from_string
        sections = ("global", options.get("section", "main"))
        shortcodes_config = itertools.chain(
            *(config.section_as_dict(section).items() for section in sections)
        )

        parser = scodes.Parser()
        for item, conf in shortcodes_config:
            # Make a closure so the correct config object passes through.
            def handler_closure(cconf: str) -> Any:
                def handler(
                    context: Any, content: Any, pargs: Any, kwargs: Dict[str, Any]
                ) -> str:
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
    """Lektor plugin for shortcode support."""

    name = "lektor-shortcodes"
    description = "Shortcodes for Lektor."

    def on_process_template_context(
        self, context: Dict[str, Any], **extra: Any
    ) -> None:
        """Add shortcodes filter to Jinja2 environment."""
        if "shortcodes" not in self.env.jinja_env.filters:
            self.env.jinja_env.filters["shortcodes"] = shortcode_factory(
                self.get_config(), ctx=context, env=self.env.jinja_env
            )

    def on_markdown_config(self, config: Any, **extra: Any) -> None:
        """Configure markdown processing with shortcode lexer."""
        shortcodes_config = self.get_config()
        self.lexer = ShortcodeLexer(shortcodes_config, env=self.env.jinja_env)
        config.options["block"] = self.lexer

    def on_markdown_meta_init(self, meta: Any, **extra: Any) -> None:
        """Initialize markdown metadata with context."""
        context = {"this": extra["record"]}
        if extra["record"]:
            context["site"] = extra["record"].pad
        self.lexer._current_context = context
