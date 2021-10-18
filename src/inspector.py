import pickle
from src import gameLogic, aiLogic


with open('ai_guts.pkl', 'rb') as inp:
    david_states = pickle.load(inp)
    leo_states = pickle.load(inp)
    print('Loaded')

game = gameLogic.TicTacToe()

david = aiLogic.AIPlayer(name='david', token='x', states=david_states)
leo = aiLogic.AIPlayer(name='leo', token='o', states=leo_states)

game.players.append(david)
game.players.append(leo)

game.play(p=True)
