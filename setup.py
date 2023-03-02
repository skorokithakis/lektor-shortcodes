from setuptools import setup

setup(
    name="lektor-shortcodes",
    version="0.2.7",
    author=u"Stavros Korokithakis,,,",
    author_email="hi@stavros.io",
    url="https://github.com/skorokithakis/lektor-shortcodes",
    description="The Lektor Shortcodes plugin allows you to use shortcodes (shortcodes are something like custom tags) in your fields (not templates), so your content doesn't have to have repetitive snippets over and over.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["lektor_shortcodes"],
    keywords="lektor shortcodes",
    install_requires=[],
    entry_points={"lektor.plugins": ["shortcodes = lektor_shortcodes:ShortcodesPlugin"]},
)
