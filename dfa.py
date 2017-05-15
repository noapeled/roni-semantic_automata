"""
A class representing a Deterministic Finite Automaton (DFA) over any finite alphabet.
"""
import datetime
import os

from graphviz import Digraph

class DFA:
    def __init__(self, states, transitions, initial, accepting):
        """
        Initializes a DFA instance.
        
        @param states: The names of the states of the DFA.
        @param transitions: the transitions of the DFA, as a dictionary where each key-value pair
                            is of the form state: {letter1: next state, ..., letterN: next state},
                            where letter1, ..., letterN are the letters of the alphabet.}
        @param initial: the name of the initial state.
        @param accepting: The names of the accepting states.
        """
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.accepting = accepting

    def __str__(self):
        to_string = ""
        to_string += "states: "
        to_string += str(self.states) + '\n'
        to_string += "accepting states: "
        if len(self.accepting) == 0:
            to_string += "empty set.\n"
        else:
            to_string += str(self.accepting) + '\n'
        to_string += "transitions: "
        to_string += str(self.transitions)
        return to_string

    def recognize(self, word):
        """
        Decides whether a given word is in the language of the DFA.

        @param word: The word to decide.
        @return: Whether or not the word is in the language of the DFA.
        """
        curr_state = self.initial
        for letter in word:
            try:
                curr_state = self.transitions[curr_state][letter]
            except KeyError:
                # If no transition is defined for the current state and letter, then the DFA rejects the word.
                return False
        return curr_state in self.accepting

    def plot_transitions(self, graph_name, directory):
        # Requires graphviz executables to be installed.
        dot = Digraph(comment=graph_name,
                      format='png',
                      name=graph_name,
                      directory=directory,
                      graph_attr={'rankdir': 'LR'})
        dot.node(graph_name, shape='square')

        for state in self.states:
            node_attributes = {'shape': 'doublecircle' if state in self.accepting else 'circle'}
            if state == self.initial:
                node_attributes['fontname'] = 'bold'
            dot.node(state, **node_attributes)

        for source_state, targets in self.transitions.items():
            for letter, target_state in targets.items():
                dot.edge(source_state, target_state, label=letter)

        dot.render(graph_name + '.gv')

    def reaches_qf(self, state):
        return bool(self.transitions.get(state, {}).get('#'))

    def encode(self):
        forward_transition_letter = '1' if self.transitions[self.initial].get('0') == self.initial else '0'
        encoding = forward_transition_letter
        current_state = self.initial
        for i in range(len(self.states)):
            if 'q%s' % i in self.states:
                encoding += '1' if self.reaches_qf(current_state) else '0'
        return encoding

    def encode_positive_example(self, word):
        def deterministic_transition(state):
            return len(self.transitions[state]) == 1

        def at_most_two_transitions(state):
            return len(self.transitions[curr_state]) <= 2

        encoding = ''
        curr_state = self.initial
        letter_encoding_in_state_which_reaches_qf = {'0': '00', '1': '10', '#': '11'}
        for letter in word:
            encoding += \
                '' if deterministic_transition(curr_state) else \
                (letter if at_most_two_transitions(curr_state) else
                 letter_encoding_in_state_which_reaches_qf[letter])
            curr_state = self.transitions[curr_state][letter]
        return encoding


if __name__ == '__main__':

    ### ---------------------------------------------------------------------------------------
    ### DFA for "All"
    states_all = {'q0', 'q1'}
    transitions_all = {
       'q0': {'0': 'q1', '1': 'q0'},
       'q1': {'0': 'q1', '1': 'q1'}
    }
    initial_all = 'q0'
    accepting_all = {'q0'}
    dfa_all = DFA(states_all, transitions_all, initial_all, accepting_all)

    dfa_all.plot_transitions('tmp_dfa', 'figures/tmp_dfa')
    
    assert dfa_all.recognize('') and dfa_all.recognize('1')
    assert not (dfa_all.recognize('0') or dfa_all.recognize('11110') or dfa_all.recognize('0'))
    dfa_nevery = dfa_all.get_complement()
    assert not (dfa_nevery.recognize('1') or dfa_nevery.recognize('11'))
    assert dfa_nevery.recognize('0') and dfa_nevery.recognize('10') and dfa_nevery.recognize('01')

    ### ---------------------------------------------------------------------------------------
    ### DFA for "At_least_1"
    states_at_least_1 = {'q0', 'q1'}
    transitions_at_least_1 = {
       'q0': {'0': 'q0', '1': 'q1'},
       'q1': {'0': 'q1', '1': 'q1'}
    }
    initial_at_least_1 = 'q0'
    accepting_at_least_1 = {'q1'}
    dfa_at_least_1 = DFA(states_at_least_1, transitions_at_least_1, initial_at_least_1, accepting_at_least_1)
    assert dfa_at_least_1.recognize('1000') and dfa_at_least_1.recognize('0001')
    assert not (dfa_at_least_1.recognize('000') or dfa_at_least_1.recognize('') or dfa_at_least_1.recognize('0'))
    dfa_no = dfa_at_least_1.get_complement()
    assert not (dfa_no.recognize('1') or dfa_no.recognize('11'))
    assert dfa_no.recognize('00') and dfa_no.recognize('0') and dfa_no.recognize('000')
