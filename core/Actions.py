from enum import Enum
import Player
import Game

# --- = work in progress

# Enumerate ActionData for autocomplete
class ActionData(Enum):
    BUILD_NODE_ID = "build_node_id"
    BUILD_EDGE_ID = "build_edge_id"

    RESOURCE_GIVE = "resource_give"
    RESOURCE_GET = "resource_get"
    RESOURCE_GET_EXTRA = "resource_get_extra"

    TARGET_PLAYER = "target_player"
    PORT = "port"
    SPECIAL_RESOURCE_GIVE = "special_resource_give"

    ROBBER_NODE_ID = "robber_node_id"

# Data for all possible actions ---
action_data = {
    # Building data
    ActionData.BUILD_NODE_ID: int,
    ActionData.BUILD_EDGE_ID: int,

    # Development card data
    ActionData.RESOURCE_GIVE: '',
    ActionData.RESOURCE_GET: '',
    ActionData.RESOURCE_GET_EXTRA: '',

    # Trade data
    ActionData.TARGET_PLAYER: '',
    ActionData.PORT: '',
    ActionData.SPECIAL_RESOURCE_GIVE: '',

    # Other data
    ActionData.ROBBER_NODE_ID: int
}


# Build
def build_road(player, game, action_data):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.pieces['roads'] -= 1
    game.edges[action_data.get(ActionData.BUILD_EDGE_ID) - 1][action_data.get(ActionData.BUILD_EDGE_ID)][1] = player

def build_settlement(player, game, action_data):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.cards['sheep'] -= 1
    player.cards['wheat'] -= 1
    player.pieces['settlements'] -= 1
    game.nodes[action_data.get(ActionData.BUILD_EDGE_ID) - 1][action_data.get(ActionData.BUILD_EDGE_ID)][1][1] = player
    game.nodes[action_data.get(ActionData.BUILD_EDGE_ID) - 1][action_data.get(ActionData.BUILD_EDGE_ID)][1][2] = 'settlement'

def build_city(player, game, action_data):
    player.cards['wheat'] -= 2
    player.cards['stone'] -= 3
    player.pieces['cities'] -= 1
    game.nodes[action_data.get(ActionData.BUILD_EDGE_ID) - 1][action_data.get(ActionData.BUILD_EDGE_ID)][1][1] = player
    game.nodes[action_data.get(ActionData.BUILD_EDGE_ID) - 1][action_data.get(ActionData.BUILD_EDGE_ID)][1][2] = 'city'


# Buy development card
def buy_devcard(player, game, action_data):
    player.cards['wheat'] -= 1
    player.cards['sheep'] -= 1
    player.cards['stone'] -= 1
    player.cards[game.development_cards.pop()] += 1


# Use development cards ---
def use_devcard_knight(player, game, action_data):
    player.cards['knight'] -= 1

# ---
def use_devcard_buildroad(player, game, action_data):
    player.cards['build_road'] -= 1

def use_devcard_yearofplenty(player, game, action_data):
    player.cards['year_of_plenty'] -= 1
    player.cards[action_data.get(ActionData.RESOURCE_GET)] += 1
    player.cards[action_data.get(ActionData.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(player, game, action_data):
    player.cards['monopoly'] -= 1
    for item in game.PLAYERS:
        if player != item and player != 'none':
            player.cards[action_data.get(ActionData.RESOURCE_GET)] += item.cards[action_data.get(ActionData.RESOURCE_GET)]
            item.cards[action_data.get(ActionData.RESOURCE_GET)] = 0


# Trade ---
def tradebank(player, game, action_data):
    player.cards[action_data.get()] -= 4
    player.cards[action_data.get()] += 1

def tradeport(player, game, action_data):
    if action_data.get() == '3:1':
        player.cards[action_data.get()] -= 3
        player.cards[action_data.get()] += 1
    else:
        player.cards[action_data.get()] -= 2
        player.cards[action_data.get()] += 1

# Trade player ---


# Move robber ---
# End turn ---




# Test functions
p1 = Player(1)
p1.cards['brick'] = 1
p1.cards['wood'] = 1

print(p1.cards['brick'])
print(p1.cards['wood'])

build_city(p1)

print(p1.cards['wheat'])
print(p1.cards['stone'])
