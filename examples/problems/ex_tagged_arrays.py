#!/usr/bin/env python
"""
Tagged Arrays
-------------
"""

###############################################################################
# This notebook introduces :class:`moscot.solvers.TaggedArray`.
#
# :class:`moscot.solvers.TaggedArray` stores the data passed by the users in a unified
# way before it is passed to the backend.

from moscot.datasets import simulate_data
from moscot.problems.generic import FGWProblem
import scanpy as sc

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)
adata = simulate_data(n_distributions=2, key="batch")
sc.pp.pca(adata)
adata

###############################################################################
# We instantiate and prepare a :class:`moscot.problems.generic.FGWProblem` to demonstrate
# the role of :class:`moscot.solvers.TaggedArray`.

fgwp = FGWProblem(adata)
fgwp = fgwp.prepare(key="batch", joint_attr="X_pca", GW_x="X_pca", GW_y="X_pca")

###############################################################################
# The `:class:moscot.problems.base.OTProblem` has attributes
# `:attr:moscot.problems.base.OTProblem.xy`,
# `:attr:moscot.problems.base.OTProblem.x`, and
# `:attr:moscot.problems.base.OTProblem.y`, storing the data for the linear and
# quadratic terms, respectively. These attributes are all of type :class:`moscot.solvers.TaggedArray`.

print(fgwp["0", "1"].x)
print(fgwp["0", "1"].y)
print(fgwp["0", "1"].xy)


# Each :class:`moscot.solvers.TaggedArray` has attributes
# :attr:`moscot.solvers.TaggedArray.data_src`, :attr:`moscot.solvers.TaggedArray.data_tgt`,
# :attr:`moscot.solvers.TaggedArray.cost`, and :attr:`moscot.solvers.TaggedArray.tag`.

print(fgwp["0", "1"].xy.data_src)
print(fgwp["0", "1"].xy.data_tgt)
print(fgwp["0", "1"].xy.cost)
print(fgwp["0", "1"].xy.tag)

###############################################################################

# The :attr:`moscot.solvers.TaggedArray.tag` is of type :class:`moscot.solvers.Tag` and
# defines what kind of data is stored in the :class:`moscot.solvers.TaggedArray`.
# Possible tags are "cost_matrix", "kernel", and "point_cloud". Whenever the `tag` is "point_cloud",
# the backend is expted to compute the cost on the fly. Note that this often reduces
# memory complexity from quadratic to linear and hence is advisable.
# :attr:`moscot.solvers.TaggedArray.cost` should then specify which cost to compute from the
# point clouds.
#
# If the :class:`moscot.solvers.TaggedArray` corresponds to a linear term,
# :attr:`moscot.solvers.TaggedArray.data_src` and :attr:`moscot.solvers.TaggedArray.data_tgt`
# contain the point clouds of the source and the target distribution, respectively.

print(type(fgwp["0", "1"].xy.data_src))
print(type(fgwp["0", "1"].xy.data_tgt))

###############################################################################

# If the :class:`moscot.solvers.TaggedArray` corresponds to a quadratic term, the cost
# will be computed pairwise between points of the same distribution. Hence,
# :attr:`moscot.solvers.TaggedArray.data_tgt` will be `None`.

print(type(fgwp["0", "1"].x.data_src))
print(type(fgwp["0", "1"].x.data_tgt))

###############################################################################
# Whenever the `tag` is "cost_matrix", the backend expects an instantiated cost matrix.
# There are two different cases to distinguish. First, the user might directly want to
# pass custom cost matrices, see for example
# :ref:`sphx_glr_auto_examples_problems_ex_passing_custom_cost_matrices.py`. In this case,
# :attr:`moscot.solvers.TaggedArray.cost` must be set to `custom`. When setting custom
# cost matrices, e.g. via :meth:`moscot.problems.base.OTProblem.set_xy`, the
# :class:`moscot.solvers.TaggedArray` will change its :attr:`moscot.solvers.TaggedArray.tag`.
# Before setting the custom cost matrix we still have "point_cloud" as a tag and
# :attr:`moscot.solvers.TaggedArray.data_tgt` is not `None`, as it contains
# the point cloud of the target distribution.

print(fgwp["0", "1"].xy.tag)
print(type(fgwp["0", "1"].xy.data_tgt))

###############################################################################
# We now construct a (random) custom cost matrix for the linear term.

obs_names_0 = fgwp["0", "1"].adata_src.obs_names
obs_names_1 = fgwp["0", "1"].adata_tgt.obs_names
cost_linear_01 = np.abs(rng.normal(size=(len(obs_names_0), len(obs_names_1))))
cm_linear = pd.DataFrame(data=cost_linear_01, index=obs_names_0, columns=obs_names_1)

fgwp["0", "1"].set_xy(cm_linear, tag="cost_matrix")

print(fgwp["0", "1"].xy.tag)
print(type(fgwp["0", "1"].xy.data_tgt))

###############################################################################
# If the cost matrix is to be computed via a class in :mod:`moscot.costs`, the
# :attr:`moscot.solvers.TaggedArray.cost` must be set to the :obj:`str`, see for example
# :ref:`sphx_glr_auto_examples_problems_ex_use_leaf_distance.py`.
