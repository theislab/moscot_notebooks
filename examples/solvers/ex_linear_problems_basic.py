#!/usr/bin/env python
"""
Solving linear problems
-----------------------
"""

###############################################################################
# This notebook elaborates on how to solve linear problems, e.g. the
# :class:`moscot.problems.time.TemporalProblem` and the
# :class:`moscot.problems.generic.SinkhornProblem`.

from moscot.datasets import simulate_data
from moscot.problems.generic import SinkhornProblem

import numpy as np

adata = simulate_data(n_distributions=2, key="day")
adata

###############################################################################
# The :meth:`moscot.problems.time.TemporalProblem.solve` has numerous arguments,
# a few of which will be discussed in the following.
###############################################################################
# Basic parameters
# ~~~~~~~~~~~~~~~~
# `epsilon` is the regularization parameter. The lower `epsilon`, the sparser the
# transport map. At the same time, the algorithm takes longer to converge. `tau_a`
# and `tau_b` denote the unbalancedness parameters in the source and the target
# distribution, respectively. `tau_a = 1` means the source marginals have to be fully
# satisfied while `0 < tau_a < 1` relaxes this condition. Analgously, `tau_b` affects
# the marginals of the target distribution. We demonstrate the effect of `tau_a` and `tau_b`
# with the :class:`moscot.problems.generic.SinkhornProblem`.
# Whenever the prior marginals `a` and `b` of the source and the target distribution,
# respectively, are not passed (TODO link to marginals notebook), they are set to be uniform.

sp = SinkhornProblem(adata)
sp = sp.prepare(key="day")
print(sp[0, 1].a[:5], sp[0, 1].b[:5])

###############################################################################
# First, we solve the problem in a balanced manner, such that the posterior marginals of the
# solution (the sum over the rows and the columns for the source marginals and the
# target marginals, respectively) are equal to the prior marginals up to small
# errors (which define the convergence criterion in the balanced case).
sp = sp.solve(epsilon=1e-2, tau_a=1, tau_b=1)
print(sp[0, 1].solution.a[:5], sp[0, 1].solution.b[:5])


###############################################################################
# If we solve an unbalanced problem, the posterior marginals will be different.
sp = sp.solve(epsilon=1e-2, tau_a=0.9, tau_b=0.99)
print(sp[0, 1].solution.a[:5], sp[0, 1].solution.b[:5])

###############################################################################
# Low-rank solutions
# ~~~~~~~~~~~~~~~~~~
# Whenever the dataset is very large, the computational complexity can be
# reduced by setting `rank` to a positive integer (:cite:`scetbon:21a`). In this
# case, `epsilon` can also be set to 0, while only the balanced case
# (`tau_a = tau_b = 1`) is supported. The `rank` should be significantly
# smaller than the number of cells in both source and target distribution.

sp = sp.solve(epsilon=0, rank=3)

###############################################################################
# Scaling the cost
# ~~~~~~~~~~~~~~~~
# `scale_cost` scales the cost matrix which often helps the algorithm to converge.
# While any number can be passed, it is also possible to scale the cost matrix
# by e.g. its mean, median, and maximum. We recommend using the `mean` as this
# is possible without instantiating the cost matrix and hence reduces computational
# complexity. Moreover, it is more stable w.r.t. outliers than for example scaling
# by the maximum. Note that the solution of the Optimal Transport is not stable
# across different scalings:
sp = sp.solve(epsilon=1e-2, scale_cost="mean")
tm_mean = sp[0, 1].solution.transport_matrix
print(tm_mean[:3, :3])

###############################################################################
sp = sp.solve(epsilon=1e-2, scale_cost="max_cost")
tm_max = sp[0, 1].solution.transport_matrix
print(tm_max[:3, :3])

###############################################################################
# We can compute the correlation of the flattened transport matrix to get an
# idea of the influence of different scalings.
correlation = np.corrcoef(tm_mean.flatten(), tm_max.flatten())[0, 1]
print(f"{correlation:.4f}")

###############################################################################
# TODO See other examples for ...
