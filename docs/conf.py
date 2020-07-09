# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import re
import io

_docs_path = os.path.dirname(__file__)
_version_path = os.path.abspath(os.path.join(_docs_path,
    '..', 'astrocabtools', '__init__.py'))

with io.open(_version_path, 'r', encoding='latin1') as fp:
    try:
        _version_info = re.search(r"^__version__ = '"
                r"(?P<major>\d+)"
                r"\.(?P<minor>\d+)" 
                r"\.(?P<patch>\d+)"
                r"(?P<tag>.*)?'$",
                fp.read(), re.M).groupdict()
    except IndexError:
        raise RuntimeError('Unable to determine version.')

# -- Project information -----------------------------------------------------

project = 'AstroCabTools'
copyright = '2020, Alejandro Gorgues'
author = 'Alejandro Gorgues'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.autosectionlabel',
        'sphinx.ext.todo',
        'sphinx.ext.githubpages',

]

try:
    import sphinxcontrib.seplling #noqa
    extension.append('sphinxcontrib.spelling')
except ImportError:
    pass

intersphinx_mapping = {
        'python': ('http://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme= 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

version = '{major}.{minor}'.format(**_version_info)
release = '{major}.{minor}.{patch}{tag}'.format(**_version_info)

highlight_language = 'python3'
source_suffix = '.rst'

master_doc = 'index'

numfig = True

pygments_style = 'sphinx'
