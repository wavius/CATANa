from enum import Enum
from dataclasses import dataclass
import random
import Player
import Game
# --- = work in progress


# ------------------------------
# Execute action methods
# ------------------------------

"Any data needed to execute a move is first updated in action_data dict in Player class"
"Execute action methods are then called"

# Build
def build_road(player, game):
    player.resource_cards['wood'] -= 1
    player.resource_cards['brick'] -= 1
    game.resource_cards['wood'] += 1
    game.resource_cards['brick'] += 1

    player.pieces['roads'] -= 1
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1] = player.id

def build_settlement(player, game):
    player.resource_cards['wood'] -= 1
    player.resource_cards['brick'] -= 1
    player.resource_cards['sheep'] -= 1
    player.resource_cards['wheat'] -= 1
    game.resource_cards['wood'] += 1
    game.resource_cards['brick'] += 1
    game.resource_cards['sheep'] += 1
    game.resource_cards['wheat'] += 1

    player.vic_points += 1
    player.pieces['settlements'] -= 1
    game.nodes[player.action_data.get(Player.ActionData.BUILD_NODE_ID)][1][1] = player.id
    game.nodes[player.action_data.get(Player.ActionData.BUILD_NODE_ID)][1][2] = 'settlement'

def build_city(player, game):
    player.resource_cards['wheat'] -= 2
    player.resource_cards['stone'] -= 3
    game.resource_cards['wheat'] += 2
    game.resource_cards['stone'] += 3

    player.pieces['cities'] -= 1
    player.vic_points += 1
    game.nodes[player.action_data.get(Player.ActionData.BUILD_NODE_ID)][1][1] = player.id
    game.nodes[player.action_data.get(Player.ActionData.BUILD_NODE_ID)][1][2] = 'city'

# Buy development card
def buy_devcard(player, game):
    player.resource_cards['wheat'] -= 1
    player.resource_cards['sheep'] -= 1
    player.resource_cards['stone'] -= 1
    game.resource_cards['wheat'] += 1
    game.resource_cards['sheep'] += 1
    game.resource_cards['stone'] += 1

    drawn_card = game.development_cards.pop()
    player.development_cards[drawn_card] += 1
    if drawn_card == 'vic_point':
        player.vic_points += 1

# Use development cards
##
def use_devcard_knight(player, game):
    player.development_cards['knight'] -= 1
    move_robber(player, game)

def use_devcard_buildroad(player, game):
    player.development_cards['build_road'] -= 1
    player.pieces['roads'] -= 2
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_ID)][1] = player.id
    game.edges[player.action_data.get(Player.ActionData.BUILD_EDGE_EXTRA_ID)][1] = player.id

def use_devcard_yearofplenty(player, game):
    player.development_cards['year_of_plenty'] -= 1

    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] -= 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET_EXTRA)] -= 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(player, game):
    player.development_cards['monopoly'] -= 1
    for item in game.players:
        if item != player and item != 'none':
            player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += item.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)]
            item.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] = 0

# Trade
def trade_bank(player, game):
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GIVE)] -= 4
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GIVE)] += 4
    player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] -= 1

def trade_port(player, game):
    if player.action_data.get(Player.ActionData.PORT) == '3:1':
        player.resource_cards[player.action_data.get(Player.ActionData.SPECIAL_RESOURCE_GIVE)] -= 3
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
        player.resource_cards[player.action_data.get(Player.ActionData.SPECIAL_RESOURCE_GIVE)] += 3
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] -= 1
    else:
        player.resource_cards[player.action_data.get(Player.ActionData.PORT)] -= 2
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] += 1
        player.resource_cards[player.action_data.get(Player.ActionData.PORT)] += 2
        player.resource_cards[player.action_data.get(Player.ActionData.RESOURCE_GET)] -= 1

# Move robber
##
def move_robber(player, game):
    game.board[game.robber_id[0]][3] = False
    game.robber_id[0] = player.action_data.get(Player.ActionData.ROBBER_TILE_ID)
    game.board[game.robber_id[0]][3] = True

    if player.action_data.get(Player.ActionData.ROBBER_PLAYER_TARGET) != "none":
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

# ------------------------------
# End turn ---
# Trade player ---
# ------------------------------

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


# ------------------------------
# Search action methods
# ------------------------------

"Searches for all available moves in categories:"
"- Build/Buy"
"- Use development cards"
"- Trade"
"- Other"
"Appends all actions to respective lists"

# Dataclass to store action type and related action data for each action
@dataclass
class Action:
    type: ActionType
    data: dict

def search_build_road(player, game):
    actions = []

    if player.pieces.get('roads') == 0 or player.resource_cards.get('brick') < 1 or player.resource_cards.get('wood') < 1:
        return actions
    else:
        # Edges owned by the player
        owned_edges = [eid for eid, data in game.edges.items() if data[1] == player.id]

        # Candidate edges adjacent to the player's roads
        open_edges = set()
        for id in owned_edges:
            node1, node2 = game.edges[id][0]
            for adj_id, adj_data in game.edges.items():
                if adj_data[1] == "none" and adj_id != id:
                    if node1 in adj_data[0] or node2 in adj_data[0]:
                        open_edges.add(adj_id)

        for edge_id in open_edges:
            new_action = Action(ActionType.BUILD_ROAD, {Player.ActionData.BUILD_EDGE_ID: edge_id})
            actions.append(new_action)

        return actions

def search_build_settlement(player, game):
    actions = []

    if player.pieces.get('settlements') == 0 or player.resource_cards.get('brick') < 1 or player.resource_cards.get('wood') < 1 or player.resource_cards.get('sheep') or player.resource_cards.get('wheat'):
        return actions
    else:
        # Get a list of owned edges
        owned_edges = []
        for key, data in game.edges.items():
            if data[1] == player.id:
                owned_edges.append(key)
        
        # Get a list of open nodes adjacent to owned edges
        open_nodes = []
        for key in owned_edges:
            for node in game.edges[key][0]:
                if game.nodes[node][1][1] == "none":
                    if node not in open_nodes:
                        open_nodes.append(node)

        # Loop over copy of open_nodes with [:]
        for key in open_nodes[:]:
            for edge in game.edges:
                # edge[0] contains the two nodes connected by the edge
                if key in game.edges[edge][0]:
                    # Get the other node in the edge
                    for node in game.edges[edge][0]:
                        if node != key and game.nodes[node][1][1] != "none":
                            open_nodes.remove(key)
                            break  # stop checking this key
                    break # stop checking other edges after removing key

        for node in open_nodes:
            new_action = Action(ActionType.BUILD_SETTLEMENT, {Player.ActionData.BUILD_EDGE_ID: node})
            actions.append(new_action)
        
        return actions

def search_build_city(player,game):
    actions = []

    if player.pieces.get('cities') == 0 or player.resource_cards.get('wheat') < 2 or player.resource_cards.get('stone') < 3:
        return actions
    else:
        for node in game.nodes:
            if game.nodes[node][1][1] == player.id and game.nodes[node][1][2] == 'settlement':
                new_action = Action(ActionType.BUILD_CITY, {Player.ActionData.BUILD_NODE_ID: node})
                actions.append(new_action)

        return actions

def search_buy_devcard(player, game):
    actions = []

    if not game.development_cards or player.resource_cards.get('wheat') < 1 or player.resource_cards.get('stone') < 1 or player.resource_cards.get('stone') < 1:
        return actions
    else:
        new_action = Action(ActionType.BUY_DEV_CARD, {})
        actions.append(new_action)
    return actions

def search_devcard_knight(player, game):
    actions = []

    if player.development_cards.get('knight') < 1:
        return actions
    else:
        # Copy of search_move_robber() with ActionType.USE_KNIGHT instead of ActionType.MOVE_ROBBER
        tiles = set(range(1, 20))
        seen_tiles = set()

        # Append tiles with adjacent players
        for node in game.nodes:
            for tile in game.nodes[node][0]:
                if tile != game.robber_id[0]:
                    if game.nodes[node][1][1] != "none" and game.nodes[node][1][1] != player.id:
                        new_action = Action(ActionType.USE_KNIGHT, {Player.ActionData.ROBBER_TILE_ID: tile, Player.ActionData.ROBBER_PLAYER_TARGET: game.nodes[node][1][1]})
                        if new_action not in actions:
                            seen_tiles.add(tile)
                            actions.append(new_action)

        # Append tiles without adjacent players
        for tile in (tiles - seen_tiles):
            if tile != game.robber_id[0]:
                new_action = Action(ActionType.USE_KNIGHT, {Player.ActionData.ROBBER_TILE_ID: tile, Player.ActionData.ROBBER_PLAYER_TARGET: "none"})
                actions.append(new_action)

        return actions

def search_devcard_buildroad(player, game):
    actions = []

    if player.development_cards.get('build_road') < 1:
        return actions
    else:
         # Get a set of owned nodes
        owned_nodes = set()
        for key, data in game.nodes.items():
            if data[1][1] == player.id:
                owned_nodes.add(key)

        road_pairs = []

        # Check open edges for first road
        first_road_ids = buildroad_helper(player, game)

        # Check open edges for second roads after first road has been placed
        for id in first_road_ids:
            copy = game
            copy.edges[id][1] = player.id
            second_road_ids = buildroad_helper(player, copy)
            road_pairs.append(id, second_road_ids)

        for pair in road_pairs:
            for id in pair[1]:
                new_action = Action(ActionType.USE_BUILDROAD, {Player.ActionData.BUILD_EDGE_ID: pair[0], Player.ActionData.BUILD_EDGE_EXTRA_ID: id})
                if new_action not in actions:
                    actions.append(new_action)

        return actions

# Helper function that returns a set of valid edge ids for placing a road
def buildroad_helper(player, game):
    # Edges owned by the player
    owned_edges = [eid for eid, data in game.edges.items() if data[1] == player.id]

    # Open edges adjacent to the player's roads
    open_edges = set()
    for id in owned_edges:
        node1, node2 = game.edges[id][0]
        for adj_id, adj_data in game.edges.items():
            if adj_data[1] == "none" and adj_id != id:
                if node1 in adj_data[0] or node2 in adj_data[0]:
                    open_edges.add(adj_id)

    return open_edges

def search_devcard_yearofplenty(player, game):
    actions = []
    if player.development_cards.get('year_of_plenty') < 1:
        return actions
    else:
        for items in player.resource_cards.items():
            for items_extra in player.resource_cards.items():
                new_action = Action(ActionType.USE_YEAROFPLENTY, {Player.ActionData.RESOURCE_GET: items[0], Player.ActionData.RESOURCE_GET_EXTRA: items_extra[0]})
                actions.append(new_action)
        return actions

def search_devcard_monopoly(player, game):
    actions = []
    if player.development_cards.get('monopoly') < 1:
        return actions
    else:
        for items in player.resource_cards.items():
            new_action = Action(ActionType.USE_MONOPOLY, {Player.ActionData.RESOURCE_GET: items[0]})
            actions.append(new_action)
        return actions
    
def search_trade_bank(player, game):
    actions = []
    for item in player.resource_cards.items():
        if item[1] >= 4:
            for item_extra in player.resource_cards.items():
                if item[0] != item_extra[0]:
                    new_action = Action(ActionType.TRADE_BANK, {Player.ActionData.RESOURCE_GIVE: item[0], Player.ActionData.RESOURCE_GET: item_extra[0]})
                    actions.append(new_action)
    return actions

def search_trade_port(player, game):
    actions = []
    port_nodes = [1, 2, 4, 5, 8, 9, 11, 12, 14, 18, 19, 21, 22, 24, 25, 28, 29]
    owned_ports = []

    # Get list of owned ports
    for node in port_nodes:
        if game.nodes[node][1][1] == player.id:
            if game.nodes[node][1][0] not in owned_ports:
                owned_ports.append(game.nodes[node][1][0])

    # 3:1 port actions
    if "3:1" in owned_ports:
        for item in player.resource_cards.items():
            if item[1] >= 3:
                for item_extra in player.resource_cards.items():
                    if item[0] != item_extra[0]:
                        new_action = Action(ActionType.TRADE_PORT, {Player.ActionData.SPECIAL_RESOURCE_GIVE: item[0], Player.ActionData.RESOURCE_GET: item_extra[0]})
                        actions.append(new_action)

    # 2:1 port actions
    for port in owned_ports:
        if port != "3:1" and player.resource_cards.get(port) >= 2:
            for item in player.resource_cards.items():
                    if port != item[0]:
                        new_action = Action(ActionType.TRADE_PORT, {Player.ActionData.SPECIAL_RESOURCE_GIVE: port, Player.ActionData.RESOURCE_GET: item[0]})
                        actions.append(new_action)

    return actions

def search_move_robber(player, game):
    actions = []
    tiles = set(range(1, 20))
    seen_tiles = set()

    # Append tiles with adjacent players
    for node in game.nodes:
        for tile in game.nodes[node][0]:
            if tile != game.robber_id[0]:
                if game.nodes[node][1][1] != "none" and game.nodes[node][1][1] != player.id:
                    new_action = Action(ActionType.MOVE_ROBBER, {Player.ActionData.ROBBER_TILE_ID: tile, Player.ActionData.ROBBER_PLAYER_TARGET: game.nodes[node][1][1]})
                    if new_action not in actions:
                        seen_tiles.add(tile)
                        actions.append(new_action)

    # Append tiles without adjacent players
    for tile in (tiles - seen_tiles):
        if tile != game.robber_id[0]:
            new_action = Action(ActionType.MOVE_ROBBER, {Player.ActionData.ROBBER_TILE_ID: tile, Player.ActionData.ROBBER_PLAYER_TARGET: "none"})
            actions.append(new_action)

    return actions

# General search function to find all actions on player turn
def search_all(player, game):
    actions = []
    actions.append(search_build_road(player, game))
    actions.append(search_build_settlement(player, game))
    actions.append(search_build_city(player, game))
    actions.append(search_buy_devcard(player, game))
    actions.append(search_devcard_knight(player, game))
    actions.append(search_devcard_buildroad(player, game))
    actions.append(search_devcard_yearofplenty(player, game))
    actions.append(search_devcard_monopoly(player, game))
    actions.append(search_trade_bank(player, game))
    actions.append(search_trade_port(player, game))
    return actions

# ------------------------------
# Test
# ------------------------------


game = Game.Game()

game.players[0] = Player.Player(game.players[0])
game.players[1] = Player.Player(game.players[1])
game.players[2] = Player.Player(game.players[2])
game.players[3] = Player.Player(game.players[3])


game.players[0].resource_cards['wheat'] = 10
game.players[0].resource_cards['stone'] = 10
game.players[0].resource_cards['wood'] = 10
game.players[0].resource_cards['sheep'] = 10
game.players[0].resource_cards['brick'] = 10
game.players[0].development_cards['build_road'] = 10

p1 = game.players[0]
p2 = game.players[1]
p3 = game.players[2]

game.players[0].action_data[Player.ActionData.BUILD_NODE_ID] = 1
game.players[0].resource_cards['wheat'] += 1

game.nodes[1][1][1] = p3.id
game.nodes[1][1][2] = 'settlement'
game.nodes[2][1][1] = p2.id
game.nodes[2][1][2] = 'settlement'
game.edges[1][1] = p1.id
game.edges[2][1] = p1.id


print(game.robber_id)
print("----------")


list = search_move_robber(p1, game)
for item in list:
    print(item)

print("----------")

print(len(list))












#game.nodes[1][2][1][2] = 'settlement'

#test = search_build_city(p1,game)

#for item in test:
#    print(item)





#list = []
#new_action = Action(ActionType.BUILD_CITY, {Player.ActionData.BUILD_EDGE_ID: 99, Player.ActionData.BUILD_EDGE_EXTRA_ID: 99})
#list.append(new_action)

# Assigning action_data from action in list
# for item in list:
#    for key in item.data.keys():
#        p1.action_data[key] = item.data.get(key)
    
#for data in p1.action_data:
#    print(p1.action_data.get(data))