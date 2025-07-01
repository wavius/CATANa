import Player

# --- = work in progress

# Data for all possible actions ---
action_data = {
    # Player data
    "player_names": ['p1', 'p2', 'p3', 'p4'],

    # Building data
    "build_node": int,
    "build_edge": int,

    # Development card data
    "resource_give": '',
    "resource_get": '',
    "resource_get_extra": '',

    # Trade data
    "target_player": '',
    "port": '',
    "3:1_resource_give": '',

    # Other data
    "robber_node": int
}


# Build ---
def build_road(player, board, action_data):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.pieces['roads'] -= 1

# ---
def build_settlement(player, board, action_data):
    player.cards['wood'] -= 1
    player.cards['brick'] -= 1
    player.cards['sheep'] -= 1
    player.cards['wheat'] -= 1
    player.pieces['settlements'] -= 1

# ---
def build_city(player, board, action_data):
    player.cards['wheat'] -= 2
    player.cards['stone'] -= 3
    player.pieces['cities'] -= 1


# Buy development card ---
def buy_devcard(player, board, action_data):
    player.cards['wheat'] -= 1
    player.cards['sheep'] -= 1
    player.cards['stone'] -= 1


# Use development cards ---
def use_devcard_knight(player, board, action_data):
    player.cards['knight'] -= 1

# ---
def use_devcard_buildroad(player, board, action_data):
    player.cards['build_road'] -= 1

def use_devcard_yearofplenty(player, board, action_data):
    player.cards['year_of_plenty'] -= 1
    player.cards[action_data.get('resource_get')] += 1
    player.cards[action_data.get('resource_get_extra')] += 1

def use_devcard_monopoly(player, board, action_data):
    player.cards['monopoly'] -= 1
    for item in action_data.get('player_names'):
        if player != item:
            player.cards[action_data.get('resource_get')] += item.cards[action_data.get('resource_get')]
            item.cards[action_data.get('resource_get')] = 0


# Trade ---
def tradebank(player, board, action_data):
    player.cards[action_data.get('resource_give')] -= 4
    player.cards[action_data.get('resource_get')] += 1

def tradeport(player, board, action_data):
    if action_data.get('port') == '3:1':
        player.cards[action_data.get('3:1_resource_give')] -= 3
        player.cards[action_data] += 1
    else:
        player.cards[action_data.get('port')] -= 2
        player.cards[action_data.get('resource_get')] += 1

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
