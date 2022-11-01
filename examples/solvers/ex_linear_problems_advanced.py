#!/usr/bin/env python
"""
Solving linear problems
-----------------------
"""

###############################################################################
# This examples is a continuation of TODO reference and shows advanced examples
# for how to solve linear problems like the 
# :class:`moscot.problems.time.TemporalProblem` and the
# :class:`moscot.problems.generic.SinkhornProblem`.

import numpy as np
from moscot.datasets import simulate_data
from moscot.problems.generic import SinkhornProblem

adata = simulate_data(n_distributions=2, key="day")
adata

###############################################################################
# Threshold
# ~~~~~~~~~
# The `threshold` parameter defines the convergence criterion. In the balanced
# setting the `threshold` denotes the deviation between prior and posterior
# marginals, while in the unbalanced setting the `threshold` corresponds to 
# a Cauchy sequence stopping criterion. 
# 
# Initializers
# ~~~~~~~~~~~~
# Different Initializers can help to improve convergence. For the full-rank
# case we can set the initializer to the trivial initializing method denoted
# by `default`. The `gaussian` (:cite:`thornton2022`) initializer computes
# Gaussian approximations of two point clouds and leverages the closed-form 
# solution of Optimal Transport problems between Gaussians, while the `sorting`
# initializer (:cite:`thornton2022`) solves a simplified (sorting) Optimal Transport 
# problem and uses its solution as initializer. See :mod:`ott.core.initializers`
# for details.
# 
# For low-rank problems different initializers are available, see 
# :mod:`ott.core.initializers_lr`. Initialization can be `random`, `rank2`
# (:cite:`scetbon:22b`), `k-means`, or `generalized-k-means`.
# For some initializers keyword arguments can be provided as a dictionary,
# e.g. `min_iterations`
# and `max_iterations` can be provided for the k-means algorithm used by
# the `k-means` initializer. 

sp = SinkhornProblem(adata)
sp = sp.prepare(key="day")

ik = {"min_iterations": 5, "max_iterations": 200}
sp = sp.solve(epsilon=0, rank=3, initializer="k-means", initializer_kwargs=ik)

###############################################################################
# Number of iterations
# ~~~~~~~~~~~~~~~~~~~~
# There are three types of iterations, which can be set. `min_iterations` is the
# minimum number of iterations of the algorithm. `max_iterations` is the
# maximum number of iterations. If the convergence criterion is not met 
# after completing `max_iterations`, the model has not converged. `inner_iterations`
# is the number of iterations after which the model checks the convergence criterion.
# If `max_iterations` is too low, the model won't converge:
sp = sp.solve(epsilon=1e-3, inner_iterations=1, min_iterations=0, max_iterations=2)


###############################################################################
# Low rank hyperparameters
# ~~~~~~~~~~~~~~~~~~~~~~~~
# The low-rank algorithm requires more hyperparameters, i.e. `gamma`, the
# a step size of the mirror descent algorithm and `gamma_rescale`, a flag
# indicicating whether to rescale `gamma`. When tuning `gamma`, we recommend
# trying orders of 10. If `gamma` is too small or too large, the algorithm
# might not converge
sp = sp.solve(epsilon=0, rank=3, initializer="random", max_iterations=30, gamma=1000)

###############################################################################
sp = sp.solve(epsilon=0, rank=3, initializer="random", max_iterations=30, gamma=10)

###############################################################################
# Keyword arguments & Implementation details
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Whenever the :meth:`moscot.problems.time.TemporalProblem.solve` is called,
# a backend-specific linear solver is instantiated. Currently, :mod:`ott` is
# supported, its corresponding linear solvers are :class:`ott.core.sinkhorn.Sinkhorn`,
# which is used whenever `rank = -1`, and :class:`ott.core.sinkhorn_lr.LRSinkhorn`,
# its counterpart whenever `rank` is a positive integer. :mod:`moscot` wraps these 
# classes in :class:`moscot.backends.ott.SinkhornSolver` which handles both full and
# low rank.
# 
# TODO See other examples for ...
