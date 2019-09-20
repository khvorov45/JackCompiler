# pylint: disable=missing-docstring
import setuptools

NAME = "jackcompiler"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name=NAME,
    version="0.1.0",
    author="Arseniy Khvorov",
    author_email="khvorov45@gmail.com",
    description="Compiles ",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/khvorov45/jackcompiler",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "colorama",
        "cmdparserkhv"
    ],
    dependency_links=["https://github.com/khvorov45/cmdparserkhv"],
    entry_points={
        "console_scripts": ["jackcompiler=jackcompiler.command_line:main"]
    }
)
