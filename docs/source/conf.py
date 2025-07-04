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

sys.path.insert(0, os.path.abspath("../../src"))
sys.path.insert(0, os.path.abspath("../../"))

on_rtd = os.environ.get("READTHEDOCS") == "True"

if on_rtd:
    from api import app

    app.config["CELERY"]["task_always_eager"] = True


# -- Project information -----------------------------------------------------

project = "SatChecker"
copyright = "2024, IAU Centre for the Protection of Dark and Quiet Sky from \
    Satellite Constellation Interference"
author = "IAU CPS"

# The full version, including alpha/beta/rc tags
release = "1.4.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinxcontrib.httpdomain",
    "sphinx_code_tabs",
    "nbsphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "celery.contrib.sphinx",
    "myst_parser",
]

nbsphinx_allow_errors = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "custom.css",
]

autodoc_default_options = {
    "members": True,
    "private-members": True,
}

autodoc_typehints = "signature"
autodoc_class_signature = "separated"
