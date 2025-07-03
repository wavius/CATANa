import Game
import Player

# Initialize game
game = Game.Game()

# Initialize players
game.players[0] = Player.Player(game.players[0])
game.players[1] = Player.Player(game.players[1])
game.players[2] = Player.Player(game.players[2])
game.players[3] = Player.Player(game.players[3])
print( "Players initialized: ", game.players[0].id, game.players[1].id, game.players[2].id, game.players[3].id) #debug only
# Intialize turn variables
game_turn = 0
net_turn = 0

print("-----------------starting game-----------------") #debug only
# Start loop 
while net_turn < 2:
    if game_turn == 0:
            # Player 1's turn (start turns)
        pass
    elif game_turn == 1:
            # Player 2's turn (start turns)
        pass
    elif game_turn == 2:
            # Player 3's turn (start turns)
        pass
    elif game_turn == 3:
        # Player 4's turn (start turns)
        pass
    else:
        print("Error: Invalid game turn number. (start turns)")
    
    #turn ticker
    print("End of start turn ", net_turn, " for player ", game_turn + 1)
    game_turn += 1
    if game_turn > 3:
        net_turn += 1
        game_turn = 0


# Game loop
while p1.vic_points < 10 and p2.vic_points < 10 and p3.vic_points < 10 and p4.vic_points < 10 and net_turn < 200 and net_turn >= 2:
    print("----------------------------------")
    if game_turn == 0:
        # Player 1's turn
        pass
    elif game_turn == 1:
        # Player 2's turn
        pass
    elif game_turn == 2:
        # Player 3's turn
        pass
    elif game_turn == 3:
        # Player 4's turn
        pass
    else:
        print("Error: Invalid game turn number.")
        

    #turn ticker
    print("End of turn ", net_turn, " for player ", game_turn + 1)
    game_turn += 1
    if game_turn > 3:
        net_turn += 1
        game_turn = 0