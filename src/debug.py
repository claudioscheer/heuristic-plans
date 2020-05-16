# pylint: disable=import-error
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from pddl.heuristic import Heuristic
from pddl.pddl_parser import PDDLParser
from pddl.action import Action

# pylint: enable=import-error


class AdditiveHeuristic(Heuristic):
    def h(self, actions, state, goals):
        reachable = state
        goals_missing = goals[0]
        goals_reached = None
        last_state = None
        add = 0
        costs = {p: 0 for p in state}
        while last_state != reachable:
            goals_reached = goals_missing.intersection(reachable)
            if goals_reached:
                add += sum(costs[g] for g in goals_reached)
                goals_missing = goals_missing.difference(goals_reached)
            if not goals_missing:
                return add

            last_state = reachable

            for action in actions:
                if action.positive_preconditions.issubset(last_state):
                    new_reachable = action.add_effects.difference(reachable)
                    for effect in new_reachable:
                        if effect in costs:
                            old_cost = costs[effect]
                            costs[effect] = min(
                                sum(costs[pre] for pre in action.positive_preconditions) + 1,
                                old_cost,
                            )
                            if costs[effect] != old_cost:
                                pass
                        else:
                            costs[effect] = (
                                sum(costs[pre] for pre in action.positive_preconditions) + 1
                            )
                    reachable = reachable.union(new_reachable)
        return float("inf")


tsp = os.path.join(dir_path, "../examples/tsp/tsp.pddl")
pb1_tsp = os.path.join(dir_path, "../examples/tsp/pb2.pddl")


def parse_domain_problem(domain, problem):
    parser = PDDLParser()
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    # Grounding process.
    actions = []
    for action in parser.actions:
        for act in action.groundify(parser.objects):
            actions.append(act)
    return parser, actions


def test_heuristic(domain, problem, h, expected):
    parser, actions = parse_domain_problem(domain, problem)
    v = h.h(actions, parser.state, (parser.positive_goals, parser.negative_goals))
    print(
        "Expected " + str(expected) + ", got:",
        str(v) + (". Correct!" if v == expected else ". False!"),
    )


h = AdditiveHeuristic()
test_heuristic(tsp, pb1_tsp, h, 8)
