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
        reachable = [state]
        goals_missing = goals[0]
        goals_reached = None
        last_state = [frozenset()]
        add = 0
        level = 0
        while last_state[level] != reachable[level]:
            goals_reached = goals_missing.intersection(reachable[level])
            if len(goals_reached) > 0:
                add += level * len(goals_reached)
                goals_missing = goals_missing.difference(goals_reached)
            if len(goals_missing) == 0:
                return add

            last_state.append(
                frozenset(
                    [a for a in actions if a.positive_preconditions.issubset(reachable[level])]
                )
            )
            reachable.append(
                reachable[level].union([pre for a in last_state[level] for pre in a.add_effects])
            )
            level += 1
        return float("inf")


tsp = os.path.join(dir_path, "../examples/tsp/tsp.pddl")
pb1_tsp = os.path.join(dir_path, "../examples/tsp/pb1.pddl")


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
