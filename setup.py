"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()

setuptools.setup(
    name="pytraccar",
    version="master",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="",
    long_description=LONG,
    install_requires=["aiohttp"],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pytraccar",
    packages=setuptools.find_packages(include=["pytraccar.*", "pytraccar"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["traccar=pytraccar.cli:cli"]},
)
