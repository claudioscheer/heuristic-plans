from pddl.heuristic import Heuristic

class MaxHeuristic(Heuristic):
  def h(self, actions, state, goals):
    reachable = state |\label{line:reachable:h_max_python}|
    goals_missing = goals[0]
    max_cost = 0 |\label{line:max_cost_definition:h_max_python}|
    while not goals_missing.issubset(reachable): |\label{line:while:h_max_python}|
      last_state = frozenset( |\label{line:actions_applicable:h_max_python}|
        [a for a in actions if a.positive_preconditions.issubset(reachable)]
      )
      new_reachable = reachable.union([pre for a in last_state for pre in a.add_effects]) |\label{line:new_reachable:h_max_python}|
      if new_reachable == reachable: |\label{line:test_unreachable:h_max_python}|
        return float("inf")
      reachable = new_reachable
      max_cost += 1
    return max_cost