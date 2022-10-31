#!/usr/bin/env python
"""
Handling marginals
------------------
"""

###############################################################################
# This notebook demonstrates how to marginals are handled.
#
# Marginals define the weight of each single cell within a distribution of cells.
# In many cases, marginals are chosen to be uniform as all cells are considered
# to be equally important. In some cases, we have prior knowledge to adapt the 
# marginals. For example, 
# :meth:`moscot.problems.time.TemporalProblem.score_genes_for_marginals` computes
# the marginals such that cells expressing proliferation marker genes get a higher
# weight as they are assumed to have multiple descendants. See the TODO notebooks
# for a use case in the temporal domain. 
# Here, we demonstrate how to pass marginals with the `moscot.problems.space.AlignmentProblem`.
# We might want to adapt the marginals as we know that certain cells are outliers in space,
# so they should not influence the mapping too much.

import numpy as np
from moscot.datasets import sim_align
from moscot.problems.space import AlignmentProblem

adata = sim_align()
adata

###############################################################################
# If marginals are not specified, they are assumed to be uniform. 

ap = AlignmentProblem(adata)
ap = ap.prepare(batch_key="batch", policy="sequential")
print(ap["0","1"].a, ap["0","1"].b)

###############################################################################
# If we want to specify the marginals, they should be passed via 
# :attr:`anndata.AnnData.obs`. Let's assume, we want to assign less weight to 
# the "first" cell in our source distribution. 
source_marginals = np.ones(adata.n_obs)
source_marginals[0] = 0.5
adata.obs["source_marginals"] = source_marginals

###############################################################################
# Similarly, we want to assign less weight to cell '397-1' in the target 
# distribution.
target_marginals = np.ones(adata.n_obs)
target_marginals[np.where(adata.obs_names=='397-1')[0]] = 0.5
adata.obs["target_marginals"] = target_marginals
###############################################################################
ap2 = AlignmentProblem(adata)
ap2 = ap2.prepare(batch_key="batch", a="source_marginals", b="target_marginals")
print(ap2["0","1"].a, ap2["1","2"].b)

###############################################################################
# Note that cell `397-1` belongs to batch 2, hence it never appears in a source
# distribution as we have chosen the sequential policy. Thus, the value in
# `adata[adata.obs_names=='397-1'].obs["source_distributions"]` has no effect. 
# Similarly, the cells belonging to batch "0" are never part of a target distribution.
# Hence, the values in `adata[adata.obs["batch"]=="0"].obs["target_marginals"]` are 
# irrelevant.
# Also note that the scale of the marginals influences the convergence criterion.
# Hence, we recommend normalizing the marginals to 1.
# TODO See other examples for ...