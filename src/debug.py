# pylint: disable=import-error
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from pddl.heuristic import Heuristic
from pddl.pddl_parser import PDDLParser
from pddl.action import Action

# pylint: enable=import-error


class FastForwardHeuristic(Heuristic):
    def build_bs_table(self, actions, initial_state, goal):
        self.empty_action = Action(
            "nop", frozenset(), frozenset(), frozenset(), frozenset(), frozenset()
        )
        self.bs_table = dict()
        return self.update_bs_table(actions, initial_state, goal)

    def update_bs_table(self, actions, initial_state, goal):
        positive_g, negative_g = goal
        if not positive_g:
            return 0
        reachable = set(initial_state)
        missing_positive_g = set(positive_g)
        last_state = None
        # Everything in the initial state costs 0.
        t_add = {p: 0 for p in initial_state}
        add = 0
        while last_state != reachable:
            g_reached = missing_positive_g.intersection(reachable)
            if g_reached:
                add += sum(t_add[g] for g in g_reached)
                missing_positive_g -= g_reached
                if not missing_positive_g:
                    return add
            last_state = set(reachable)
            for a in actions:
                if a.positive_preconditions <= last_state:
                    new_reachable = a.add_effects - reachable
                    for eff in new_reachable:
                        if eff in t_add:
                            old_t_add = t_add[eff]
                            t_add[eff] = min(
                                sum(t_add[pre] for pre in a.positive_preconditions) + 1, t_add[eff]
                            )
                            if t_add[eff] != old_t_add:
                                # best supporter changed
                                self.bs_table[eff] = a
                        else:
                            t_add[eff] = sum(t_add[pre] for pre in a.positive_preconditions) + 1
                            self.bs_table[eff] = a
                    reachable.update(new_reachable)
        return float("inf")

    def best_supporter(self, actions, initial_state, g):
        if g not in self.bs_table.keys():
            return self.empty_action
        return self.bs_table[g]

    def h(self, actions, initial_state, goal):
        # Build best supporter (I've done this for you).

        h_add = self.build_bs_table(actions, initial_state, goal)
        if h_add == 0:
            return 0


        return len([])


tsp = os.path.join(dir_path, "../examples/tsp/tsp.pddl")
pb1_tsp = os.path.join(dir_path, "../examples/tsp/pb1.pddl")
pb2_tsp = os.path.join(dir_path, "../examples/tsp/pb2.pddl")

dwr = os.path.join(dir_path, "../examples/dwr/dwr.pddl")
pb1_dwr = os.path.join(dir_path, "../examples/dwr/pb1.pddl")
pb2_dwr = os.path.join(dir_path, "../examples/dwr/pb2.pddl")

dompteur = os.path.join(dir_path, "../examples/dompteur/dompteur.pddl")
pb1_dompteur = os.path.join(dir_path, "../examples/dompteur/pb1.pddl")


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


h = FastForwardHeuristic()
test_heuristic(dwr, pb1_dwr, h, 16)
test_heuristic(dwr, pb2_dwr, h, 0)
test_heuristic(tsp, pb1_tsp, h, 5)
test_heuristic(tsp, pb2_tsp, h, 5)
test_heuristic(dompteur, pb1_dompteur, h, 2)
