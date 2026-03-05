"""Configuration file for the Sphinx documentation builder."""

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Project Name"
copyright = "2025, Alessandro Palmas"  # noqa: A001
author = "Alessandro Palmas"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # parses Google/NumPy style docstrings
    "sphinx_autodoc_typehints",  # shows type hints
    "myst_parser",  # for markdown files
]


# Optional MyST extensions
myst_enable_extensions = [
    "colon_fence",  # allows ::: for directives
    "deflist",  # definition lists
]

templates_path = ["_templates"]
# exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "Project Name"
html_static_path = ["_static"]

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#FD3030",
        "color-brand-content": "#FD3030",
    },
    "dark_css_variables": {
        "color-brand-primary": "#FD3030",
        "color-brand-content": "#FD3030",
    },
}

html_favicon = "_static/favicon.ico"
