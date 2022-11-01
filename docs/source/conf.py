# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
from pathlib import Path
import os
import sys

from sphinx.application import Sphinx

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

sys.path.insert(0, os.path.abspath("_ext"))
needs_sphinx = "5.0"

# -- Project information -----------------------------------------------------

project = "moscot"
# author = moscot.__author__
# copyright = f"{datetime.now():%Y}, {author}."
release = "main"
# version = f"{release} ({moscot.__version__})"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx_gallery.load_style",
    "nbsphinx",
    "sphinxcontrib.bibtex",
    "sphinx_gallery.load_style",
    "nbsphinx",
    "sphinxcontrib.bibtex",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "jax": ("https://jax.readthedocs.io/en/latest/", None),
    "ott": ("https://ott-jax.readthedocs.io/en/latest/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
    "scanpy": ("https://scanpy.readthedocs.io/en/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
source_suffix = [".rst", ".ipynb"]
master_doc = "index"
pygments_style = "sphinx"

# citation
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"
bibtex_default_style = "alpha"

# spelling
spelling_lang = "en_US"
spelling_warning = True
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_add_pypi_package_names = True
spelling_show_suggestions = True
spelling_exclude_patterns = ["references.rst"]
# see: https://pyenchant.github.io/pyenchant/api/enchant.tokenize.html
spelling_filters = ["enchant.tokenize.URLFilter", "enchant.tokenize.EmailFilter", "enchant.tokenize.MentionFilter"]

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "auto_*/**.ipynb",
    "auto_*/**.md5",
    "auto_*/**.py",
    "**.ipynb_checkpoints",
    "auto_examples/problems/**/index.rst",
    "auto_*/**/index.rst",
]  # ignore anything that isn't .rst or .ipynb

# -- sphinx gallery


def reset_matplotlib(_gallery_conf, _fname):
    import matplotlib as mpl

    mpl.use("agg")

    import matplotlib.pyplot as plt

    plt.rcdefaults()
    mpl.rcParams["savefig.bbox"] = "tight"
    mpl.rcParams["savefig.transparent"] = True
    mpl.rcParams["figure.figsize"] = (12, 8)
    mpl.rcParams["figure.dpi"] = 96
    mpl.rcParams["figure.autolayout"] = True


_root = Path(__file__).parent.parent.parent
sphinx_gallery_conf = {
    "image_scrapers": "matplotlib",
    "reset_modules": (reset_matplotlib,),
    "filename_pattern": f"{os.path.sep}ex",
    "examples_dirs": [_root / "examples"],
    "gallery_dirs": ["auto_examples"],
    "abort_on_example_error": True,
    "show_memory": True,
    "reference_url": {
        "sphinx_gallery": None,
    },
    "line_numbers": False,
    "compress_images": (
        "images",
        "thumbnails",
        "-o3",
    ),
    "remove_config_comments": True,
    "inspect_global_variables": False,
    "backreferences_dir": "gen_modules/backreferences",
    "doc_module": "moscot",
    "download_all_examples": False,
    "show_signature": False,
    "pypandoc": {
        "extra_args": [
            "--mathjax",
        ],
    },
    "default_thumb_file": "_static/img/logo.png",
    "plot_gallery": "'True'",  # https://github.com/sphinx-gallery/sphinx-gallery/issues/913
}
nbsphinx_thumbnails = {
    "auto_examples/problems/**": "_static/img/logo.png",
    "auto_examples/plotting/**": "_static/img/logo.png",
}
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'png', 'pdf'}",  # correct figure resize
    "--InlineBackend.rc={'figure.dpi': 96}",
]

# we ignore this because external tutorials require some heavy libraries (tensorflow/pytorch/pyqt5)
# _nbsphinx_prolog = r"""
# {% set docname = 'docs/source/' + env.doc2path(env.docname, base=None) %}
# .. raw:: html

#    <div class="binder-badge docutils container">
#        <a class="reference external image-reference"
#           href="https://mybinder.org/v2/gh/scverse/squidpy_notebooks/{{ env.config.release|e }}?filepath={{ docname|e }}"> # noqa: E501
#        <img alt="Launch binder" src="https://mybinder.org/badge_logo.svg" width="150px">
#        </a>
#    </div>
# """  # noqa: E501

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
todo_include_todos = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_theme = "furo"
html_static_path = ["_static"]
# html_theme_options = {"navigation_depth": 4, "logo_only": True} # TODO(giovp): seems unsupported
html_show_sphinx = False

github_repo = "moscot"
github_repo_nb = "moscot_notebooks"


def setup(app: Sphinx) -> None:
    app.add_css_file("css/custom.css")
