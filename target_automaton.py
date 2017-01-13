from dfa import DFA


class TargetAutomaton:
    def __init__(self, positive_examples, annealer):
        self.positive_examples = positive_examples
        self.annealer = annealer

    def between_x_and_y(self, x, y):
        states = ['q%s' % i for i in range(y + 2)] + ['qF']

        transitions = {'q%s' % i: {'0': 'q%s' % i} for i in range(y + 2)}
        for i in range(y + 1):
            transitions['q%s' % i]['1'] = 'q%s' % (i + 1)
        for i in range(x, y + 1):
            transitions['q%s' % i]['#'] = 'qF'
        transitions['q%s' % (y + 1)]['1'] = 'q%s' % (y + 1)

        initial = 'q0'
        accepting = 'qF'

        g = DFA(states, transitions, initial, accepting)
        g.plot_transitions('Target Automaton for AT LEAST %s AND AT MOST %s ; E_%s' %
                           (x, y, self.annealer.metric_calc(g, self.positive_examples)))
        return g
