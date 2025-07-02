from enum import Enum
import random
import Player
import Game
# --- = work in progress


# Build
def build_road(player, game):
    player.resource_cards['wood'] -= 1
    player.resource_cards['brick'] -= 1
    player.pieces['roads'] -= 1
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1] = player

def build_settlement(player, game):
    player.resource_cards['wood'] -= 1
    player.resource_cards['brick'] -= 1
    player.resource_cards['sheep'] -= 1
    player.resource_cards['wheat'] -= 1
    player.vic_points += 1
    player.pieces['settlements'] -= 1
    game.nodes[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1][1] = player
    game.nodes[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1][2] = 'settlement'

def build_city(player, game):
    player.resource_cards['wheat'] -= 2
    player.resource_cards['stone'] -= 3
    player.pieces['cities'] -= 1
    player.vic_points += 1
    game.nodes[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1][1] = player
    game.nodes[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1][2] = 'city'

# Buy development card
def buy_devcard(player, game):
    player.resource_cards['wheat'] -= 1
    player.resource_cards['sheep'] -= 1
    player.resource_cards['stone'] -= 1

    drawn_card = game.development_cards.pop()
    player.development_cards[drawn_card] += 1
    if drawn_card == 'vic_point':
        player.vic_points += 1

# Use development cards
def use_devcard_knight(player, game):
    player.development_cards['knight'] -= 1
    move_robber(player, game)

def use_devcard_buildroad(player, game):
    player.development_cards['build_road'] -= 1
    player.pieces['roads'] -= 2
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1] = player
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_EXTRA_ID) - 1][player.action_data.get(Player.ActionData.BUILD_EDGE_EXTRA_ID)][1] = player

def use_devcard_yearofplenty(player, game):
    player.development_cards['year_of_plenty'] -= 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(player, game):
    player.cards['monopoly'] -= 1
    for item in game.PLAYERS:
        if player != item and player != 'none':
            player.cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += item.cards[player.action_data.get(Player.ActionData.RESOURCE_GET)]
            item.cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] = 0

# Trade
def trade_bank(player, game):
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GIVE)] -= 4
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GIVE)] += 1

def trade_port(player, game):
    if player.action_data.get() == '3:1':
        player.resource_cards[player.action_data.get(Player.ActionData.SPECIAL_RESOURCE_GIVE)] -= 3
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
    else:
        player.resource_cards[player.action_data.get(Player.ActionData.PORT)] -= 2
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1

# Trade player ---


# Move robber
def move_robber(player, game):
    game.board[game.robber_id[0]][3] = False
    game.robber_id[0] = player.action_data.get(Player.ActionData.ROBBER_NODE_ID)
    game.board[game.robber_id[0]][3] = True

    target_player = player.action_data.get(Player.ActionData.ROBBER_PLAYER_TARGET)
    card_list = []
    
    for item in target_player.resource_cards:
        count = target_player.resource_cards.get(item)
        for i in range(count):
            card_list.append(item)
        target_player.resource_cards[item] = 0

    random.shuffle(card_list)
    player.resource_cards[card_list.pop()] += 1

    for item in card_list:
        target_player.resource_cards[item] += 1


# End turn ---


# Enumeration for all possible actions
class ActionType(Enum):
    # Buy actions
    BUILD_ROAD = "build_road"
    BUILD_SETTLEMENT = "build_settlement"
    BUILD_CITY = "build_city"
    BUY_DEV_CARD = "buy_devcard"

    # Use development card actions
    USE_KNIGHT = "use_devcard_knight"
    USE_BUILDROAD = "use_devcard_buildroad"
    USE_MONOPOLY = "use_devcard_monopoly"
    USE_YEAROFPLENTY = "use_devcard_yearofplenty"

    # Trade actions
    TRADE_BANK = "trade_bank"
    TRADE_PORT = "trade_port"
    TRADE_PLAYER = "trade_player"

    # Other actions
    MOVE_ROBBER = "move_robber"
    END_TURN = "end_turn"

# Defining enumerations to match the action methods
ACTIONS = {
    ActionType.BUILD_ROAD: build_road,
    ActionType.BUILD_SETTLEMENT: build_settlement,
    ActionType.BUILD_CITY: build_city,
    ActionType.BUY_DEV_CARD: buy_devcard,

    ActionType.USE_KNIGHT: use_devcard_knight,
    ActionType.USE_BUILDROAD: use_devcard_buildroad,
    ActionType.USE_MONOPOLY: use_devcard_monopoly,
    ActionType.USE_YEAROFPLENTY: use_devcard_yearofplenty,

    ActionType.TRADE_BANK: trade_bank,
    ActionType.TRADE_PORT: trade_port,
    # ActionType.TRADE_PLAYER: trade_player,

    ActionType.MOVE_ROBBER: move_robber,
    # ActionType.END_TURN: end_turn
}

# Method to execute general action
def execute_action(player, game, action_type):
    ACTIONS[action_type](player, game)




# Test functions
p1 = Player.Player(1)
game = Game.Game()

print(game.board[game.robber_id[0]][3])
