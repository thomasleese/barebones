#!/usr/bin/env python3
from setuptools import setup


setup(
    name="barebones",
    version="1.0.0",
    description="Interpreter for an extended Barebones language written in Python.",
    url="https://github.com/tomleese/barebones",
    author="Tom Leese",
    author_email="inbox@tomleese.me.uk",
    packages=["barebones"],
    entry_points = {
        "console_scripts": ["barebones = barebones:main"]
    }
)
