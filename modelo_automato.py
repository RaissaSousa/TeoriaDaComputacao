automaton = {
    'initial': 'q1',
    'final': ['q3', 'q4'],
    'states': {
        'q1': {
            0: 'q2',
            1: 'q2',
            'e': 'q3'
        },
        'q2': {
            0: 'q4',
            1: 'q2',
            'e': 'q3',
        },
        'q3': {
            1: 'q4',
        }
    }
}