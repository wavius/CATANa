from enum import Enum
from Player import Player
from Game import Game
# --- = work in progress


# Build
def build_road(player, game):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.pieces['roads'] -= 1
    game.edges[player.action_data.get(ActionType.BUILD_EDGE_ID) - 1][player.action_data.get(ActionType.BUILD_EDGE_ID)][1] = player

def build_settlement(player, game):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.cards['sheep'] -= 1
    player.cards['wheat'] -= 1
    player.pieces['settlements'] -= 1
    game.nodes[player.action_data.get(ActionType.BUILD_EDGE_ID) - 1][player.action_data.get(ActionType.BUILD_EDGE_ID)][1][1] = player
    game.nodes[player.action_data.get(ActionType.BUILD_EDGE_ID) - 1][player.action_data.get(ActionType.BUILD_EDGE_ID)][1][2] = 'settlement'

def build_city(player, game):
    player.cards['wheat'] -= 2
    player.cards['stone'] -= 3
    player.pieces['cities'] -= 1
    game.nodes[player.action_data.get(ActionType.BUILD_EDGE_ID) - 1][player.action_data.get(ActionType.BUILD_EDGE_ID)][1][1] = player
    game.nodes[player.action_data.get(ActionType.BUILD_EDGE_ID) - 1][player.action_data.get(ActionType.BUILD_EDGE_ID)][1][2] = 'city'


# Buy development card
def buy_devcard(player, game):
    player.cards['wheat'] -= 1
    player.cards['sheep'] -= 1
    player.cards['stone'] -= 1
    player.cards[game.development_cards.pop()] += 1


# Use development cards ---
def use_devcard_knight(player, game):
    player.cards['knight'] -= 1

# ---
def use_devcard_buildroad(player, game):
    player.cards['build_road'] -= 1

def use_devcard_yearofplenty(player, game):
    player.cards['year_of_plenty'] -= 1
    player.cards[player.action_data.get(ActionType.RESOURCE_GET)] += 1
    player.cards[player.action_data.get(ActionType.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(player, game):
    player.cards['monopoly'] -= 1
    for item in game.PLAYERS:
        if player != item and player != 'none':
            player.cards[player.action_data.get(ActionType.RESOURCE_GET)] += item.cards[player.action_data.get(ActionType.RESOURCE_GET)]
            item.cards[player.action_data.get(ActionType.RESOURCE_GET)] = 0


# Trade ---
def tradebank(player, game):
    player.cards[player.action_data.get()] -= 4
    player.cards[player.action_data.get()] += 1

def tradeport(player, game):
    if player.action_data.get() == '3:1':
        player.cards[player.action_data.get()] -= 3
        player.cards[player.action_data.get()] += 1
    else:
        player.cards[player.action_data.get()] -= 2
        player.cards[player.action_data.get()] += 1

# Trade player ---


# Move robber ---
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

    ActionType.TRADE_BANK: tradebank,
    ActionType.TRADE_PORT: tradeport,
    # ActionType.TRADE_PLAYER: tradeplayer,

    # ActionType.MOVE_ROBBER: moverobber,
    # ActionType.END_TURN: end_turn
}


# Method to execute general action
def execute_action(player, board, action_data, action_type):
    ACTIONS[action_type](player, board, action_data)


# Test functions
p1 = Player(1)
game = Game()
p1.cards['brick'] = 1
p1.cards['wood'] = 1
print(p1.cards['brick'])
print(p1.cards['wood'])

build_city(p1, game)

print(p1.cards['wheat'])
print(p1.cards['stone'])
