"""
A class representing an annealer that connects between the DFA module and the Simulated Annealing module
"""
# TODO: log run progress properly to file

from dfa import DFA
from relation import Relation
from copy import deepcopy
import random

class DFA_Annealer:
    def initial_hypothesis(self):
        """
        Returns a DFA that accepts all strings
        """
        states = {'q0', 'qF'}
        transitions = {'q0':{'0': 'q0', '1': 'q0', '#': 'qF'}}
        initial_state = 'q0'
        accepting_states = {'qF'}
        return DFA(states, transitions, initial_state, accepting_states)

    def compare_energy(self, dfa_a, dfa_b, positive_examples):
        metric_eval_a = self.metric_calc(dfa_a, positive_examples)
        print("Evaluation of suggested hypothesis =", metric_eval_a)
        metric_eval_b = self.metric_calc(dfa_b, positive_examples)
        print("Evaluation of current hypothesis =", metric_eval_b)
        return metric_eval_a - metric_eval_b

    def get_random_neighbor(self, dfa, data):
        """
        Chooses randomly a potential random neighbor and calls function try_option in order to check the validity of the chosen neighbor.
        If the random neighbor is not valid for some reason (as will be described in the try_option documantion),
        the function will re-choose a potential neighbor.
        Number of retries is limited to 20. Once a valid neighbor is found, it will be returned by the function.
        If by the end of 20 tries it doesn't find a valid neighbor, the current DFA is returned.
        """
        options = [self.__remove_final_state,
                   self.__switching_transitions,
                   self.__add_final_state,
                   self.__increase_accepting_from_left,
                   self.__increase_accepting_from_right,
                   self.__decrease_accepting_from_left,
                   self.__decrease_accepting_from_right,
                   self.__remove_transition_from_qn]
        for i in range(20): #Limited to 20 tries
            if i>=1:
                print("Raffles another hypothesis.")
            chosen_option = random.choice(options)
            result = self.__try_option(dfa, data, chosen_option)
            if result is not None:
                return result
        return dfa

    def metric_calc(self, dfa, positive_examples):
        len_g = len(dfa.encode())
        len_d_g = sum(len(dfa.encode_positive_example(string))
                      for string in positive_examples)
        return len_g + len_d_g

    '''
    Functions for getting random neighbor
    '''

    def __add_final_state(self, dfa):
        """
        Returns a DFA with one more state than the given DFA, which will be the new final state.
        The acceptance of the new final state will be identical to the acceptance of the previous final state

        @param DFA: DFA with n states
        @return new_DFA: DFA with n+1 states
        """
        # finding final state of given DFA
        prev_final_state = "q"+str(len(dfa.states) - 2)
        # finding final state of new DFA
        new_final_state = "q" + str(len(dfa.states) - 1)
        # Building new DFA
        new_states = dfa.states | {new_final_state} # Adding new final state
        new_transitions = deepcopy(dfa.transitions)
        if new_transitions['q0'].get('0') == 'q0':
            new_transitions[prev_final_state]['1'] = new_final_state
        else:
            new_transitions[prev_final_state]['0'] = new_final_state
        new_transitions[new_final_state] = {}
        new_transitions[new_final_state]['0'] = new_final_state
        new_transitions[new_final_state]['1'] = new_final_state
        # new final state will agree with acceptance of prev final state
        if dfa.reaches_qf(prev_final_state):
            new_transitions[new_final_state]['#'] = 'qF'
        new_accepting = deepcopy(dfa.accepting)
        new_dfa = DFA(new_states, new_transitions, 'q0', new_accepting)
        print(new_dfa)
        return new_dfa

    def __remove_final_state(self, dfa):
        """
        Returns a DFA with one less state than the given DFA
        @param DFA: DFA with n states
        @return new_DFA: DFA with n-1 states
        """
        # Getting q_n of given DFA
        prev_final_state = "q"+str(len(dfa.states) - 2)
        # Removing q_n from states
        new_states = dfa.states - {prev_final_state}
        # Getting q_n of new DFA
        new_final_state = "q"+str(len(new_states)-2)
        # Deleting transitions associated with q_n from transitions
        new_transitions = deepcopy(dfa.transitions)
        new_transitions[new_final_state]['0'] = new_final_state
        new_transitions[new_final_state]['1'] = new_final_state
        del new_transitions[prev_final_state]
        # Removing prev_final_state from accepting states of new dfa, if necessary
        new_accepting = dfa.accepting - {prev_final_state}

        new_dfa = DFA(new_states, new_transitions, 'q0' , new_accepting)
        print(new_dfa)
        return new_dfa

    def __switching_transitions(delf, dfa):
        new_initial = 'q0'
        new_states = deepcopy(dfa.states)
        new_accepting = deepcopy(dfa.accepting)
        # Changing transitions
        new_transitions = deepcopy(dfa.transitions)
        for state in new_states - {'qF'}:
            state_trans = new_transitions[state]
            state_trans['0'], state_trans['1'] = state_trans.get('1'), state_trans.get('0')
        new_dfa = DFA(new_states, new_transitions, new_initial, new_accepting)
        print(new_dfa)
        return new_dfa

    def __change_accepting_states(self, dfa, refer_state, size_change):
        """
        @param DFA: DFA with n states and x accpeting states
        @param refer_state: 'first_acc' for left-most accepting state or 'last_acc' for right-most accepting state.
        @param size_change: 'increase' or 'decrease'.
        @return new_DFA: DFA with change in accepting states per the other parameters.
        """
        accepting_ints = [int(state[1:]) for state in dfa.states if dfa.reaches_qf(state)]
        new_transitions = deepcopy(dfa.transitions)
        if refer_state == 'first_acc':
            min_acc_index = min(accepting_ints)
            if size_change == 'decrease' or min_acc_index == 0:
                new_transitions['q' + str(min_acc_index)].pop('#')
            else:
                new_transitions['q' + str(min_acc_index - 1)]['#'] = 'qF'
        else:
            max_acc_index = max(accepting_ints)
            if size_change == 'decrease' or max_acc_index == len(dfa.states) - 2:
                new_transitions['q' + str(max_acc_index)].pop('#')
            else:
                new_transitions['q' + str(max_acc_index + 1)]['#'] = 'qF'

        new_dfa = DFA(deepcopy(dfa.states), new_transitions, 'q0' , deepcopy(dfa.accepting))
        print(new_dfa)
        return new_dfa

    def __decrease_accepting_from_right(self, dfa):
        """
        @param DFA: DFA with n states and x accpeting states
        @return new_DFA: DFA with n and x+1 or x-1 accepting states, depanding on random choice
        """
        return self.__change_accepting_states(dfa, 'last_acc', 'decrease')

    def __decrease_accepting_from_left(self, dfa):
        """
        @param DFA: DFA with n states and x accpeting states
        @return new_DFA: DFA with n and x+1 or x-1 accepting states, depanding on random choice
        """
        return self.__change_accepting_states(dfa, 'first_acc', 'decrease')

    def __increase_accepting_from_right(self, dfa):
        """
        @param DFA: DFA with n states and x accpeting states
        @return new_DFA: DFA with n and x+1 or x-1 accepting states, depanding on random choice
        """
        return self.__change_accepting_states(dfa, 'last_acc', 'increase')

    def __increase_accepting_from_left(self, dfa):
        """
        @param DFA: DFA with n states and x accpeting states
        @return new_DFA: DFA with n and x+1 or x-1 accepting states, depanding on random choice
        """
        return self.__change_accepting_states(dfa, 'first_acc', 'increase')

    def __get_index_of_qn(self, dfa):
        return max(i for i in range(len(dfa.states)) if ('q%s' % i) in dfa.states)

    def __remove_transition_from_qn(self, dfa):
        new_transitions = deepcopy(dfa.transitions)
        last_state_index = self.__get_index_of_qn(dfa)
        if last_state_index is not None:
            last_state = 'q%s' % last_state_index
            if all(symbol not in dfa.transitions[last_state] for symbol in ['0', '1']):
                return deepcopy(dfa)
            if last_state_index == 0 or any(symbol not in dfa.transitions[last_state] for symbol in ['0', '1']):
                transition_to_remove = random.choice([symbol for symbol in dfa.transitions[last_state] if symbol != '#'])
            else:
                prev_state = 'q%s' % (last_state_index - 1)
                transition_to_remove = '0' if new_transitions[prev_state].get('0') == last_state else '1'
            new_transitions[last_state].pop(transition_to_remove)

        new_dfa = DFA(deepcopy(dfa.states), new_transitions, 'q0' , deepcopy(dfa.accepting))
        print(new_dfa)
        return new_dfa

    def __try_option(self, dfa, data, chosen_option):
        """
        Checks whether a chosen neighbor is valid, i.e:
        1) Accepts all pairs in data
        2) Doesn't reduce a state from an only-state machine

        If one of the above doesn't hold, None is returned. Otherwise, the chosen neighbor is returned.
        """
        print("Random neighbor to be checked:", chosen_option.__name__) 
        if len(dfa.states) <= 2 and chosen_option==self.__remove_final_state:
            print("Neigbor will cause dfa to have 0 states.")
            return None
        neighbor = chosen_option(dfa)
        # Check whether the neighbor dfa recognizes all couples in data
        # If not, return old dfa (i.e don't use neighbor). Otherwise, return neighbor
        for i,j in data:
            R = Relation(i,j)
            bin_rep = R.get_bianry_representation()
            if not neighbor.recognize(bin_rep):
                print("Neighbor didn't recognize one of the pairs in data: %s" % bin_rep)
                return None
        print("Neighbor is valid.")
        return neighbor



if __name__== "__main__":
    annealer = DFA_Annealer()
    print("AT LEAST 1")
    dfa_1 = annealer.initial_hypthesis_at_least()
    print("AT LEAST 2")
    dfa_2 = annealer.increasing_state(dfa_1)
    print("AT LEAST 3")
    dfa_3 = annealer.increasing_state(dfa_2)
    print("AT LEAST 2")
    dfa_4 = annealer.decreasing_state(dfa_3)
    print("AT MOST 1")
    dfa_5 = annealer.complement_relation(dfa_4)
    print("AT MOST NOT 1")
    dfa_8 = annealer.__switching_transitions(dfa_5)

    print("\nTesting find_hyp")
    DOGS = {'Rex', 'Spot', 'Bolt', 'Belka', 'Laika', 'Azit'}
    BROWN_ANIMALS = {'Belka', 'Spot', 'Azit', 'Mitzi'}
    SATELLITES =  {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Amos_5', 'Glonass'}
    LOW_EARTH_ORBIT = {'Yaogan', 'Ofeq_7', 'Ofeq_9', 'WorldView', 'Eros_B', 'Hubble'}
    data_at_least = [(DOGS, BROWN_ANIMALS) , (SATELLITES, LOW_EARTH_ORBIT)] 
    data_no = [(DOGS, LOW_EARTH_ORBIT) , (SATELLITES, BROWN_ANIMALS)]
    dfa_6 = annealer.find_initial_hypthesis(data_at_least)
    print('\n')
    dfa_7 = annealer.find_initial_hypthesis(data_no)

