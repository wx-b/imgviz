# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import inspect
import os
import pkg_resources
import sys

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # NOQA

import _docstring_check

__version__ = pkg_resources.get_distribution('imgviz').version
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
tag = 'master'

# -- Project information -----------------------------------------------------

project = u'imgviz'
copyright = '2019, Kentaro Wada'
author = 'Kentaro Wada'

# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.linkcode',
    'sphinx.ext.mathjax',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'imgvizdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'imgviz.tex', u'imgviz Documentation',
     u'Matthew Matl', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'imgviz', u'imgviz Documentation', [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'imgviz', u'imgviz Documentation',
     author, 'imgviz', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
}

# Autosummary fix
autosummary_generate = True

# Try to suppress multiple-definition warnings by always taking the shorter
# path when two or more paths have the same base module


def setup(app):
    app.connect('autodoc-process-docstring', _autodoc_process_docstring)


def _autodoc_process_docstring(app, what, name, obj, options, lines):
    _docstring_check.check(app, what, name, obj, options, lines)


def _import_object_from_name(module_name, fullname):
    obj = sys.modules.get(module_name)
    if obj is None:
        return None
    for comp in fullname.split('.'):
        obj = getattr(obj, comp)
    return obj


def _is_egg_directory(path):
    return (path.endswith('.egg') and
            os.path.isdir(os.path.join(path, 'EGG-INFO')))


def _is_git_root(path):
    return os.path.isdir(os.path.join(path, '.git'))


_source_root = None


def _find_source_root(source_abs_path):
    # Note that READTHEDOCS* environment variable cannot be used, because they
    # are not set under docker environment.
    global _source_root
    if _source_root is None:
        dir = os.path.dirname(source_abs_path)
        while True:
            if _is_egg_directory(dir) or _is_git_root(dir):
                # Reached the root directory
                _source_root = dir
                break

            dir_ = os.path.dirname(dir)
            if len(dir_) == len(dir):
                raise RuntimeError('Couldn\'t parse root directory from '
                                   'source file: {}'.format(source_abs_path))
            dir = dir_
    return _source_root


def _get_source_relative_path(source_abs_path):
    return os.path.relpath(source_abs_path, _find_source_root(source_abs_path))


def _get_sourcefile_and_linenumber(obj):
    # Retrieve the original function wrapped by contextlib.contextmanager
    if callable(obj):
        closure = getattr(obj, '__closure__', None)
        if closure is not None:
            obj = closure[0].cell_contents

    # Get the source file name and line number at which obj is defined.
    try:
        filename = inspect.getsourcefile(obj)
    except TypeError:
        # obj is not a module, class, function, ..etc.
        return None, None

    # inspect can return None for cython objects
    if filename is None:
        return None, None

    # Get the source line number
    _, linenum = inspect.getsourcelines(obj)

    return filename, linenum


def linkcode_resolve(domain, info):
    if domain != 'py' or not info['module']:
        return None
    if 1 == int(os.environ.get('IMGVIZ_DOCS_SKIP_LINKCODE', 0)):
        return None

    # Import the object from module path
    obj = _import_object_from_name(info['module'], info['fullname'])

    # If it's not defined in the internal module, return None.
    mod = inspect.getmodule(obj)
    if mod is None:
        return None
    if not (mod.__name__ == 'imgviz' or mod.__name__.startswith('imgviz.')):
        return None

    # Retrieve source file name and line number
    filename, linenum = _get_sourcefile_and_linenumber(obj)
    if filename is None or linenum is None:
        return None

    filename = os.path.realpath(filename)
    relpath = _get_source_relative_path(filename)

    return 'https://github.com/iory/imgviz/blob/{}/{}#L{}'.format(
        tag, relpath, linenum)