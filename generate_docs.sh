#!/bin/bash

## Instal deps
python setup.py develop
python -m pip install pdoc --user

# Generate docs 
pdoc pytraccar --html --html-dir tempdocs  --overwrite

# Out with the old.

rm -R docs

# Inn with the new
mkdir docs
cp tempdocs/pytraccar/* docs/

# Fix headers
sed -i "s,<h1>Index</h1>,<h1><a href=\"index.html\">Index</a></h1>,g" docs/api.m.html
sed -i "s,<h1>Index</h1>,<h1><a href=\"index.html\">Index</a></h1>,g" docs/cli.m.html
sed -i "s,<h1>Index</h1>,<h1><a href=\"index.html\">Index</a></h1>,g" docs/const.m.html
sed -i "s,<h1>Index</h1>,<h1><a href=\"index.html\">Index</a></h1>,g" docs/index.html

# Cleanup
rm -R tempdocs