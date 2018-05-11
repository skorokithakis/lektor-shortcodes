from setuptools import setup

setup(
    name='lektor-shortcodes',
    version='0.2.0',
    author=u'Stavros Korokithakis,,,',
    author_email='hi@stavros.io',
    url='https://github.com/skorokithakis/lektor-shortcodes',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['lektor_shortcodes'],
    keywords="lektor shortcodes",
    install_requires=[
    ],
    entry_points={
        'lektor.plugins': [
            'shortcodes = lektor_shortcodes:ShortcodesPlugin',
        ]
    }
)
