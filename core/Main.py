import Game
import Player
game = Game.Game()
p1 = Player.Player("Player 1")
p2 = Player.Player("Player 2")
p3 = Player.Player("Player 3")
p4 = Player.Player("Player 4")
game_turn = 0
net_turn = 0
print("-----------------starting game-----------------")

# Game loop
while p1.vic_points < 10 and p2.vic_points < 10 and p3.vic_points < 10 and p4.vic_points < 10 and net_turn < 200:
    print("----------------------------------")
    if net_turn < 2:
        print("start turn")
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
    elif game_turn == 0:
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