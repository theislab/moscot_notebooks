#!/usr/bin/env python
"""
Solving quadratic problems basic
--------------------------------
"""

###############################################################################
# This notebook elaborates on how to quadratic problems, e.g. the
# :class:`moscot.problems.time.LineageProblem`,
# the :class:`moscot.problems.spatio_temporal.SpatioTemporalProblem`,
# the :class:`moscot.problems.space.MappingProblem`,
# the :class:`moscot.problems.time.AlignmentProblem`,
# the :class:`moscot.problems.generic.GWProblem`, 
# and the the :class:`moscot.problems.generic.FGWProblem`.

import scanpy as sc
import numpy as np

from moscot.datasets import simulate_data
from moscot.problems.generic import GWProblem, FGWProblem

adata = simulate_data(n_distributions=2, key="batch", quad_cost_matrix="spatial")
sc.pp.pca(adata)
adata

###############################################################################
# Basic parameters 
# ~~~~~~~~~~~~~~~~
# There are some paraemeters in quadratic problems which play the same role as 
# in linear problems. Hence, we refer to TODO for the role of `epsilon`, `tau_a`,
# and `tau_b`. In fused quadratic problems (also referred to as Fused Gromov-
# Wasserstein) there is an additional parameter `alpha` defining the convex
# combination between the quadratic and the linear term. Setting `alpha=1` only
# considers the quadratic term, while `alpha -> 1` only considers the linear term.
# While choosing `alpha=0` is possible in fused quadratic problems, and corresponds
# to the pure quadratic problem, `alpha=0` is
# not possible, and hence linear problems must be chosen. 

gwp = GWProblem(adata)
gwp = gwp.prepare(key="batch", GW_x="spatial", GW_y="spatial")
gwp = gwp.solve(alpha=0, epsilon=1e-1)

fgwp = FGWProblem(adata)
fgwp = fgwp.prepare(key="batch", GW_x="spatial", GW_y="spatial", joint_attr="X_pca")
fgwp = fgwp.solve(epsilon=1e-1)

max_difference = np.max(np.abs(gwp["0", "1"].solution.transport_matrix - fgwp["0", "1"].solution.transport_matrix))
print(f"{max_difference:.6f}")

###############################################################################
# Low-rank solutions
# ~~~~~~~~~~~~~~~~~~
# Whenever the dataset is very large, the computational complexity can be
# reduced by setting `rank` to a positive integer (:cite:`scetbon:21a`). In this
# case, `epsilon` can also be set to 0, while only the balanced case
# (`tau_a = tau_b = 1`) is supported. Moreover, the data has to be provided
# as point clouds, i.e. no precomputed cost matrix can be passed. 
gwp = gwp.solve(epsilon=1e-2, rank=3)

###############################################################################
# Scaling the cost
# ~~~~~~~~~~~~~~~~
# `scale_cost` works the same way as for linear problems. Note that all cost
# terms will be scaled by the same argument. 

###############################################################################
# TODO See other examples for ...