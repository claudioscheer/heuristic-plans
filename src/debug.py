# pylint: disable=import-error
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from pddl.heuristic import Heuristic
from pddl.pddl_parser import PDDLParser
from pddl.action import Action

# pylint: enable=import-error


class MaxHeuristic(Heuristic):
    def h(self, actions, state, goals):
        """
            I think that only positive preconditions/goals will not work well.
            I will need to merge positive and negative states.
            
            goals: positive goals and negative goals in a tuple.
        """
        fact_level = [state]
        action_level = []
        # I think that only positive preconditions will not work.
        positive_goals = goals[0]
        max_cost = 0

        # While the goals are not in the state, keep seeking.
        while not positive_goals.issubset(fact_level[max_cost]):
            # Get all actions applicable to the current state level.
            action_level.append(
                [a for a in actions if a.positive_preconditions.issubset(fact_level[max_cost])]
            )

            # The next state will contain all the actions from previous states, plus the effects actions when executing the actions applicable to the current state.
            fact_level.append(
                fact_level[max_cost].union(
                    [pre for a in action_level[max_cost] for pre in a.add_effects]
                )
            )

            # When the next state is the same as the current state, it means that there are no more effect actions that can reach the goal.
            if fact_level[max_cost + 1] == fact_level[max_cost]:
                return float("inf")
            max_cost += 1
        return max_cost


dwr = os.path.join(dir_path, "../examples/dwr/dwr.pddl")
pb1_dwr = os.path.join(dir_path, "../examples/dwr/pb1.pddl")


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


h = MaxHeuristic()
test_heuristic(dwr, pb1_dwr, h, 6)
