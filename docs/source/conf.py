"""Sphinx docs config."""

import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import json_log_display

project = "JSON log display"
copyright = "2022, " + json_log_display.pkg_meta.author
author = json_log_display.pkg_meta.author
release = json_log_display.pkg_meta.version
version = json_log_display.pkg_meta.version

extensions = [
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_css_files = ["custom.css"]
