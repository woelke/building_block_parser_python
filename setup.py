import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bb_parser-woelke",
    version="0.0.1",
    author="Sebastian Woelke",
    author_email="Sebastian.Woelke@posteo.de",
    description=" A declarative general purpose parser for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woelke/building_block_parser_python",
    project_urls={
        "Bug Tracker": "https://github.com/woelke/building_block_parser_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
