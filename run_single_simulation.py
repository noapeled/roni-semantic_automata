import glob
import os
import random
import shutil

from dfa_annealer import DFA_Annealer
from simulated_annealing import Simulated_annealing_learner


def make_list_of_set_pairs(at_least, at_most, min_list_size, max_list_size, number_of_lists):
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

    :param at_least:
    :param at_most:
    :param min_list_size:
    :param max_list_size:
    :param number_of_lists:
    :return:
    """
    lists = []
    for i in range(number_of_lists):
        list_size = random.choice(range(min_list_size, max_list_size))
        list_1 = set(range(list_size))
        list_2 = set(range(random.choice(range(at_least, min(at_most + 1, list_size)))))
        lists.append((list_1, list_2))
    return lists


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


def simulate_between_3_and_6():
    data = make_list_of_set_pairs(at_least=3, at_most=6, min_list_size=5, max_list_size=61, number_of_lists=50)
    annealer = DFA_Annealer()
    initial_temperature = 2000
    threshold = 1.0
    alpha = 0.95

    learner = Simulated_annealing_learner(initial_temperature, data, annealer)
    final_hyp, positive_examples, directory = learner.logger(threshold, alpha, data, learner)

    with open(os.path.join(directory, 'parameters.csv'), 'w') as params_f:
        params_f.write('initial_temperature,%s\n' % initial_temperature)
        params_f.write('threshold,%s\n' % threshold)
        params_f.write('alpha,%s\n' % alpha)

    # target = TargetAutomaton(positive_examples, annealer, directory)
    # target.between_x_and_y(3, 6)

    with open(os.path.join(directory, 'positive_examples.txt'), 'w') as pos_f:
        pos_f.write('\n'.join(positive_examples))

    gv_directory = os.path.join(directory, 'gv')
    os.mkdir(gv_directory)
    for file in glob.glob(os.path.join(directory, '*.gv')):
        shutil.move(file, gv_directory)

    ##    print("\n# INITIAL HYPTHESIS: ")
    ##    print(learner.hyp)
    ##    print("\n")


    # learner.simulated_annealing(0.4, 0.95)


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
    simulate_between_3_and_6()