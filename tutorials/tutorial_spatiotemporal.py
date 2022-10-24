#!/usr/bin/env python
"""
Mapping across space and time
---
This tutorial the standard pipeline for performing mapping across time-pooints using spatial information
using the moscot solver :class:`moscot.solvers.spatio_temporal.SpatioTemporalProblem`.

We exemplify this using a subsample of spatiotemporal transcriptomics atlas of mouse organogenesis
using DNA nanoball-patterned arrays generated by :cite:`chen:22`.
"""

from moscot.problems.spatio_temporal import SpatioTemporalProblem
from moscot.datasets import mosta

###############################################################################
# We first load the data.
#
# The anndata object includes three time-points with embryo sections E9.5 E2S1, E10.5 E2S1, E11.5 E1S2.
# sThe :attr:`anndata.AnnData.X`
# # entry is based on reprocessing of the counts data consisting of :meth:`scanpy.pp.normalize_total` and
# # :meth:`scanpy.pp.log1p`
#
adata = mosta()

###############################################################################
# Now we can set a problem by defining:
#
# -`time_key` - Time point key in :attr:`anndata.AnnData.obs`.
# -`spatial_key` - Key in :attr:`anndata.AnnData.obsm` where spatial coordinates are stored.
# - `joint_attr` - The key for the joint space fot the mapping.
#       - If `None`, a value is computed based on `callback` using :attr:`anndata.AnnData.X`.
#           If callback is not specified PCA is computed.
#       - If `str`, it must refer to a key in :attr:`anndata.AnnData.obsm`.
#       - If `dict`, the dictionary stores `attr` (attribute of :class:`anndata.AnnData`) and `key`
#       (key of :class:`anndata.AnnData` ``['{attr}']``)
# - `callback` - Custom callback applied to each distribution as preprocessing step.
#
# ** For the purpose of iilustration we specifically specify the callback but this is not necessary.

stp = SpatioTemporalProblem(adata=adata).prepare(
                time_key="time",
                spatial_key="spatial",
                attr_joint=None,
                callback="local-pca",
            )

###############################################################################
# To solve the problem we call :class:`moscot.solvers.spatio_temporal.SpatioTemporalProblem.solve()` and pass:
#
# - `alpha` - Interpolation parameter between quadratic term (spatial coordinates) and linear term (PCA space).
# - `epsilon` - Entropic regularisation parameter.
#
# Here we solve the full-rank problem, for low-rank example see XX #TODO add refs

stp =  stp.solve(alpha=0.5, epsilon=1e-2)

###############################################################################
# Now we can visualize the results.
# We look at the transition matrix aggregated across cell-type's in the data.

import moscot.plotting as mpl

stp.cell_transition(
    source=9.5,
    target=10.5,
    source_groups="annotation",
    target_groups="annotation",
)
mpl.cell_transition(stp)








