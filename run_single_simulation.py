import glob
import os
import random
import shutil

from dfa_annealer import DFA_Annealer
from simulated_annealing import Simulated_annealing_learner
from relation import Relation


def make_list_of_set_pairs_quantifier_EXACTLY(ns, min_sample_for_each_n, max_sample_for_each_n,
                                              min_zeros_per_positive_example, max_zeros_per_positive_example):
    pairs = []
    for n in ns:
        pairs.extend([(set(range(n + random.randint(min_zeros_per_positive_example, max_zeros_per_positive_example))),
                       set(range(n)))
                      for _ in range(random.randint(min_sample_for_each_n, max_sample_for_each_n))
                      ])
    return pairs


def simulate_EXACTLY(initial_temperature, threshold, alpha,
                     ns, min_sample_for_each_n, max_sample_for_each_n,
                     min_zeros_per_positive_example, max_zeros_per_positive_example):
    data = make_list_of_set_pairs_quantifier_EXACTLY(
            ns, min_sample_for_each_n, max_sample_for_each_n,
            min_zeros_per_positive_example, max_zeros_per_positive_example)
    return __simulate_with_data('EXACTLY',
                                dict(
                                        ns=ns, min_sample_for_each_n=min_sample_for_each_n,
                                        max_sample_for_each_n=max_sample_for_each_n,
                                        min_zeros_per_positive_example=min_zeros_per_positive_example,
                                        max_zeros_per_positive_example=max_zeros_per_positive_example),
                                data, initial_temperature, threshold, alpha)


def make_list_of_set_pairs_quantifier_ALL_OF_THE_EXACTLY(ns, min_sample_for_each_n, max_sample_for_each_n):
    pairs = []
    for n in ns:
        pairs.extend([(set(range(n)), set(range(n))) for _ in range(
                random.randint(min_sample_for_each_n, max_sample_for_each_n))])
    return pairs


def simulate_ALL_OF_THE_EXACTLY(initial_temperature, threshold, alpha, ns, min_sample_for_each_n,
                                max_sample_for_each_n):
    data = make_list_of_set_pairs_quantifier_ALL_OF_THE_EXACTLY(ns, min_sample_for_each_n, max_sample_for_each_n)
    return __simulate_with_data(data, initial_temperature, threshold, alpha)


def make_list_of_set_pairs_for_quantifier_all(min_set_size, max_set_size, number_of_pairs):
    lists = []
    for i in range(number_of_pairs):
        list_size = random.choice(range(min_set_size, max_set_size))
        lists.append((set(range(list_size)), set(range(list_size))))
    return lists


def make_list_of_set_pairs_for_quantifier_none(min_set_size, max_set_size, number_of_pairs):
    lists = []
    for i in range(number_of_pairs):
        list_size = random.choice(range(min_set_size, max_set_size))
        lists.append((set(range(list_size)), set()))
    return lists


def make_list_of_set_pairs_for_quantifier_between(at_least_ones, at_most_ones,
                                                  min_size_of_universe,
                                                  max_size_of_universe,
                                                  number_of_positive_examples,
                                                  add_examples_which_are_all_ones_of_these_lengths=[]):
    """
    Returns pairs, each of which will later be transformed into a binary string, which represents set membership.
    In each pair:
    1) First element is the universe: a set {0,...,M}, where M is a random number in [min_list_size, ..., max_list_size].
    2) Second element is a random subset {0,...,K}, where K is in [at_least, ..., at_most]. More precisely, K is in [at_least,..., M] if M < at_most.

    Thus generally speaking, the result is multiple instances of the generalized quantifier, each taken at random from a random size universe. Numeric example:
    at_least=3
    at_most=6
    min_list_size=20
    max_list_size=40
    number_of_lists=18
    We'll get 18 pairs. Example of one pair:
    (L1, L2) where
    L1 = {0, 1, 2, ..., 32}
    L2 = set(range(random.choice(range(3, min(7, 33))))) = set(range(random.choice(range(3, 7))) = set(range(22))

    :param at_least_ones:
    :param at_most_ones:
    :param min_size_of_universe:
    :param max_size_of_universe:
    :param number_of_positive_examples:
    :return:
    """
    if not all(at_least_ones <= length <= at_most_ones for length in add_examples_which_are_all_ones_of_these_lengths):
        raise ValueError('Length to add is out of allowed range')
    positive_examples_as_pairs_of_sets = []
    for i in range(number_of_positive_examples):
        universe_size = random.choice(range(min_size_of_universe, max_size_of_universe))
        univese_set = set(range(universe_size))
        subset_of_universe = set(range(random.choice(range(at_least_ones, min(at_most_ones + 1, universe_size)))))
        positive_examples_as_pairs_of_sets.append((univese_set, subset_of_universe))
    positive_examples_as_pairs_of_sets.extend(
            (set(range(length)), set(range(length))) for length in add_examples_which_are_all_ones_of_these_lengths)
    return positive_examples_as_pairs_of_sets


def simulate_whatever():
    DOGS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit'}
    BROWN_ANIMALS = {'Belka', 'Spot', 'Azit', 'Mitzi'}
    SATELLITES = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Amos_5', 'Glonass'}
    LOW_EARTH_ORBIT = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Hubble'}
    data = [(DOGS, BROWN_ANIMALS), (SATELLITES, LOW_EARTH_ORBIT)]

    DOGS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit'}
    BROWN_ANIMALS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit', 'IKEA table', 'Humus'}
    SATELLITES = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B'}
    LOW_EARTH_ORBIT = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Hubble'}
    BOYS = {'Tom', 'John', 'Max', 'Mark', 'Barak', 'Guy', 'Ted', 'Joey'}
    HAPPY = {'Linda', 'Mary', 'Tom', 'John', 'Max', 'Mark', 'Barak', 'Guy', 'Ted', 'Joey'}
    data5 = [(DOGS, BROWN_ANIMALS), (SATELLITES, LOW_EARTH_ORBIT), (BOYS, HAPPY)]  # ALL

    GROUP_A = {'hello'}
    GROUP_B = {'hello'}
    GROUP_C = {'0', '2', '6', '17'}
    GROUP_D = {'0', '2', '6', '17'}
    data_1 = [(GROUP_A, GROUP_B), (GROUP_C, GROUP_D)]  # Minimal Quantifier: NONE

    CATS = {'Mitzi', 'Tuli', 'KitKat', 'Chat', 'Ears'}
    TWEET = {'Tweety', 'Zebra Finch', 'Cockatoo'}
    HAVE_ONE_SOUL = {'Rex', 'John'}
    data7 = [(CATS, TWEET), (CATS, HAVE_ONE_SOUL), (CATS, DOGS)]


def simulate_data_3():
    def make_list_of_set_pairs_2(at_least_not, at_most_not, list_size):
        Q = frozenset(range(1, at_most_not * 2))
        return [(frozenset(random.sample(Q, len(Q) - random.randint(at_least_not, at_most_not))), Q) for i in
                range(list_size)]

    data3 = make_list_of_set_pairs_2(at_least_not=3, at_most_not=7, list_size=50)
    assert all(len(Q) - 10 <= len(P) <= len(Q) - 0 for P, Q in data3)


def create_output_directory(quantifier_type, additional_parameters_to_persist,
                            positive_examples, initial_temperature, threshold, alpha):
    folder_name = ('tempinit=%s_thres=%s_alpha=%s_' % (initial_temperature, threshold, alpha)) + \
        '_'.join('%s=%s' % (pname, pval) for pname, pval in additional_parameters_to_persist.items())
    output_directory = os.path.expanduser(
            os.path.join('~', 'Desktop', 'semantic_automata_simulations', quantifier_type, folder_name))
    os.makedirs(output_directory)
    with open(os.path.join(output_directory, 'parameters.csv'), 'w') as params_f:
        params_f.write('initial_temperature,%s\n' % initial_temperature)
        params_f.write('threshold,%s\n' % threshold)
        params_f.write('alpha,%s\n' % alpha)
        for param_name, param_value in additional_parameters_to_persist.items():
            params_f.write('%s,%s' % (param_name, param_value))
    with open(os.path.join(output_directory, 'positive_examples.txt'), 'w') as pos_f:
        pos_f.write('\n'.join(positive_examples))
    return output_directory


def cleanup_output_directory(output_directory):
    gv_directory = os.path.join(output_directory, 'gv')
    os.mkdir(gv_directory)
    for file in glob.glob(os.path.join(output_directory, '*.gv')):
        shutil.move(file, gv_directory)


def __simulate_with_data(quantifier_type, additional_parameters_to_persist,
                         data, initial_temperature, threshold, alpha):
    positive_examples = [Relation(i, j).get_bianry_representation() for i, j in data]
    output_directory = create_output_directory(quantifier_type, additional_parameters_to_persist,
                                               positive_examples, initial_temperature, threshold, alpha)
    annealer = DFA_Annealer()
    learner = Simulated_annealing_learner(initial_temperature, data, annealer)
    final_hyp = learner.logger(positive_examples, output_directory, threshold, alpha)
    cleanup_output_directory(output_directory)


def simulate_between_3_and_6_dynamic_set_size(initial_temperature, threshold, alpha, all_ones):
    data = make_list_of_set_pairs_for_quantifier_between(at_least_ones=3, at_most_ones=6, min_size_of_universe=5,
                                                         max_size_of_universe=61,
                                                         number_of_positive_examples=50,
                                                         add_examples_which_are_all_ones_of_these_lengths=all_ones)
    return __simulate_with_data(data, initial_temperature, threshold, alpha)


def simulate_BETWEEN_with_fixed_universe_size(initial_temperature, threshold, alpha, all_ones,
                                              at_least_ones, at_most_plus_1_ones,
                                              fixed_universe_size, number_of_positive_examples):
    data = make_list_of_set_pairs_for_quantifier_between(at_least_ones, at_most_plus_1_ones,
                                                         min_size_of_universe=fixed_universe_size,
                                                         max_size_of_universe=fixed_universe_size + 1,
                                                         number_of_positive_examples=number_of_positive_examples,
                                                         add_examples_which_are_all_ones_of_these_lengths=all_ones)
    return __simulate_with_data(data, initial_temperature, threshold, alpha)


def simulate_all(initial_temperature, threshold, alpha,
                 min_set_size, max_set_size, number_of_pairs):
    data = make_list_of_set_pairs_for_quantifier_all(min_set_size, max_set_size, number_of_pairs)
    return __simulate_with_data(data, initial_temperature, threshold, alpha)


def simulate_none(initial_temperature, threshold, alpha,
                  min_set_size, max_set_size, number_of_pairs):
    data = make_list_of_set_pairs_for_quantifier_none(
            min_set_size, max_set_size, number_of_pairs)
    return __simulate_with_data(data, initial_temperature, threshold, alpha)


def run_single_simulation(quantifier_type,
                          initial_temperature,
                          threshold,
                          alpha,
                          *args, **kwargs):
    if quantifier_type == 'EXACTLY':
        return simulate_EXACTLY(initial_temperature, threshold, alpha, *args, **kwargs)
    else:
        raise ValueError('Unknown quantifier type %s' % quantifier_type)


if __name__ == "__main__":
    #    shutil.rmtree('./figures')
    ##
    ##    print("# APPLYING LEARNER ON THE FOLLOWING PAIRS OF SETS: ")
    ##    pair_counter = 1
    ##    for set_tuple in data:
    ##        print("Pair no.", pair_counter)
    ##        print(set_tuple)
    ##        R = Relation(set_tuple[0], set_tuple[1])
    ##        print("Binary representation of pair:", R.get_bianry_representation())
    ##        pair_counter += 1

    initial_temperature = 2000
    threshold = 1.0
    alpha = 0.95
    number_of_pairs = 50
    # simulate_between_3_and_6(initial_temperature=2000, threshold=1.0, alpha=0.95, all_ones=[4])

    # simulate_all(initial_temperature=2000, threshold=1.0, alpha=0.95,
    #   max_set_size=61, number_of_pairs=50)

    # simulate_none(initial_temperature=2000, threshold=1.0, alpha=0.95,
    #               min_set_size=5, max_set_size=61, number_of_pairs=50)

    # simulate_BETWEEN_with_fixed_universe_size(initial_temperature, threshold, alpha,
    #                                           all_ones=[],
    #                                           at_least_ones=3, at_most_plus_1_ones=6, fixed_universe_size=10,
    #                                           number_of_positive_examples=number_of_pairs)

    # simulate_ALL_OF_THE_EXACTLY(initial_temperature, threshold, alpha,
    #                             ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10)

    # simulate_EXACTLY(initial_temperature, threshold, alpha,
    #                  ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10,
    #                  min_zeros_per_positive_example=0, max_zeros_per_positive_example=20)

    run_single_simulation('EXACTLY', initial_temperature, threshold, alpha,
                          ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10,
                          min_zeros_per_positive_example=0, max_zeros_per_positive_example=20)
