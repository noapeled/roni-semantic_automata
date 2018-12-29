from dfa import DFA


def expected_final_hyp_none():
    return DFA(
        states={'q0', 'qF'},
        transitions={'q0': {'0': 'q0', '#': 'qF'}},
        initial='q0',
        accepting={'qF'}
    )


def expected_final_hyp_all():
    return DFA(
        states={'q0', 'qF'},
        transitions={'q0': {'1': 'q0', '#': 'qF'}},
        initial='q0',
        accepting={'qF'}
    )
