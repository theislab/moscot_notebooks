#!/usr/bin/env python
"""
Plotting Sankey diagrams
------------------------
"""

###############################################################################
# In this notebook, we will showcase how to use :meth:`moscot.plotting.sankey`.
# We use the HSPC dataset to demonstrate the usage.

from moscot.datasets import hspc
from moscot.problems.time import TemporalProblem
import moscot.plotting as mpl

adata = hspc()

###############################################################################
# First, we need to prepare and solve the problem. Here, we set the `threshold`
# parameter to a relative high value to speed up convergence at the cost of
# lower quality.

tp = TemporalProblem(adata).prepare(time_key="day").solve(epsilon=1e-2, threshold=1e-2)

###############################################################################
# As for all plotting functionalities in moscot, we first call the method of
# the problem class, which stores the results of the computation in the
# :class:`anndata.AnnData` instance. Let us assume we want to plot the sankey diagram
# across all time points 2, 3, 4, and 7. Moreover, we want the Sankey diagram
# to visualize flows between cell types. In general, we can visualize the flow defined
# by any column in :attr:`anndata.AnnData.obs` via the `source_groups` parameter and
# the `target_groups` parameter, respectively. In this example, we are intereseted in
# descendants as opposed to ancestors, which is why we choose `forward` to be `True`.
# The information required to plot the Sankey diagram is provided in transition matrices,
# which we would obtain by `return_data` to `True`. Here, we are only interested in the
# visualization.

tp.sankey(source=2, target=7, source_groups="cell_type", target_groups="cell_type", forward=True, return_data=False)

###############################################################################
# Having called the `sankey` method of the problem instance, we now pass the result
# to the :mod:`moscot.plotting` module.
# Therefore, we can either pass the :class:`anndata.AnnData` instance or the problem
# instance. We can set the size of the figure via `dpi` and set a title via `title`.

mpl.sankey(tp, dpi=100, title="Cell type evolution over time")

###############################################################################
# By default, the result of the `sankey` method of a problem instance is saved
# `anndata.AnnData.uns['moscot_results']['sankey']['sankey'] and overrides
# this element every time the method is called. To prevent this, we can specify the parameter
# `key_added`, which we will do to store the results of the following use case.

###############################################################################
# We can also visualize flows of only a subset of categories of an :attr:`anndata.AnnData.obs` column
# by passing a dictionary for `source_groups` or `target_groups`.
new_key = "subset_sankey"
tp.sankey(
    source=2,
    target=7,
    source_groups={"cell_type": ["HSC", "MasP", "MkP"]},
    target_groups={"cell_type": ["HSC", "MasP", "MkP"]},
    forward=True,
    return_data=False,
    key_added=new_key,
)
mpl.sankey(tp, dpi=100, title="Cell type evolution over time", uns_key=new_key)
