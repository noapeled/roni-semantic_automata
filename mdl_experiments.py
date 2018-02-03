from collections import defaultdict

from dfa import DFA
from dfa_annealer import DFA_Annealer

ARBITRARY_REPETITIONS_ALL_OF_EXACTLY = 5


def create_dfa_all_of_the_exactly(n_values):
    states = ['qF'] + ['q' + str(i) for i in range(max(n_values) + 1)]
    transitions = defaultdict(dict)
    for i in range(max(n_values)):
        transitions['q' + str(i)]['1'] = 'q' + str(i + 1)
    for n in n_values:
        transitions['q' + str(n)]['#'] = 'qF'
    return DFA(
        states=states,
        transitions=transitions,
        initial='q0',
        accepting=['qF']
    )

def create_dfa_all():
    return DFA(
        states = ['q0', 'qF'],
        transitions={'q0': {'1': 'q0', '#': 'qF'}},
        initial='q0',
        accepting=['qF']
    )


def mdl_differences(min_n1, max_n1, min_n2, max_n2):
    results = {}
    for n1 in range(min_n1, max_n1 + 1):
        for n2 in range(n1, max_n2 + 1):
            results[n1, n2] = DFA_Annealer.compare_energy(
                create_dfa_all(),
                create_dfa_all_of_the_exactly((n1, n2)),
                sorted(['1' * n1, '1' * n2] * ARBITRARY_REPETITIONS_ALL_OF_EXACTLY)
            )
    return results

if __name__ == '__main__':
    print(mdl_differences(1, 3, 1, 3))