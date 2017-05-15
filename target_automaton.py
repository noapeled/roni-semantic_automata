from dfa import DFA


class TargetAutomaton:
    @staticmethod
    def none():
        return DFA(
            states={'q0', 'qF'},
            transitions={'q0': {'0': 'q0', '#': 'qF'}},
            initial='q0',
            accepting='qF'
        )