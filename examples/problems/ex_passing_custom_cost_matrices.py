#!/usr/bin/env python
"""
Using custom cost matrices
--------------------------
"""

###############################################################################
# This notebook demonstrates how to use custom cost matrices
#
# Even if it is recommended to pass the data as opposed to pre-computed cost
# matrices due to computational complexity, we demonstrate in the following how
# to pass custom cost matrices.
#
# There are two ways to pass custom cost matrices, either by setting them on a
# single problem level after preparing the problem or by
# :attr:`anndata.AnnData.obsp`.

from moscot.datasets import simulate_data
from moscot.problems.generic import FGWProblem
import scanpy as sc

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)
adata = simulate_data(n_distributions=3, key="batch")
sc.pp.pca(adata)
adata

###############################################################################
# The first option is to prepare the problem in an arbitrary way and override
# the cost terms of the single OT problems after.

fgwp = FGWProblem(adata)
fgwp = fgwp.prepare(key="batch", joint_attr="X_pca", GW_x="X_pca", GW_y="X_pca")
fgwp

###############################################################################
# We can pass the custom cost matrices by accessing the
# :class:`moscot.problems.base.OTProblem`. The method
# :meth:`moscot.problems.base.OTProblem.set_xy` allows to pass a custom cost matrix
# for the linear term. :meth:`moscot.problems.base.OTProblem.set_x` allows to set
# a custom cost matrix for the quadratic term corresponding to the source distribution,
# while :meth:`moscot.problems.base.OTProblem.set_y` works analogously for the quadratic
# term in the target distribution.
#
# When using the above-mentioned methods we need to pass a :class:`pandas.DataFrame`
# to ensure that the order of the rows and columns of the cost matrix is correct.
# In the following we retrieve the cell names to construct the :class:`pandas.DataFrame`
# containing (random) custom cost matrices.

obs_names_0 = fgwp["0", "1"].adata_src.obs_names
obs_names_1 = fgwp["0", "1"].adata_tgt.obs_names

cost_linear_01 = np.abs(rng.normal(size=(len(obs_names_0), len(obs_names_1))))
cost_quad_0 = np.abs(rng.normal(size=(len(obs_names_0), len(obs_names_0))))
np.fill_diagonal(cost_quad_0, 0)
cost_quad_1 = np.abs(rng.normal(size=(len(obs_names_1), len(obs_names_1))))
np.fill_diagonal(cost_quad_1, 0)

cm_linear = pd.DataFrame(data=cost_linear_01, index=obs_names_0, columns=obs_names_1)
cm_quad_0 = pd.DataFrame(data=cost_quad_0, index=obs_names_0, columns=obs_names_0)
cm_quad_1 = pd.DataFrame(data=cost_quad_1, index=obs_names_1, columns=obs_names_1)

###############################################################################
# Now we can set the custom cost matrices:

fgwp["0", "1"].set_xy(cm_linear, tag="cost_matrix")
fgwp["0", "1"].set_x(cm_quad_0, tag="cost_matrix")
fgwp["0", "1"].set_y(cm_quad_1, tag="cost_matrix")

###############################################################################
# When solving the problem, the custom cost matrices will be used for the
# problem mapping from batch "0" to batch "1", while the problem mapping from batch "1" to
# batch "2" is still using the information passed in
# :meth:`moscot.problems.generic.FGWProblem.prepare`.

###############################################################################
# A second way to pass custom cost matrices is using :attr:`anndata.AnnData.obsp`.
# This is especially useful when saving and loading a model. On the other hand,
# it might be more difficult to store the cost matrix in the correct place in
# :attr:`anndata.AnnData.obsp`.
# In the following, we construct the attr:`anndata.AnnData.obsp` layer. When doing
# this, be sure that the order of the cost matrix entries are correct.
# In the following, we construct an :attr:`anndata.AnnData.obsp` layer containing
# custom cost matrices for both linear and quadratic terms for both OT problems,
# mapping from batch "0" to batch "1", and from batch "1" to batch "2".

obs_names_2 = fgwp["1", "2"].adata_tgt.obs_names

cost_linear_12 = np.abs(rng.normal(size=(len(obs_names_1), len(obs_names_2))))
cost_quad_2 = np.abs(rng.normal(size=(len(obs_names_2), len(obs_names_2))))
np.fill_diagonal(cost_quad_2, 0)

print(cost_quad_0.shape)
print(cost_quad_1.shape)
print(cost_quad_2.shape)
print(cost_linear_01.shape)
print(cost_linear_12.shape)

blocks = [
    [cost_quad_0, cost_linear_01, np.zeros((len(obs_names_0), len(obs_names_2)))],
    [np.zeros((len(obs_names_1), len(obs_names_0))), cost_quad_1, cost_linear_12],
    [np.zeros((len(obs_names_2), len(obs_names_0))), np.zeros((len(obs_names_2), len(obs_names_1))), cost_quad_2],
]

print(adata.shape)
adata.obsp["cost_matrices"] = np.block(blocks)

###############################################################################
# We need to specify where to fetch the custom cost matrices in the
# :meth:`moscot.problems.generic.FGWProblem.prepare` methods. If we want to only
# use the linear custom cost matrix, we need to modify the `joint_attr` as follows

joint_attr = {"key": "cost_matrices", "tag": "cost_matrix"}
fgwp = fgwp.prepare(key="batch", joint_attr=joint_attr, GW_x="X_pca", GW_y="X_pca")

###############################################################################
# If we want to use only quadratic custom cost matrices, we need to modify `GW_x`
# and `GW_y`.

GW_x = {"attr": "obsp", "key": "cost_matrices", "tag": "cost_matrix", "cost": "custom"}
GW_y = {"attr": "obsp", "key": "cost_matrices", "tag": "cost_matrix", "cost": "custom"}
fgwp = fgwp.prepare(key="batch", joint_attr="X_pca", GW_x=GW_x, GW_y=GW_y)

###############################################################################
# If we want to use custom cost matrices for all terms, we can do this the following
# way

fgwp = fgwp.prepare(key="batch", joint_attr=joint_attr, GW_x=GW_x, GW_y=GW_y)

###############################################################################
# TODO: link to notebook explaining tagged arrays
