#!/usr/bin/env python
"""
Passing custom cost matrices
----------------------------
"""

###############################################################################
# This notebook demonstrates how to pass custom cost matrices.
#
# Costs (or cost matrices) are an integral part of all OT problems. :class:`moscot`
# allows data, which cost matrices are computed from, to be passed in different ways.
# In many cases, it is desirable to pass the two cell distributions as opposed to
# a precomputed cost matrix as this reduces memory.

import scanpy as sc
from scipy.sparse import dok_matrix
from sklearn.metrics import pairwise_distances
from moscot.datasets import simulate_data
from moscot.problems.time import TemporalProblem, LineageProblem

adata = simulate_data(n_distributions=2, key="day")
sc.pp.pca(adata)

###############################################################################
# We start with the `moscot.problems.time.TemporalProblem`, which only requires
# one cost matrix to be computed. The first option is to pass the cell distribution
# (in the embedded space) and the pairwise costs will be computed by the backend.
# This reduces the memory complexity, and hence this approach should be preferred.
tp = TemporalProblem(adata)
tp = tp.prepare(time_key="batch", joint_attr="X_pca")

###############################################################################
# We see that the data is still saved as pointclouds:
tp[0,1].x.data.shape, tp[0,1].x.data_y.shape

###############################################################################
# Alternatively, we can pre-compute the cost matrix.
obs_0 = adata.obs["day"]==0
obs_1 = adata.obs["day"]==1
cell_embedding_0 = adata[obs_0].obsm["X_pca"]
cell_embedding_1 = adata[obs_1].obsm["X_pca"]
cost_matrix = pairwise_distances(cell_embedding_0, cell_embedding_1, metric="sqeuclidean")

###############################################################################
# Custom cost matrices should be passed in :attr:`anndata.AnnData.obsp`.
