#!/usr/bin/env python
"""
Plotting pull or push distributions
-----------------------------------
"""

###############################################################################
# In this notebook, we will showcase how to use :meth:`moscot.plotting.push` and
# its counterpart :meth:`moscot.plotting.pull`.
# These visualisation functions are only implemented for non-spatial problems.
# To see how pullback or pushforward cell distributions can be visualized for
# problems incorporating spatial information, please have a look at the tutorials.
# Here, we use the HSPC dataset to demonstrate the usage of :meth:`moscot.plotting.push` and
# :meth:`moscot.plotting.pull` with the :class:`moscot.problems.time.TemporalProblem`.
# In this context, the pull-back distribution corresponds to the set of ancestor cells, while
# the push-forward distribution corresponds to the set of descending cells.

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
# :class:`anndata.AnnData` instance. Let us assume we look for the descendants
# of cells of time point 4 in time point 7. We can specify whether we want to
# return the result via the `return_data` parameter.
tp.push(start=4, end=7, return_data=False)

###############################################################################
# We can now visualize the result. As we have multiple time points in the UMAP
# embedding, it is best to visualize in one plot all the cells corresponding to
# time point 4, and then the ones corresponding to the descending cells.
# As the :class:`anndata.AnnData` instance contains UMAP embeddings for both
# gene expression and ATAC, we need to define which one to use via `basis`.

mpl.push(tp, time_points=[4], basis="umap_GEX")
mpl.push(tp, time_points=[7], basis="umap_GEX")

###############################################################################
# By default, the result of the `push` method of a problem instance is saved
# `anndata.AnnData.uns['moscot_results']['push']['push'] and overrides
# this element every time the method is called. To prevent this, we can specify the parameter
# `key_added`, which we will do to store the results of the following use case.

###############################################################################
# We can also visualize the descendants of only a subset of categories of an
# :attr:`anndata.AnnData.obs` column
# by specifying the `data` and the `subset` parameter.
new_key = "subset_push"
tp.push(start=4, end=7, data="cell_type", subset="HSC", return_data=False, key_added=new_key)
mpl.push(tp, time_points=[4], uns_key=new_key, basis="umap_GEX")
mpl.push(tp, time_points=[7], uns_key=new_key, basis="umap_GEX")
