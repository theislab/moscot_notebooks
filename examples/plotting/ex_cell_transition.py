#!/usr/bin/env python
"""
Plotting cell transitions
-------------------------
"""

###############################################################################
# In this notebook, we will showcase how to use :meth:`moscot.plotting.cell_transition`.
# We use the HSPC dataset to demonstrate the usage.

from moscot.datasets import hspc
from moscot.problems.time import TemporalProblem
import moscot.plotting as mpl

adata = hspc()

###############################################################################
# First, we need to prepare and solve the problem. Here, we set the `threshold`
# parameter to a relative high value to speed up convergence at the cost of
# lower quality.

tp = TemporalProblem(adata).prepare(time_key="day").solve(epsilon=1e-2, threshold=1e-2)

###############################################################################
# As for all plotting functionalities in moscot, we first call the method of
# the problem class, which stores the results of the computation in the
# :class:`anndata.AnnData` instance. Let us assume we want to plot the cell transition
# between time point 4 and time point 7. Moreover, we want the rows and columns
# of our transition matrix to represent cell types. In general, we can aggregagte
# by any column in :attr:`anndata.AnnData.obs` via the `source_groups` parameter and
# the `target_groups` parameter, respectively. Moreover, we are intereseted in
# descendants as opposed to ancestors, which is why we choose `forward` to be `True`.

cell_transition = tp.cell_transition(
    source=4, target=7, source_groups="cell_type", target_groups="cell_type", forward=True
)

###############################################################################
# `cell_transition` is a data frame containing all the information needed, we now
# want to nicely visualize the result with :meth:`moscot.plotting.cell_transition`.
# Therefore, we can either pass the :class:`anndata.AnnData` instance or the problem
# instance. Depending on the size of our transition matrix, we might want to adapt the
# `dpi` parameter and the `fontsize` parameter. If we don't want to plot the values of
# the transition, e.g. because the transition matrix is very large, we can simply set
# the `annotation` parameter to `False`.

mpl.cell_transition(tp, dpi=100, fontsize=10)

###############################################################################
# By default, the result of the `cell_transition` method of a problem instance is saved
# `anndata.AnnData.uns['moscot_results']['cell_transition']['cell_transition'] and overrides
# this element every time the method is called. To prevent this, we can specify the parameter
# `key_added`, which we will do to store the results of the following use case.

###############################################################################
# We can also visualize transitions of only a subset of categories of an :attr:`anndata.AnnData.obs` column
# by passing a dictionary for `source_groups` or `target_groups`. Moreover, passing
# a dictionary also allows to specify the order of the `source_groups` and `target_groups`,
# respectively.
new_key = "subset_cell_transition"
_ = tp.cell_transition(
    source=4,
    target=7,
    source_groups={"cell_type": ["HSC", "MasP", "MkP", "NeuP"]},
    target_groups={"cell_type": ["MasP", "MkP", "BP"]},
    forward=True,
    key_added=new_key,
)
mpl.cell_transition(tp, dpi=100, fontsize=10, uns_key=new_key)
