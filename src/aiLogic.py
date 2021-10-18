import numpy as np


class AIPlayer:
    def __init__(self, name: str, token: str, states=None):
        if states is None:
            states = list()
        self.states = states
        self.name = name
        self.token = token
        self.played_moves = list()

    def __add_state(self, parsed):
        possibilities = self.__get_available_moves(parsed)
        probabilities = self.__set_probabilities(possibilities)
        frequencies = self.__set_frequencies(possibilities)
        self.states.append(dict(state=parsed,
                                possibilities=possibilities,
                                probabilities=probabilities,
                                frequencies=frequencies))

    def __parse_state(self, state):
        parsed = [[None for y in range(len(state[0]))] for x in range(len(state))]

        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] is None:
                    continue
                elif state[i][j] == self.token:
                    parsed[i][j] = 1
                else:
                    parsed[i][j] = 0
        return parsed

    def get_move(self, state):
        parsed = self.__parse_state(state)
        move_vector = self.__get_state(parsed)

        random = np.random.uniform(0, 1)

        i = 0
        s = move_vector['probabilities'][i]

        while s < random:
            i += 1
            try:
                s = s + move_vector['probabilities'][i]
            except IndexError:
                i -= 1
                break
        self.played_moves.append(dict(move_vector=move_vector, played=i))
        return move_vector['possibilities'][i]

    def reinforce_probabilities(self):
        for state in self.states:
            s = np.sum(state['frequencies'])

            for i in range(len(state['probabilities'])):
                state['probabilities'][i] = (state['frequencies'][i]/s + state['probabilities'][i])/2
                state['frequencies'][i] = 1

    def reinforce_frequencies(self, score=0):
        for move in self.played_moves:
            played = move['played']

            if score != 0:
                move['move_vector']['frequencies'][played] += score
        self.played_moves = list()

    def __get_state(self, state):
        num_checked = 0
        broken = False

        for s in self.states:
            is_match = 0
            for i in range(len(state)):
                for j in range(len(state[0])):
                    if s['state'][i][j] != state[i][j]:
                        num_checked += 1
                        broken = True
                        break
                    else:
                        is_match += 1
                if broken:
                    broken = False
                    break

            if is_match == 9:
                return s

        if num_checked >= len(self.states):
            self.__add_state(state)
            return self.states[-1]

    @staticmethod
    def __get_available_moves(state):
        available = list()
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] is None:
                    available.append([i, j])

        return available

    @staticmethod
    def __set_probabilities(possibilities):
        probabilities = list()
        for i in range(1, len(possibilities) + 1):
            probabilities.append(np.divide(1, len(possibilities)))
        return probabilities

    @staticmethod
    def __set_frequencies(possibilities):
        frequencies = list()
        for i in range(len(possibilities)):
            frequencies.append(1)
        return frequencies
