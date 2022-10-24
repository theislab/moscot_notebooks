#!/usr/bin/env python
"""
In this notebook, we will showcase how to use the `ProblemManager` capabilities in :class:`from moscot.problems.CompoundProblem`.

Let's load one temporal dataset, with 4 time points.
"""

from moscot.problems.time import TemporalProblem
from moscot.datasets import hspc

adata = hspc()

###############################################################################
# Let's prepare and solve the problem.

tp = TemporalProblem(adata).prepare(time_key="day").solve(epsilon=1e-2)

""
for k in tp.problems.keys():
    print(f"key: {k}", f"solutions: {tp.problems[k].solution}")

###############################################################################
# Let's say we now want to solve one of the problems again, because for example the solver did not converge, or we simply want to try it
# with a different set of parameters for the OT solver.
# What we need to do, is to copy the single problem and solve it again.

key = (2, 3)
new_problem = tp.problems[(2, 3)]
new_problem = new_problem.solve(epsilon=1e-2, tau_a=0.95)
new_problem.solution

###############################################################################
# For example, in this case we added a `tau` penalty for the unbalance case, resulting in a higher cost compared to the result above.
# Let's add this solution to the  :class:`moscot.problems.time.TemporalProblem` class from above.

tp = tp.add_problem((2, 3), new_problem, overwrite=True)
for k in tp.problems.keys():
    print(f"key: {k}", f"solutions: {tp.problems[k].solution}")
