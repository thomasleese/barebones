from setuptools import setup

config = {
    "name": "barebones",
    "version": "0.0.1",
    "description": "A simple python interpreter for an extended Barebones language.",
    "url": "https://github.com/tomleese/barebones",
    "author": "Tom Leese",
    "author_email": "tom@tomleese.me.uk",
    "scripts": [ "bin/barebones" ],
    "packages": [ "barebones" ],
}

setup(**config)
