import matplotlib
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from dfa import DFA
from dfa_annealer import DFA_Annealer
from relation import Relation
from run_single_simulation import make_list_of_set_pairs_quantifier_EXACTLY

ARBITRARY_REPETITIONS_ALL_OF_EXACTLY = 5


def get_positive_examples_for_exactly(n1, n2):
    return [Relation(i, j).get_binary_representation(shuffle=True) for i, j in
            make_list_of_set_pairs_quantifier_EXACTLY(
                ns=(n1, n2),
                min_sample_for_each_n=5,
                max_sample_for_each_n=10,
                min_zeros_per_positive_example=0,
                max_zeros_per_positive_example=20)]


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


# def create_dfa_all():
#     return DFA(
#         states = ['q0', 'qF'],
#         transitions={'q0': {'1': 'q0', '#': 'qF'}},
#         initial='q0',
#         accepting=['qF']
#     )


def create_dfa_init_hyp():
    return DFA(
        states = ['q0', 'qF'],
        transitions={'q0': {'0': 'q0', '1': 'q0', '#': 'qF'}},
        initial='q0',
        accepting=['qF']
    )


def create_dfa_exactly(n_values):
    states = ['qF'] + ['q' + str(i) for i in range(max(n_values) + 1)]
    transitions = defaultdict(dict)
    for i in range(max(n_values)):
        transitions['q' + str(i)]['0'] = 'q' + str(i)
        transitions['q' + str(i)]['1'] = 'q' + str(i + 1)
    transitions['q' + str(max(n_values))]['0'] = 'q' + str(max(n_values))
    for n in n_values:
        transitions['q' + str(n)]['#'] = 'qF'
    return DFA(
        states=states,
        transitions=transitions,
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

def compute_mdl_differences_init_hyp_vs_all_of_the_exactly(num_repetitions_of_each_positive_example, min_n, max_n):
    results = {}
    for n1 in range(min_n, max_n + 1):
        for n2 in range(n1, max_n + 1):
            results[n1, n2] = DFA_Annealer.compare_energy(
                create_dfa_init_hyp(),
                create_dfa_all_of_the_exactly((n1, n2)),
                sorted(['1' * n1 + '#', '1' * n2 + '#'] * num_repetitions_of_each_positive_example)
            )
    return results


def compute_mdl_differences_init_hyp_vs_exactly(min_n, max_n):
    results = {}
    for n1 in range(min_n, max_n + 1):
        for n2 in range(n1, max_n + 1):
            results[n1, n2] = DFA_Annealer.compare_energy(
                create_dfa_init_hyp(),
                create_dfa_exactly((n1, n2)),
                get_positive_examples_for_exactly(n1, n2)
            )
    return results


def plot_mdl_differences(title, image_file_name, max_n, matrix_as_dict):
    font = {'weight': 'bold', 'size': 15}
    matplotlib.rc('font', **font)
    mask = np.zeros((max_n + 1, max_n + 1))
    mask[:, 0] = True
    mask[0, :] = True
    matrix_as_array = np.zeros((max_n + 1, max_n + 1))
    for k, v in matrix_as_dict.items():
        matrix_as_array[k[1], k[0]] = v
        if k[0] != k[1]:
            mask[k[0], k[1]] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(20, 20))
        # cbar_ax = fig.add_axes([.905, .1, .05, .7])
        ax = sns.heatmap(matrix_as_array, ax=ax, mask=mask, square=True,
                         cmap='inferno_r',
                         # cbar_ax = cbar_ax, cbar=True
                         annot=True, fmt='.0f')
        ax.invert_yaxis()
        ax.set_xlim(xmin=1)
        ax.set_ylim(ymin=1)
        ax.set_title(title)
        ax.set_xlabel('$n_2$')
        ax.set_ylabel('$n_1$')
        plt.savefig(image_file_name)


if __name__ == '__main__':
    # print('\n'.join(str(item) for item in sorted(compute_mdl_differences(1, 20).items(),
    #                                              key=lambda pair: pair[1])))
    for num_repeat_pos_ex in range(1, 6):
        minimum_n, maximum_n = 1, 20
        plot_mdl_differences(
            'ALL_OF_THE_EXACTLY\n$E$(Initial DFA) - $E$(Target DFA)\n#Each Positive Example = %d' % num_repeat_pos_ex,
            'init_hyp_vs_all_of_the_exactly_min_%d_max_%d_rpt_%d.png' % (minimum_n, maximum_n, num_repeat_pos_ex),
            maximum_n,
            compute_mdl_differences_init_hyp_vs_all_of_the_exactly(num_repeat_pos_ex, minimum_n, maximum_n))

    for i in range(10):
        plot_mdl_differences(
            'EXACTLY\n$E$(Initial DFA) - $E$(Target DFA)',
            'init_hyp_vs_exactly_%d_min_%d_max_%d.png' % (i, minimum_n, maximum_n),
            maximum_n,
            compute_mdl_differences_init_hyp_vs_exactly(minimum_n, maximum_n))
