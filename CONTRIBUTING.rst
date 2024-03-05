How to write examples and tutorials for moscot
==============================================

Examples and tutorials are created using `sphinx-gallery <https://sphinx-gallery.github.io/stable/index.html>`_.

We distinguish between examples and tutorials:

- *Examples* are short explanations of one function (and optionally its related plotting function).
  See `here <https://https://moscot.readthedocs.io/en/latest/notebooks/examples/plotting/200_cell_transitions.html>`__
  for an example.
- *Tutorials* are longer vignettes, e.g., showing entire workflows.
  See `here <https://https://moscot.readthedocs.io/en/latest/notebooks/tutorials/100_lineage.html>`__ for an example.

Set up environment
------------------
1. git clone most recent versions of moscot and its notebooks.
2. install latest version of moscot with ``pip install -e'.[dev,test]'``.
3. run ``pre-commit install`` in both repos.

Datasets for examples/tutorials
-------------------------------
For showcasing functions, please use one of the datasets shipped with moscot.
If you would like to add a new dataset, please open an issue.

- `moscot.datasets.bone_marrow <https://moscot.readthedocs.io/en/latest/genapi/moscot.datasets.bone_marrow.html#moscot.datasets.bone_marrow>`_ - multiome data of bone marrow measurements
- `moscot.datasets.c_elegans <https://moscot.readthedocs.io/en/latest/genapi/moscot.datasets.c_elegans.html#moscot.datasets.c_elegans>`_ - scRNA-seq time-series dataset of C.elegans embryogenesis
- ``moscot.datasets.drosophila`` - embryo of Drosophila melanogaster
- ``moscot.datasets.hspc`` - CD34+ hematopoietic stem and progenitor cells from 4 healthy human donors
- ``moscot.datasets.mosta`` - preprocessed and extracted data
- ``moscot.datasets.sciplex`` - perturbation dataset
- ``moscot.datasets.sim_align`` - spatial transcriptomics simulated dataset
- ``moscot.datasets.simulate_data`` - simulate data
- ``moscot.datasets.tedsim`` - dataset simulated with TedSim
- ``moscot.datasets.zebrafish`` - lineage-traced scRNA-seq time-series dataset of Zebrafish heart regeneration


Main examples and tutorials
---------------------------
Examples and Tutorials are represented as an executable **Python file**.
The general structure is described `here <https://sphinx-gallery.github.io/stable/syntax.html>`_ .
You can work on a jupyter notebook to develop the example, but the file needs to be pushed as a ``.ipynb`` file.
You can conveniently go back and forth with ``jupytext`` (install it with pip):

.. code-block::

   jupytext --to py:sphinx mynotebook.ipynb  # create .py file
   jupytext --to notebook mynotebook.py  # create .ipynb file

The pre-commit will flag potential problems for you.
One of the most common problems is that lines of text go over 120 characters, so make sure to check that.
Remember that the text cells in examples will be rendered with rst, so checkout this
`cheatsheet <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_.

Make sure to follow the following checklist before merging a new example/tutorial:

- if using math expressions, ensure they render properly (e.g. using the ``{math}`` directive for rst).
- make sure we're referring to the package always the same, e.g. *moscot*.
- use the ``.. seealso::`` directive to highlight the prominence of other examples in the introductory text.
- ensure examples/tutorials are properly linked (sphinx will throw warnings if not).
  Link to examples using the following syntax ``{doc}`examples/plotting/200_cell_transitions```.
- ensure that in ``.ipynb`` files, first line after the title is of the following format::

    """
    Super tutorial title
    --------------------

    This {example,tutorial} shows how to ...

    Keep 1 line above free; here comes the general description.
    ... seealso::
    <here recommend other examples>
    """

  The first line after title should be short, since this is the hover info displayed when hovering over the tutorial.
- ensure that citations are in ``docs/references.bib`` and are used within the examples/tutorials.
  Cite in .rst using the ``{cite}`` directive and in .ipynb files using ``<cite data-cite="...">...</cite>``.
  In ``references.bib``, remove the ``url`` and ``eprint`` tags, just leave the ``DOI``.
  The problem is that for ``url``, it gets incorrectly prefixed with ``https://arxiv.org``.
- ensure when referencing functions/classes/packages/etc., we use RST roles, such as:
  ``{func}`~moscot.problems.space.MappingProblem.annotation_mapping```, ``{class}`~moscot.problems.generic.SinkhornProblem```, etc.
- ensure that example/tutorial titles are capitalized, but do not follow Camel Case style
  (i.e. Process image is good, Process Image is bad).
- for example values, use ``foo = 'bar'`` instead of ``foo='bar'`` or ``foo = "bar"``
  (to be more consistent with main docs).
- ensure that .py examples/tutorials are executable (``chmod +x``) and
  have ``#!/usr/bin/env python`` shebang at the top.
- lastly, add the example/tutorial to the appropriate place in the directory structure in this repository.

After successfully merging the new example/tutorial in the moscot_notebooks repository, the main repository also needs to be updated.
1. create and switch to a new branch in the moscot repository
2. go to ``docs/notebooks``, git fetch and git pull
3. open a new pull request with these changes
