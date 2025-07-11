import Game
import Player
from Actions import *

# Initialize game
game = Game.Game()

# Initialize players
game.players[0] = Player.Player(game.players[0])
game.players[1] = Player.Player(game.players[1])
game.players[2] = Player.Player(game.players[2])
game.players[3] = Player.Player(game.players[3])

p1 = game.players[0]
p2 = game.players[1]
p3 = game.players[2]
p4 = game.players[3]

print( "Players initialized: ", game.players[0].id, game.players[1].id, game.players[2].id, game.players[3].id) #debug only

# Intialize turn variables
game_turn = 0
net_turn = 0

print("-----------------starting game-----------------") #debug only

# Start loop 
while net_turn < 2:
    if game_turn == 0:
        # Player 1's turn (start turns)
        action_list = search_action_start_turns(p1, game)

        # AI evaluation method goes here
        action_id = int

        execute_action(action_list, action_id, p1, game)

    elif game_turn == 1:
        # Player 2's turn (start turns)
        action_list = search_action_start_turns(p2, game)

        # AI evaluation method goes here
        action_id = int

        execute_action(action_list, action_id, p2, game)

    elif game_turn == 2:
        # Player 3's turn (start turns)
        action_list = search_action_start_turns(p3, game)

        # AI evaluation method goes here
        action_id = int

        execute_action(action_list, action_id, p3, game)

    elif game_turn == 3:
        # Player 4's turn (start turns)
        action_list = search_action_start_turns(p4, game)

        # AI evaluation method goes here
        action_id = int

        execute_action(action_list, action_id, p4, game)

    else:
        print("Error: Invalid game turn number.")
    
    
    # turn ticker
    print("End of start turn ", net_turn, " for player ", game_turn + 1)

    # --- snake-order advance ---
    if net_turn == 0:
        game_turn += 1
        if game_turn > 3:
            net_turn = 1
            game_turn = 3
    else:
        # descending phase: move 3→2→1→0
        game_turn -= 1
        if game_turn < 0:
            net_turn = 2
            game_turn = 0
            print("End of start turns, starting game turns now.") #debug only


# Game loop
while p1.vic_points < 10 and p2.vic_points < 10 and p3.vic_points < 10 and p4.vic_points < 10 and net_turn < 75 and net_turn >= 2:
    print("----------------------------------") #debug only
    if game_turn == 0:
        current_roll = game.roll_dice()
        if current_roll == "robber":
            # Robber turn code
            action_list = search_move_robber(p1, game)

            # AI evaluation method goes here
            action_id = int

            execute_action(action_list, action_id, p1, game)
            check_bonuses(p1, game)

            p1.turn = True
            while p1.turn == True:
                action_list = search_action(p1, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p1, game)
                check_bonuses(p1, game)
        else:
            valid_hexes = current_roll

            # Player 1's turn
            p1.turn = True
            while p1.turn == True:
                action_list = search_action(p1, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p1, game)
                check_bonuses(p1, game)

    elif game_turn == 1:
        current_roll = game.roll_dice()
        if current_roll == "robber":
            # Robber turn code
            action_list = search_move_robber(p2, game)

            # AI evaluation method goes here
            action_id = int

            execute_action(action_list, action_id, p2, game)
            check_bonuses(p1, game)

            p2.turn = True
            while p2.turn == True:
                action_list = search_action(p2, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p2, game)
                check_bonuses(p1, game)
        else:
            valid_hexes = current_roll
            # Player 2's turn 
            p2.turn = True
            while p2.turn == True:
                action_list = search_action(p2, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p2, game)
                check_bonuses(p1, game)

    elif game_turn == 2:
        current_roll = game.roll_dice()
        if current_roll == "robber":
            # Robber turn code
            action_list = search_move_robber(p3, game)

            # AI evaluation method goes here
            action_id = int

            execute_action(action_list, action_id, p3, game)
            check_bonuses(p1, game)

            p3.turn = True
            while p3.turn == True:
                action_list = search_action(p3, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p3, game)
                check_bonuses(p1, game)
        else:
            valid_hexes = current_roll

            # Player 3's turn
            p3.turn = True
            while p3.turn == True:
                action_list = search_action(p3, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p3, game)
                check_bonuses(p1, game)

    elif game_turn == 3:
        current_roll = game.roll_dice()
        if current_roll == "robber":
            # Robber turn code
            action_list = search_move_robber(p4, game)

            # AI evaluation method goes here
            action_id = int

            execute_action(action_list, action_id, p4, game)
            check_bonuses(p1, game)

            p4.turn = True
            while p4.turn == True:
                action_list = search_action(p4, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p4, game)
                check_bonuses(p1, game)
        else:
            valid_hexes = current_roll

            # Player 4's turn 
            p4.turn = True
            while p4.turn == True:
                action_list = search_action(p4, game)

                # AI evaluation method goes here
                action_id = int

                execute_action(action_list, action_id, p4, game)
                check_bonuses(p1, game)

    else:
        print("Error: Invalid game turn number. (start turns)")
    print(current_roll) #debug only   
    #turn ticker
    print("End of turn ", net_turn, " for player ", game_turn + 1)
    game_turn += 1
    if game_turn > 3:
        net_turn += 1
        game_turn = 0