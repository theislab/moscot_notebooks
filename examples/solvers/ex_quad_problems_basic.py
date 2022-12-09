#!/usr/bin/env python
"""
Solving quadratic problems basic
--------------------------------

.. seealso::
    See :ref:`sphx_glr_auto_examples_solvers_ex_quad_problems_advanced.py` for an advanced
    example how to solve quadratic problems.
    See :ref:`sphx_glr_auto_examples_solvers_ex_linear_problems_basic.py` for an introduction
    to solving linear problems.
    See :ref:`sphx_glr_auto_examples_solvers_ex_linear_problems_advanced.py` for an advanced
    example how to solve linear problems.
"""

###############################################################################
# This notebook elaborates on how to quadratic problems, e.g. the
# :class:`moscot.problems.time.LineageProblem`,
# the :class:`moscot.problems.spatio_temporal.SpatioTemporalProblem`,
# the :class:`moscot.problems.space.MappingProblem`,
# the :class:`moscot.problems.time.AlignmentProblem`,
# the :class:`moscot.problems.generic.GWProblem`,
# and the the :class:`moscot.problems.generic.FGWProblem`.

from moscot.datasets import simulate_data
from moscot.problems.generic import GWProblem, FGWProblem
import scanpy as sc

import numpy as np

adata = simulate_data(n_distributions=2, key="batch", quad_term="spatial")
sc.pp.pca(adata)
print(adata)

###############################################################################
# Basic parameters
# ~~~~~~~~~~~~~~~~
# There are some parameters in quadratic problems which play the same role as
# in linear problems. Hence, we refer to TODO for the role of `epsilon`, `tau_a`,
# and `tau_b`. In fused quadratic problems (also referred to as Fused Gromov-
# Wasserstein) there is an additional parameter `alpha` defining the convex
# combination between the quadratic and the linear term. Setting `alpha=1` only
# considers the quadratic term, while `alpha -> 0` only considers the linear term.
# While choosing `alpha=0` is possible in fused quadratic problems, and corresponds
# to the pure quadratic problem, `alpha=0` is
# not possible, and hence linear problems must be chosen.

gwp = GWProblem(adata)
gwp = gwp.prepare(key="batch", GW_x={"attr": "obsm", "key": "spatial"}, GW_y={"attr": "obsm", "key": "spatial"})
gwp = gwp.solve(alpha=0, epsilon=1e-1)

fgwp = FGWProblem(adata)
fgwp = fgwp.prepare(
    key="batch", GW_x={"attr": "obsm", "key": "spatial"}, GW_y={"attr": "obsm", "key": "spatial"}, joint_attr="X_pca"
)
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
