import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="restack",
    version="0.0.1",
    author="Dave Jeffrey",
    author_email="mail@davidjeffrey.co.uk",
    description="A wrapper for working with Restack, the API for IoT communication",
    license="BSD",
    keywords="restack IoT",
    url="https://github.com/lepoetemaudit/restack",
    packages=['restack'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)