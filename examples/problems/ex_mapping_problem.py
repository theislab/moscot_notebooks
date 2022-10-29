#!/usr/bin/env python
"""
Spatial mapping
---------------
"""

###############################################################################
# In this notebook, we will showcase how to use the
# :class:`moscot.problems.space.MappingProblem`.

from moscot.datasets import drosophila_sc, drosophila_sp
from moscot.problems.time import MappingProblem

adata_sc = drosophila_sc()
adata_sp = drosophila_sp()

###############################################################################
# Let's prepare and solve the problem.

mp = MappingProblem(adata_sc=adata_sc, adata_sp=adata_sp)
