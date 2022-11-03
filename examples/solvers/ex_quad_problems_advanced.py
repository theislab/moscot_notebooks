#!/usr/bin/env python
"""
Solving quadratic problems - advanced
-------------------------------------

.. seealso::
    See :ref:`sphx_glr_auto_examples_solvers_ex_quad_problems_basic.py` for an introduction
    to solving quadratic problems.
    See :ref:`sphx_glr_auto_examples_solvers_ex_linear_problems_basic.py` for an introduction
    to solving linear problems.
    See :ref:`sphx_glr_auto_examples_solvers_ex_linear_problems_advanced.py` for an advanced
    example how to solve linear problems.
"""

from moscot.datasets import simulate_data
from moscot.problems.generic import GWProblem

###############################################################################
# This examples is a continuation of TODO reference and shows advanced examples
# for how to solve quadratic problems,
# e.g. the
# :class:`moscot.problems.time.LineageProblem`,
# the :class:`moscot.problems.spatio_temporal.SpatioTemporalProblem`,
# the :class:`moscot.problems.space.MappingProblem`,
# the :class:`moscot.problems.time.AlignmentProblem`,
# the :class:`moscot.problems.generic.GWProblem`,
# and the the :class:`moscot.problems.generic.FGWProblem`.
import scanpy as sc

adata = simulate_data(n_distributions=2, key="day", quad_cost_matrix="spatial")
adata

###############################################################################
# Threshold
# ~~~~~~~~~
# The `threshold` parameter defines the convergence criterion. In the balanced
# setting the `threshold` denotes the deviation between prior and posterior
# marginals, while in the unbalanced setting the `threshold` corresponds to
# a Cauchy sequence stopping criterion.
adata = simulate_data(n_distributions=2, key="batch", quad_cost_matrix="spatial")
sc.pp.pca(adata)
gwp = GWProblem(adata)
gwp = gwp.prepare(key="batch", GW_x="spatial", GW_y="spatial")

###############################################################################
# Initializers
# ~~~~~~~~~~~~
# Different Initializers can help to improve convergence. For the full-rank
# case only the default initializer exists, hence the `initializer` argument
# must be set to `None`.
#
# For low-rank problems the same initializers as for the linear low-rank solvers
# are available, and `initializer_kwargs` can be passed the same way, see TODO

###############################################################################
# Number of iterations
# ~~~~~~~~~~~~~~~~~~~~
# To solve a quadratic Optimal Transport problem, a consecutively updated linearized
# problem is solved `n_iterations` time. Here, `min_iterations` denotes a lower bound
# for `n_iterations` and `max_iterations` an upper bound. If `max_iterations` is too
# low, the model might not converge.
gwp = gwp.solve(alpha=0.5, epsilon=1e-1, min_iterations=0, max_iterations=1)

###############################################################################
# Iterations of the inner loop & linear solver keyword arguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# As mentioned above, each outer loop step of the Gromov-Wasserstein algorithm
# consists of solving a linear problem. Arguments for the linear solver can
# be specified via `linear_solver_kwargs`, keyword arguments for
# :class:`ott.core.sinkhorn.Sinkhorn` in the full-rank case or keyword arguments
# for :class:`ott.core.sinkhorn_lr.LRSinkhorn`, respectively. This way, we can
# also set the minimum and maximum number of iterations for the linear solver:
ls_kwargs = {"min_iterations": 10, "max_iterations": 100}
gwp = gwp.solve(alpha=0.5, epsilon=1e-1, linear_solver_kwargs=ls_kwargs)

###############################################################################
# Low rank hyperparameters
# ~~~~~~~~~~~~~~~~~~~~~~~~
# The parameters `gamma` and `gamma_rescale` are the same as in the linear case,
# see example TODO.
# It remains to consider `ranks` and `tolerances`.


###############################################################################
# Keyword arguments & Implementation details
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Whenever the `solve` method of a quadratic problem is called,
# a backend-specific quadratic solver is instantiated. Currently, :mod:`ott` is
# supported, its corresponding quadratic solvers is :class:`ott.core.gromov_wasserstein.GromovWasserstein`,
# handling both the full-rank and the low-rank case. :mod:`moscot` wraps this
# class in :class:`moscot.backends.ott.GWSolver` and :class:`moscot.backends.ott.FGWSolver`,
# handling the purely quadratic and the fused quadratic problem, respectively.
