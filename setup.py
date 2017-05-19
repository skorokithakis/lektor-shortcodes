from setuptools import setup

setup(
    name='lektor-shortcodes',
    version='0.1.1',
    author=u'Stavros Korokithakis,,,',
    author_email='hi@stavros.io',
    url='https://github.com/skorokithakis/lektor-shortcodes',
    license='MIT',
    py_modules=['lektor_shortcodes'],
    install_requires=[
    ],
    entry_points={
        'lektor.plugins': [
            'shortcodes = lektor_shortcodes:ShortcodesPlugin',
        ]
    }
)
