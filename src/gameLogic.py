from src import aiLogic
import pickle


class TicTacToe:
    """
    The actual game of naughts and crosses, nothing really strange here, just modified slightly to incorporate the
    reinforcement directly.
    """
    def __init__(self):
        self.board = [[None for x in range(3)] for y in range(3)]       # Play space
        self.players = list()                                           # Who's playing
        self.num_wins = [0, 0, 0]                                       # A win record
        self.player_number = 0                                          # Who is playing

    def play(self, p: bool):
        """
        The central play loop
        :param p: do we print the board?
        :return: who won?
        """
        self.player_number = 0
        while True:
            cur_player = self.players[self.player_number]                       # Get current player
            player_move = cur_player.get_move(self.board)                       # Get player move
            self.board[player_move[0]][player_move[1]] = cur_player.token       # Set the move

            if p:                       # Do we print the board?
                for b in self.board:
                    print(b)
                print('\n')

            if self.player_win(player_move):                                        # Check if win
                cur_player.reinforce_frequencies(score=10)                          # Adding frequencies with some score
                self.players[(self.player_number + 1) % 2].reinforce_frequencies()  # Adding frequencies with 0 zero
                self.board = [[None for x in range(3)] for y in range(3)]           # Reset board
                self.num_wins[self.player_number] += 1                              # Record who won
                return cur_player.name
            elif self.tie():                                                                # Check for tie
                cur_player.reinforce_frequencies(score=1)                                   # Just say this wasn't bad
                self.players[(self.player_number + 1) % 2].reinforce_frequencies(score=1)
                self.board = [[None for x in range(3)] for y in range(3)]           # Reset board
                self.num_wins[2] += 1                                               # Record a tie
                return "no one!"
            else:                                                                   # Next player's turn
                self.player_number = (self.player_number + 1) % 2

    def player_win(self, last_played):
        """
        Did the last move win the game? Uses some sussy fucking logic that is not scalable at all, at all
        :param last_played: the index of the last played move
        :return: True if game was won, False otherwise
        """

        a = self.board[last_played[0]][0]
        b = self.board[0][last_played[1]]
        c = self.board[last_played[0]][last_played[1]]
        try:
            if a in self.board[last_played[0]][1] and a in self.board[last_played[0]][2]:
                return True
        except TypeError:
            pass
        try:
            if b in self.board[1][last_played[1]] and b in self.board[2][last_played[1]]:
                return True
        except TypeError:
            pass
        try:
            if c in self.board[0][0] and c in self.board[1][1] and c in self.board[2][2]:
                return True
        except TypeError:
            pass
        try:
            if c in self.board[0][2] and c in self.board[1][1] and c in self.board[2][0]:
                return True
        except TypeError:
            pass
        return False

    def tie(self):              # Check if board is full
        for b in self.board:
            if None in b:
                return False
        return True


game = TicTacToe()
david = aiLogic.AIPlayer('david', 'x')
leo = aiLogic.AIPlayer('leo', 'o')

game.players.append(david)
game.players.append(leo)

n = 5000                                # How many games do we play before we change the probabilities?

for i in range(150*n):                  # Scalar reflects how many total games we are playing
    game.play(p=False)
    if i % n == n - 1:
        david.reinforce_probabilities()         # Derive new probabilities
        leo.reinforce_probabilities()
        print('Reinforcing:' + str((i+1)/n))    # Which reinforce are we on
        print(game.num_wins)
        game.num_wins = [0, 0, 0]               # Just so we can see how the win-rates are progressing

for i in range(5):
    print('----- New Game -----\n')
    game.play(True)

print(david.states[0])
print('Game over!')
print(game.num_wins)
