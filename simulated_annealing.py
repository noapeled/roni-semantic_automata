import datetime
import os

from relation import Relation
import random, math


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
        self.creation_time = datetime.datetime.now()
    
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
        directory = os.path.join('C:\\Users\\Noa Peled\\Desktop\\figures''',
                                 'figures_' + self.creation_time.strftime('%Y%m%d_%H%M%S'))
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
            energy = self.annealer.metric_calc(self.hyp, positive_examples)
            self.hyp.plot_transitions('hyp_%d ; E_%s' % (iter_counter, energy), directory)
            self.T *= alpha
        print("CHOSEN HYPOTHESIS:\n", self.hyp)

        return self.hyp, positive_examples, directory

    def logger(self, threshold, alpha, data, learner):
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
            
        return self.simulated_annealing(threshold, alpha)
