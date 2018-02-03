import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
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


def create_dfa_init_hyp():
    return DFA(
        states = ['q0', 'qF'],
        transitions={'q0': {'0': 'q0', '1': 'q0', '#': 'qF'}},
        initial='q0',
        accepting=['qF']
    )


# def compute_mdl_differences_all_vs_all_of_the_exactly(min_n, max_n):
#     results = {}
#     for n1 in range(min_n, max_n + 1):
#         for n2 in range(n1, max_n + 1):
#             results[n1, n2] = DFA_Annealer.compare_energy(
#                 create_dfa_all(),
#                 create_dfa_all_of_the_exactly((n1, n2)),
#                 sorted(['1' * n1, '1' * n2] * ARBITRARY_REPETITIONS_ALL_OF_EXACTLY)
#             )
#     return results

def compute_mdl_differences_init_hyp_vs_all_of_the_exactly(min_n, max_n):
    results = {}
    for n1 in range(min_n, max_n + 1):
        for n2 in range(n1, max_n + 1):
            results[n1, n2] = DFA_Annealer.compare_energy(
                create_dfa_init_hyp(),
                create_dfa_all_of_the_exactly((n1, n2)),
                sorted(['1' * n1, '1' * n2] * ARBITRARY_REPETITIONS_ALL_OF_EXACTLY)
            )
    return results


def plot_mdl_differences(image_file_name, max_n, matrix_as_dict):
    fig, ax = plt.subplots()
    mask = np.zeros((max_n + 1, max_n + 1))
    matrix_as_array = np.zeros((max_n + 1, max_n + 1))
    for k, v in matrix_as_dict.items():
        matrix_as_array[k[1], k[0]] = v
        if k[0] != k[1]:
            mask[k[0], k[1]] = True
    with sns.axes_style("white"):
        ax = sns.heatmap(matrix_as_array, mask=mask, square=True, cmap='inferno_r')
        ax.invert_yaxis()
        ax.set_xlim(xmin=1)
        ax.set_ylim(ymin=1)
        plt.savefig(image_file_name)


if __name__ == '__main__':
    # print('\n'.join(str(item) for item in sorted(compute_mdl_differences(1, 20).items(),
    #                                              key=lambda pair: pair[1])))
    plot_mdl_differences(
        'init_hyp_vs_all_of_the_exactly.png',
        20, compute_mdl_differences_init_hyp_vs_all_of_the_exactly(1, 20))