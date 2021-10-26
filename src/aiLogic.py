import numpy as np


class AIPlayer:
    """
    The AI that is to learn how to play the game through guessing its way forward
    """
    def __init__(self, name: str, token: str, states=None):
        """
        Set up our beautiful AI boi
        :param name: name just for tracking
        :param token: what symbol we are playing with, will be used for parsing later
        :param states: do we already have some states and probabilities to work with?
        """
        if states is None:
            states = list()
        self.states = states
        self.name = name
        self.token = token
        self.played_moves = list()

    def __add_state(self, parsed):
        """
        Add a new game state to memory along with setting up its initial probabilities
        :param parsed: the parsed game state
        :return: nothing
        """
        possibilities = self.__get_available_moves(parsed)          # What moves are legal?
        probabilities = self.__set_probabilities(possibilities)     # What should their probabilities be?
        frequencies = self.__set_frequencies(possibilities)         # What should their frequencies be?
        self.states.append(dict(state=parsed,                       # Each state is a dictionary of these things!
                                possibilities=possibilities,
                                probabilities=probabilities,
                                frequencies=frequencies))

    def __parse_state(self, state):
        """
        Change the board with symbols into a board which is made of 0s and 1s so that we can learn regardless of which
        symbol we decide to give the AI, so long as we give 2 different symbols
        :param state: present unadulterated game state
        :return: the parsed state
        """
        parsed = [[None for y in range(len(state[0]))] for x in range(len(state))]      # Initial parsed board

        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] is None:             # If square not used do nothing
                    continue
                elif state[i][j] == self.token:     # If we have a token there, set to 1
                    parsed[i][j] = 1
                else:
                    parsed[i][j] = 0                # If someone else has a token there, set to 0
        return parsed

    def get_move(self, state):
        """
        What move is the AI going to play given the current board state?
        :param state: the current unadulterated board state
        :return: an index on the board
        """
        parsed = self.__parse_state(state)          # Set the parsed state
        move_vector = self.__get_state(parsed)      # Get the possibilities and probabilities for current game state

        random = np.random.uniform(0, 1)            # Generate a random choice0

        i = 0
        s = move_vector['probabilities'][i]

        while s < random:       # Check which move in the move_vector we are going to play
            i += 1
            try:
                s = s + move_vector['probabilities'][i]
            except IndexError:
                i -= 1
                break
        self.played_moves.append(dict(move_vector=move_vector, played=i))       # Add move to played moves for later
        return move_vector['possibilities'][i]

    def reinforce_probabilities(self):
        """Generate the new probabilties given the observed frequencies; this needs tweaking"""
        for state in self.states:
            s = np.sum(state['frequencies'])

            for i in range(len(state['probabilities'])):
                state['probabilities'][i] = (state['frequencies'][i]/s + state['probabilities'][i])/2   # Just average
                state['frequencies'][i] = 1

    def reinforce_frequencies(self, score=0):
        """
        Adding frequencies of wins for each move; the score reflects how much we want to reward a winning series of
        moves
        :param score: how much do we want to reward winning moves
        :return:
        """
        for move in self.played_moves:
            played = move['played']

            if score != 0:
                move['move_vector']['frequencies'][played] += score
        self.played_moves = list()

    def __get_state(self, state):
        """
        Gets the current state from the AIs played game states, adds one if not in the list.
        We need a much better structure for this because having a list is a nightmare; search tree?
        :param state:
        :return:
        """
        num_checked = 0
        broken = False

        for s in self.states:
            is_match = 0
            for i in range(len(state)):
                for j in range(len(state[0])):
                    if s['state'][i][j] != state[i][j]:     # Just garbage
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

        if num_checked >= len(self.states):     # Adding a new state and returning it
            self.__add_state(state)
            return self.states[-1]

    @staticmethod
    def __get_available_moves(state):
        """
        What positions are blank?
        :param state: a game state - either parsed or not
        :return: a list of available position indexes
        """
        available = list()
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] is None:
                    available.append([i, j])

        return available

    @staticmethod
    def __set_probabilities(possibilities):
        """
        Takes a possibility list and returns a uniform distribution for them
        :param possibilities: list of available moves
        :return: a list of probabilities
        """
        probabilities = list()
        for i in range(1, len(possibilities) + 1):
            probabilities.append(np.divide(1, len(possibilities)))
        return probabilities

    @staticmethod
    def __set_frequencies(possibilities):
        """
        Sets initial frequencies for a possibility vector, could have literally just use numpy
        :param possibilities: list of possible moves
        :return: a list of 1s
        """
        frequencies = list()
        for i in range(len(possibilities)):
            frequencies.append(1)
        return frequencies
