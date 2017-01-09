from dfa_annealer import *
from dfa import DFA
from relation import Relation
import random, math
import shutil

class Simulated_annealing_learner:

    def __init__(self, initial_t, data, annealer):
        """
        @param data: The input data.
        @param initial_t: Initial value of temperature.
        """
        self.annealer = annealer
        self.T = initial_t
        self.data = data
        # self.hyp = self.annealer.find_initial_hypthesis(data)
        self.hyp = self.annealer.initial_hypothesis()
    
    def simulated_annealing(self, threshold, alpha):
        """
        Performs simulated annealing.

        @param threshold: stop threshold for the temperature.
        @param alpha: The decrease factor of the temperature.

        """
        iter_counter = 0 
        p = None
        positive_examples = [Relation(i,j).get_bianry_representation()
                             for i,j in self.data]
        while self.T > threshold:
            iter_counter += 1 
            print ("# ITERATION COUNTER =" , iter_counter)
            print ("Current temperature:", self.T)
            H_tag = self.annealer.get_random_neighbor(self.hyp, self.data)
            delta = self.annealer.compare_energy(H_tag, self.hyp, positive_examples)
            print("Delta =", delta)
            if delta < 0:
                p = 1
            else:
                p = math.exp(-delta/self.T)
            if p >= random.random():
                print("Changing hypothesis\n")
                self.hyp = H_tag
            else:
                print("Didn't change hypothesis\n")
            self.hyp.plot_transitions('hyp_%d' % iter_counter)
            self.T *= alpha
        print("CHOSEN HYPOTHESIS:\n", self.hyp)
        return self.hyp

    def logger(self, threshold, alpha):
        print("# APPLYING LEARNER ON THE FOLLOWING PAIRS OF SETS: ")
        pair_counter = 1
        for set_tuple in data:
            print("Pair no.", pair_counter)
            print(set_tuple)
            R = Relation(set_tuple[0], set_tuple[1])
            print("Binary representation of pair:", R.get_bianry_representation())
            pair_counter += 1
        
        print("\nInitial temperature:", self.T, ", Threshold:", threshold, ", Alpha:" , alpha)  
        print("\n# INITIAL HYPTHESIS: ")
        print(learner.hyp)
        print("\n")
            
        self.simulated_annealing(threshold, alpha)

if __name__== "__main__":
#    shutil.rmtree('./figures')
    
    def make_list_of_set_pairs(at_least, at_most, min_list_size, max_list_size, number_of_lists):
        lists = []
        for i in range(number_of_lists):
            list_size = random.choice(range(min_list_size, max_list_size))
            list_1 = set(range(list_size))
            list_2 = set(range(random.choice(range(at_least, min(at_most, list_size)))))
            lists.append((list_1, list_2))
        return lists
    
    data2 = make_list_of_set_pairs(at_least=3, at_most=6, min_list_size = 5, max_list_size = 61, number_of_lists = 50)

    def make_list_of_set_pairs_2(at_least_not, at_most_not, list_size):
        Q = frozenset(range(1, at_most_not * 2))
        return [(frozenset(random.sample(Q, len(Q) - random.randint(at_least_not, at_most_not))), Q) for i in range(list_size)]

    data3 = make_list_of_set_pairs_2(at_least_not=3, at_most_not=7, list_size=50)
    assert all(len(Q) - 10 <= len(P) <= len(Q) - 0 for P, Q in data3)

        
    DOGS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit'}
    BROWN_ANIMALS = {'Belka', 'Spot', 'Azit', 'Mitzi'}
    SATELLITES =  {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Amos_5', 'Glonass'}
    LOW_EARTH_ORBIT = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Hubble'}
    data = [(DOGS, BROWN_ANIMALS) , (SATELLITES, LOW_EARTH_ORBIT)]

    DOGS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit'}
    BROWN_ANIMALS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit', 'IKEA table', 'Humus'}
    SATELLITES =  {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B'}
    LOW_EARTH_ORBIT = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Hubble'}
    BOYS =  {'Tom', 'John', 'Max', 'Mark', 'Barak', 'Guy', 'Ted', 'Joey'}
    HAPPY = {'Linda', 'Mary', 'Tom', 'John', 'Max', 'Mark', 'Barak', 'Guy', 'Ted', 'Joey'}    
    data5 = [(DOGS, BROWN_ANIMALS) , (SATELLITES, LOW_EARTH_ORBIT), (BOYS, HAPPY)] #ALL


    GROUP_A = {'hello'}
    GROUP_B = {'hello'}
    GROUP_C = {'0', '2', '6', '17'}
    GROUP_D = {'0', '2', '6', '17'}
    data_1 = [(GROUP_A, GROUP_B) , (GROUP_C, GROUP_D)] #Minimal Quantifier: NONE

    CATS = {'Mitzi', 'Tuli', 'KitKat', 'Chat', 'Ears'}
    TWEET = {'Tweety', 'Zebra Finch', 'Cockatoo'}
    HAVE_ONE_SOUL = {'Rex', 'John'}
    data7= [(CATS, TWEET),(CATS, HAVE_ONE_SOUL), (CATS, DOGS)]

    
    data = data2

##    
##    print("# APPLYING LEARNER ON THE FOLLOWING PAIRS OF SETS: ")
##    pair_counter = 1
##    for set_tuple in data:
##        print("Pair no.", pair_counter)
##        print(set_tuple)
##        R = Relation(set_tuple[0], set_tuple[1])
##        print("Binary representation of pair:", R.get_bianry_representation())
##        pair_counter += 1

    annealer = DFA_Annealer()
    learner = Simulated_annealing_learner(1000, data, annealer)
    learner.logger(1.0, 0.96)

    
##    print("\n# INITIAL HYPTHESIS: ")
##    print(learner.hyp)
##    print("\n")

    
    #learner.simulated_annealing(0.4, 0.95)
    
