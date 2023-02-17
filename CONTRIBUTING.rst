How to write examples and tutorials for moscot
==============================================
Examples and tutorials are created using `sphinx-gallery <https://sphinx-gallery.github.io/stable/index.html>`_.
They are automatically run by CI every time a PR is merged to mater in the
`moscot repository <https://github.com/theislab/moscot>`_.

We distinguish between four types of examples and tutorials:

- *Examples* are short explanations of one function (and optionally its related plotting function).
  TODO link example
- *Tutorials* are longer vignettes, e.g., showing entire workflows.
  TODO link example
- *External tutorials* are tutorials that use external python packages that should be excluded from CI.
  They should be placed in ``docs/source/external_tutorials/`` and prefixed with ``tutorial_``.
- *OT tutorials* TODO

Datasets for examples/tutorials
-------------------------------
For showcasing functions, please use one of the datasets shipped with moscot.

- ``moscot.datasets.simulated()`` - good for graph
- ``moscot.datasets.hspc()`` - good for graph
- ``moscot.datasets.pancreas_multiome()`` - good for graph

Main examples and tutorials
---------------------------
.. TODO(michalk8): update
Examples and Tutorials are represented as an executable **Python file**.
The general structure is described `here <https://sphinx-gallery.github.io/stable/syntax.html>`_ .
You can work on a jupyter notebook to develop the example, but the file needs to be pushed as a ``.py`` file.
You can conveniently go back and forth with ``jupytext`` (install it with pip):

.. code-block::

   jupytext --to py:sphinx mynotebook.ipynb  # create .py file
   jupytext --to notebook mynotebook.py  # create .ipynb file

The pre-commit will flag potential problems for you.
One of the most common problems is that lines of text go over 120 characters, so make sure to check that.
Remember that the text cells in examples will be rendered with rst, so checkout this
`cheatsheet <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_.

Make sure to follow the following checklist before merging a new example/tutorial:

- if using math expressions, ensure they render properly (e.g. using the ``:math:`` directive for rst).
- make sure we're referring to the package always the same way, e.g. *moscot*.
- use the ``.. seealso::`` directive to highlight the prominence of other examples in the introductory text.
- ensure examples/tutorials are properly linked (sphinx will throw warnings if not).
  Link to examples using the following syntax ``:ref:`sphx_glr_auto_tutorials_tutorial_seqfish.py```. TODO: adapt
- ensure that in ``.py`` files, first line after the title is of the following format::

    """
    Super tutorial title
    --------------------

    This {example,tutorial} shows how to ...

    Keep 1 line above free; here comes the general description.
    ... seealso::
    <here recommend other examples>
    """

  The first line after title should be short, since this is the hover info displayed when hovering over the tutorial.
- ensure that citations are in ``docs/source/references.bib`` and are used within the examples/tutorials.
  Cite in .rst using the ``:cite:`` directive and in .ipynb files using ``<cite data-cite="...">...</cite>``.
  In ``references.bib``, remove the ``url`` and ``eprint`` tags, just leave the ``DOI``.
  The problem is that for ``url``, it gets incorrectly prefixed with ``https://arxiv.org``.
- ensure when referencing functions/classes/packages/etc., we use RST roles, such as:
  ``:func:`moscot.pl.cell_transition```, ``:class:`moscot.problems.time.TemporalProblem```, etc.
- ensure that example/tutorial titles are capitalized, but do not follow Camel Case style
  (i.e. Compute transport map is fine, Compute Transport Map is bad).
- for example values, use ``foo = 'bar'`` instead of ``foo='bar'`` or ``foo = "bar"``
  (to be more consistent with main docs).
- ensure that .py examples/tutorials are executable (``chmod +x``) and
  have ``#!/usr/bin/env python`` shebang at the top.
- lastly, add the example/tutorial to the appropriate place in ``docs/source/examples.rst`` or
  ``docs/source/tutorials.rst`` both in this repository and the main repository.

External tutorials
------------------
.. TODO(michalk8): update

Generating documentation
------------------------
.. TODO(michalk8): update
