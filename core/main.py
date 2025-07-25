import game
from player import Player
from actions import *

# Initialize game
catan_game = game.Game()
# Initialize players
for name in catan_game.PLAYER_NAMES:
    catan_game.players.append(Player(name))


p1 = catan_game.players[0]
p2 = catan_game.players[1]
p3 = catan_game.players[2]
p4 = catan_game.players[3]


player = game.players[game.current_player_idx]
        


        
dict = {
    # Player state
    "player_state": [],
    # Pieces
    # Resource cards
    # Development cards
    # Victory points

    # Board state
    "board_state": [],
    # Robber
    # Dots, resources
    # Nodes, edges

    # Game state
    "turn_index": game.turn_number,
    "actions": search_action(player, game)
}
