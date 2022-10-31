#!/usr/bin/env python
"""
Passing lineage trees as cost
-----------------------------
"""

###############################################################################
# This notebook demonstrates how lineage trees can be passed, specifically
# useful for the :class:`moscot.problems.time.LineageProblem`.
#
# The :class:`moscot.problems.time.LineageProblem` requires lineage information.
# :mod:`moscot` allows this in three way: by passing precomputed cost matrices,
# by passing barcodes or by passing a lineage tree as a :class:`networkx.DiGraph`.
# In this notebook, we consider the lineage tree case.

from moscot.datasets import simulate_data
from moscot.problems.time import LineageProblem

adata = simulate_data(n_distributions=3, key="day", quad_term="tree")
adata

###############################################################################
# We assume trees to be saved in :attr:`anndata.AnnData.uns` as a dictionary.

adata.uns["trees"]

###############################################################################
# Now, we can instantiate and prepare the :class:`moscot.problems.time.LineageProblem`
# by specifying the cost


lp = LineageProblem(adata)
lp = lp.prepare(time_key="day", lineage_attr={"attr": "uns", "key": "trees", "cost": "leaf_distance"})

###############################################################################
# Internally, cost matrices have been computed from the trees, according to the leaf
# distance. Let us investigate the prepared problem. First, we print the first few
# entries of the cost matrix computed from the first lineage tree.
lp[0, 1].x.data[:3, :3]

###############################################################################
# Similarly, we investigate parts of the cost matrix created from the second tree.
lp[0, 1].y.data[:3, :3]

###############################################################################
# Note that the gene expression term is still saved as two point clouds. The
# cost matrix will be computed by the backend.
lp[0, 1].xy.data.shape, lp[0, 1].xy.data_y.shape

###############################################################################
# TODO See other examples for ...
