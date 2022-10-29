#!/usr/bin/env python
"""
Quadratic solver
----------------
"""
###############################################################################
# This example shows how to solve a Fused Qaudratic problem.

###############################################################################
# Let's load the data, this dataset contains spatiotemporal transcriptomics

from moscot.datasets import mosta
from moscot.problems.spatio_temporal import SpatioTemporalProblem

###############################################################################
# Let's load the data, this dataset contains spatiotemporal transcriptomics
# atlas of mouse organogenesis in two time points, E9.5, E10.5
adata = mosta()

###############################################################################
# We start by initializing a spatio-temporal problem and preparing it.

stp = SpatioTemporalProblem(adata=adata).prepare(
    time_key="time",
    spatial_key="spatial",
    joint_attr=None,
    callback="local-pca",
)

###############################################################################
# Below are some useful parameters of
# `moscot.problems.time.SpatioTemporalProblem.solve()`:
#
# - `alpha` - Interpolation parameter between quadratic term (spatial coordinates) and linear term (PCA space).
#
# - `epsilon` – entropic regularization term.
#
# - `scale_cost` – option to rescale the cost matrix. Implemented scalings are
#       "median", "mean", "max_cost", "max_norm" and "max_bound".
#       Alternatively, a float factor can be given to rescale the cost such
#       that ``cost_matrix /= scale_cost``. If `True`, use "mean".
#
# - `batch_size` – size of the batch for online computation avoiding matrix instantiation
#
# - `max_iterations` -  the maximum number of Sinkhorn iteration`
#
# - `stage` – stages of sub-problems which are to be solved. By default, prepared and solved problems are solved,
#     ("prepared", "solved").
#
# - `initializer` -     Initializer to use for the problem. In the non-low rank regime available options are:
#         - `default` (constant scalings)
#         - `gaussian` (:cite:`thornton:22`)
#         - `sorting` (:cite:`thornton:22`)
#     If `None`, the default is `default`.
# - `initializer_kwargs` - keyword arguments for the initializer, taken from
#       https://github.com/ott-jax/ott/blob/main/ott/core/initializers.py.

# stp = stp.solve(
#    alpha=0.5,
#    epsilon=1e-3,
#    scale_cost="mean",
#    #batch_size=256,
#    max_iterations=1e2,
#    stage=("prepared", "solved"),
#    initializer="sorting",
# )
# stp.solutions
