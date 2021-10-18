from src import aiLogic
import pickle


class TicTacToe:
    def __init__(self):
        self.board = [[None for x in range(3)] for y in range(3)]
        self.players = list()
        self.num_wins = [0, 0, 0]
        self.player_number = 0

    def play(self, p: bool):
        self.player_number = 0
        while True:
            cur_player = self.players[self.player_number]
            player_move = cur_player.get_move(self.board)
            self.board[player_move[0]][player_move[1]] = cur_player.token

            if p:
                for b in self.board:
                    print(b)
                print('\n')

            if self.player_win(player_move):
                cur_player.reinforce_frequencies(score=3)
                self.players[(self.player_number + 1) % 2].reinforce_frequencies()
                self.board = [[None for x in range(3)] for y in range(3)]
                self.num_wins[self.player_number] += 1
                return cur_player.name
            elif self.tie():
                cur_player.reinforce_frequencies(score=1)
                self.players[(self.player_number + 1) % 2].reinforce_frequencies(score=1)
                self.board = [[None for x in range(3)] for y in range(3)]
                self.num_wins[2] += 1
                return "no one!"
            else:
                self.player_number = (self.player_number + 1) % 2

    def player_win(self, last_played):

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

    def tie(self):
        for b in self.board:
            if None in b:
                return False
        return True


game = TicTacToe()
david = aiLogic.AIPlayer('david', 'x')
leo = aiLogic.AIPlayer('leo', 'o')

game.players.append(david)
game.players.append(leo)

for i in range(50000):
    game.play(p=False)
    if i % 1000 == 999:
        david.reinforce_probabilities()
        leo.reinforce_probabilities()
        print('Reinforcing:' + str((i+1)/1000))

print('Game over!')
print(game.num_wins)

for i in range(5):
    game.play(True)
print('xd')
