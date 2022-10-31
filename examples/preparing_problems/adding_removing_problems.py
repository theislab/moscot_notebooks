#!/usr/bin/env python
"""
Adding and removing problems
----------------------------
"""

###############################################################################
# This notebook demonstrates how to add or remove single problems.
#
# Adding a single problem can be useful for finetuning, and is sometimes needed
# for certain downstream functions, e.g. for 
# :meth:`moscot.problems.time.TemporalProblem.compute_interpolated_distance`.

from moscot.datasets import simulate_data
from moscot.problems.time import TemporalProblem

adata = simulate_data(n_distributions=4, key="time")
adata

###############################################################################
# Let's prepare and solve the problem.

tp = TemporalProblem(adata).prepare(time_key="day").solve(epsilon=1e-2)

for k in tp.problems.keys():
    print(f"key: {k}", f"solutions: {tp.problems[k].solution}")

###############################################################################
# Let's say we now want to solve one of the problems again,
# for examples because the solver did not converge, or we simply want to try
# different parameters. Let's say we want to try unbalancedness for the map between
# day 2 and day 3.
# Hence, we copy the single problem and solve it again.

key = (2, 3)
extracted_problem = tp.problems[key]
extracted_problem = extracted_problem.solve(epsilon=1e-2, tau_a=0.95, tau_b=0.95)
extracted_problem.solution

###############################################################################
# Now we are happy with the solution and add the extracted problem back to the
# :class:`moscot.problems.time.TemporalProblem` class.

tp = tp.add_problem((2, 3), extracted_problem, overwrite=True)
for k in tp.problems.keys():
    print(f"key: {k}", f"solutions: {tp.problems[k].solution}")

###############################################################################
# Similarly, we can remove a problem. For example, we realize that we are only
# interested in the first three time points. Hence, we remove the map from day
# 3 to day 4.
print(f"Problem before removal: {tp}.")
tp = tp.remove_problem((3,4))
print(f"Problem after removal: {tp}.")

###############################################################################
# In TODO link different_policies the use of different policies are explained.