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
    
    def simulated_annealing(self, positive_examples, output_directory, threshold, alpha):
        """
        Performs simulated annealing.

        @param threshold: stop threshold for the temperature.
        @param alpha: The decrease factor of the temperature.
        @param output_directory: as the name implies.

        """
        iter_counter = 0 
        p = None
        # Initial hypothesis
        self.hyp.plot_transitions('hyp_%d ; E_%s' % (iter_counter, self.annealer.metric_calc(self.hyp, positive_examples)),
                                  output_directory)

        while self.T > threshold:
            iter_counter += 1 
            print ("# ITERATION COUNTER =" , iter_counter)
            print ("Current temperature:", self.T)
            H_tag = self.annealer.get_random_neighbor(self.hyp, self.data)
            delta = self.annealer.energy_difference_a_minus_b(H_tag, self.hyp, positive_examples)
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
            self.hyp.plot_transitions('hyp_%d ; E_%s' % (iter_counter, energy), output_directory)
            self.T *= alpha
        print("CHOSEN HYPOTHESIS:\n", self.hyp)

        return self.hyp, positive_examples

    def logger(self, positive_examples, output_directory, threshold, alpha):
        print("# APPLYING LEARNER ON THE FOLLOWING POSITIVE EXAMPLES: %s" % ','.join(positive_examples))
        print("\nInitial temperature:", self.T, ", Threshold:", threshold, ", Alpha:" , alpha)  
        print("\n# INITIAL HYPOTHESIS:\n", self.hyp)
        print("\n")
        return self.simulated_annealing(positive_examples, output_directory, threshold, alpha)
