from enum import Enum
from dataclasses import dataclass
import random
import copy
from player import Player, ActionData
import game


# ------------------------------
# General methods
# ------------------------------
"action_list: [Action(ActionType, dict)] -> action_list = search_all(player, game)"
"Executes chosen action from action_list[action_index] by updating action_data then calling the correct execute action method through ACTIONS[action_type] dict"
def execute_action(action_list: list, action_id: int, player: Player, game: game.Game):

    action_type = action_list[action_id].type

    for key, value in action_list[action_id].data:
        player.action_data[key] = value

    ACTIONS[action_type](player, game)

"Checks and updates longest road and largest army"
def check_bonuses(player, game):
    check_largest_army(player, game)
    check_longest_road(player, game)

"Searches for all available actions and returns a list: [Action(ActionType.ACTION, {ActionData.DATA1: data1, ...}]"
def search_action(player, game):
    # Flatten lists with * (unpacking operator) to get a clean list instead of a list of lists
    return [
        *search_build_road(player, game),
        *search_build_settlement(player, game),
        *search_build_city(player, game),
        *search_buy_devcard(player, game),
        *search_devcard_knight(player, game),
        *search_devcard_buildroad(player, game),
        *search_devcard_yearofplenty(player, game),
        *search_devcard_monopoly(player, game),
        *search_trade_bank(player, game),
        *search_trade_port(player, game)
    ]

"Searches for all available actions on TURNS 1 & 2 and returns a list: [Action(ActionType.ACTION, {ActionData.DATA1: data1, ...}]"
def search_action_start_turns(player, game):
    actions = []
   
    # Get a list of owned edges
    owned_edges = []
    for key, data in game.edges.items():
        if data[1] == player.id:
            owned_edges.append(key)
        
     # Get a list of open nodes adjacent to owned edgescxbv 
    open_nodes = set(range(1, 55))
    occupied_nodes = set()

    for node in game.nodes:
        if game.nodes[node][1][1] != "none":
            open_nodes.remove(node)
            occupied_nodes.add(node)
            
    
    # Remove nodes that are adjacent to occupied nodes
    for node in occupied_nodes:
        for edge in game.edges:
            if node in game.edges[edge][0]:
                for unav_node in game.edges[edge][0]:
                    if unav_node in open_nodes:
                        open_nodes.remove(unav_node)
    
    for node in open_nodes:
        for edge in game.edges:
            if node in game.edges[edge][0] and game.edges[edge][1] == "none":
                new_action = Action(ActionType.START_TURNS, {ActionData.BUILD_NODE_ID: node, ActionData.BUILD_EDGE_ID: edge})
                actions.append(new_action)

    return actions


# ------------------------------
# Individual execute action methods
# ------------------------------

# Start turns
def start_turns(player, game):
    # Turn 1
    if player.pieces.get("settlements") == 5:
        player.pieces['roads'] -= 1
        game.edges[player.action_data.get(ActionData.BUILD_EDGE_ID)][1] = player.id

        player.vic_points += 1
        player.pieces['settlements'] -= 1
        game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = player.id
        game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'

    # Turn 2
    else:
        player.pieces['roads'] -= 1
        game.edges[player.action_data.get(ActionData.BUILD_EDGE_ID)][1] = player.id

        player.vic_points += 1
        player.pieces['settlements'] -= 1
        game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = player.id
        game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'

        # Get resources from tiles adjacent to BUILD_NODE
        for tile in game.nodes[ActionData.BUILD_NODE_ID][0]:
            player.resource_cards[game.board[tile][0]] += 1

# Build
def build_road(player, game):
    player.resource_cards['wood'] -= 1
    player.resource_cards['brick'] -= 1
    game.resource_cards['wood'] += 1
    game.resource_cards['brick'] += 1

    player.pieces['roads'] -= 1
    game.edges[player.action_data.get(ActionData.BUILD_EDGE_ID)][1] = player.id

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
    game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = player.id
    game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'

def build_city(player, game):
    player.resource_cards['wheat'] -= 2
    player.resource_cards['stone'] -= 3
    game.resource_cards['wheat'] += 2
    game.resource_cards['stone'] += 3

    player.pieces['cities'] -= 1
    player.vic_points += 1
    game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = player.id
    game.nodes[player.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'city'

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
def use_devcard_knight(player, game):
    player.development_cards['knight'] -= 1
    player.development_cards['used_knight'] += 1
    move_robber(player, game)

def use_devcard_buildroad(player, game):
    player.development_cards['build_road'] -= 1
    player.pieces['roads'] -= 2
    game.edges[player.action_data.get(ActionData.BUILD_EDGE_ID)][1] = player.id
    game.edges[player.action_data.get(ActionData.BUILD_EDGE_EXTRA_ID)][1] = player.id

def use_devcard_yearofplenty(player, game):
    player.development_cards['year_of_plenty'] -= 1

    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] -= 1
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET_EXTRA)] -= 1
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] += 1
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(player, game):
    player.development_cards['monopoly'] -= 1
    for other_player in game.players:
        if other_player != player and other_player != "none":
            player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] += other_player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)]
            other_player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] = 0

# Trade
def trade_bank(player, game):
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GIVE)] -= 4
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] += 1
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GIVE)] += 4
    player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] -= 1

def trade_port(player, game):
    if player.action_data.get(ActionData.PORT) == '3:1':
        player.resource_cards[player.action_data.get(ActionData.SPECIAL_RESOURCE_GIVE)] -= 3
        player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] += 1
        player.resource_cards[player.action_data.get(ActionData.SPECIAL_RESOURCE_GIVE)] += 3
        player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] -= 1
    else:
        player.resource_cards[player.action_data.get(ActionData.PORT)] -= 2
        player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] += 1
        player.resource_cards[player.action_data.get(ActionData.PORT)] += 2
        player.resource_cards[player.action_data.get(ActionData.RESOURCE_GET)] -= 1

# Move robber
def move_robber(player, game):
    game.board[game.robber_id[0]][3] = False
    game.robber_id[0] = player.action_data.get(ActionData.ROBBER_TILE_ID)
    game.board[game.robber_id[0]][3] = True

    if player.action_data.get(ActionData.ROBBER_PLAYER_TARGET) != "none":
        target_player = player.action_data.get(ActionData.ROBBER_PLAYER_TARGET)
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

# End turn
def end_turn(player, game):
    player.turn = False

# Trade player ---

# Enumeration for all possible actions
class ActionType(Enum):
    # Start turns actions
    START_TURNS = "start_turns"

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
    ActionType.START_TURNS: start_turns,

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
    ActionType.END_TURN: end_turn
}


# ------------------------------
# Search action methods
# ------------------------------
"Searches for all available moves in categories:"
"- Build/Buy"
"- Use development cards"
"- Trade"
"- Other"
"Each function returns all respective actions in a list: [Action(ActionType.ACTION, {ActionData.DATA1: data1, ...}]"

# Dataclass to store action type and related action data
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
            new_action = Action(ActionType.BUILD_ROAD, {ActionData.BUILD_EDGE_ID: edge_id})
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
            new_action = Action(ActionType.BUILD_SETTLEMENT, {ActionData.BUILD_EDGE_ID: node})
            actions.append(new_action)
        
        return actions

def search_build_city(player,game):
    actions = []

    if player.pieces.get('cities') == 0 or player.resource_cards.get('wheat') < 2 or player.resource_cards.get('stone') < 3:
        return actions
    else:
        for node in game.nodes:
            if game.nodes[node][1][1] == player.id and game.nodes[node][1][2] == 'settlement':
                new_action = Action(ActionType.BUILD_CITY, {ActionData.BUILD_NODE_ID: node})
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
                        new_action = Action(ActionType.USE_KNIGHT, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: game.nodes[node][1][1]})
                        if new_action not in actions:
                            seen_tiles.add(tile)
                            actions.append(new_action)

        # Append tiles without adjacent players
        for tile in (tiles - seen_tiles):
            if tile != game.robber_id[0]:
                new_action = Action(ActionType.USE_KNIGHT, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: "none"})
                actions.append(new_action)

        return actions

def search_devcard_buildroad(player, game):

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


    actions = []

    if player.development_cards.get('build_road') < 1:
        return actions
    else:
         # Get a set of owned nodes
        owned_nodes = set()
        for key, data in game.nodes.items():
            if data[1][1] == player.id:
                owned_nodes.add(key)

        # Store tuples of (edge_min, edge_max)
        seen_pairs = set()

        # Check open edges for first road
        first_road_ids = buildroad_helper(player, game)

        # Check open edges for second roads after first road has been placed
        for id1 in first_road_ids:
            game_copy = copy.deepcopy(game)
            game_copy.edges[id1][1] = player.id
            second_road_ids = buildroad_helper(player, game_copy)
            
            for id2 in second_road_ids:
                # Sort the edge pairs to filter duplicates
                pair = tuple(sorted((id1, id2)))

                # Skip loop iteration if pair was used
                if pair in seen_pairs:
                    continue

                seen_pairs.add(pair)

                new_action = Action(ActionType.USE_BUILDROAD, {ActionData.BUILD_EDGE_ID: pair[0], ActionData.BUILD_EDGE_EXTRA_ID: pair[1]})
                actions.append(new_action)

        return actions

def search_devcard_yearofplenty(player, game):
    actions = []
    if player.development_cards.get('year_of_plenty') < 1:
        return actions
    else:
        for items in player.resource_cards.items():
            for items_extra in player.resource_cards.items():
                new_action = Action(ActionType.USE_YEAROFPLENTY, {ActionData.RESOURCE_GET: items[0], ActionData.RESOURCE_GET_EXTRA: items_extra[0]})
                actions.append(new_action)
        return actions

def search_devcard_monopoly(player, game):
    actions = []
    if player.development_cards.get('monopoly') < 1:
        return actions
    else:
        for items in player.resource_cards.items():
            new_action = Action(ActionType.USE_MONOPOLY, {ActionData.RESOURCE_GET: items[0]})
            actions.append(new_action)
        return actions
    
def search_trade_bank(player, game):
    actions = []
    for item in player.resource_cards.items():
        if item[1] >= 4:
            for item_extra in player.resource_cards.items():
                if item[0] != item_extra[0]:
                    new_action = Action(ActionType.TRADE_BANK, {ActionData.RESOURCE_GIVE: item[0], ActionData.RESOURCE_GET: item_extra[0]})
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
                        new_action = Action(ActionType.TRADE_PORT, {ActionData.SPECIAL_RESOURCE_GIVE: item[0], ActionData.RESOURCE_GET: item_extra[0]})
                        actions.append(new_action)

    # 2:1 port actions
    for port in owned_ports:
        if port != "3:1" and player.resource_cards.get(port) >= 2:
            for item in player.resource_cards.items():
                    if port != item[0]:
                        new_action = Action(ActionType.TRADE_PORT, {ActionData.SPECIAL_RESOURCE_GIVE: port, ActionData.RESOURCE_GET: item[0]})
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
                    new_action = Action(ActionType.MOVE_ROBBER, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: game.nodes[node][1][1]})
                    if new_action not in actions:
                        seen_tiles.add(tile)
                        actions.append(new_action)

    # Append tiles without adjacent players
    for tile in (tiles - seen_tiles):
        if tile != game.robber_id[0]:
            new_action = Action(ActionType.MOVE_ROBBER, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: "none"})
            actions.append(new_action)

    return actions

def search_end_turn(player, game):
    return [Action(ActionType.END_TURN, {})]


# ------------------------------
# Additional check methods
# ------------------------------
"Methods to check largest army and longest road"

def check_largest_army(player, game):
    if player.id == game.largest_army_player_id:
        return
    elif player.development_cards.get("used_knight") < 3:
        return
    elif game.largest_army_player_id == "none":
        game.largest_army_player_id = player.id
        player.vic_points += 2
        return
    else:
        num = player.development_cards.get("used_knight")
        for other_player in game.players:
            if other_player.id != game.largest_army_player_id:
                continue
            elif num > other_player.development_cards.get("used_knight"):
                game.largest_army_player_id = player.id
                other_player.vic_points -= 2
                player.vic_points += 2
                return
            elif num == other_player.development_cards.get("used_knight"):
                game.largest_army_player_id = "none"
                other_player.vic_points -= 2
                return
            else:
                return

def check_longest_road(player, game):
    if player.id == game.longest_road_player_id:
        return

    # Build graph of the player's roads (edges)
    adj = {}
    for edge_id, (nodes, owner_id) in game.edges.items():
        if owner_id != player.id:
            continue
        a, b = nodes

        # Block roads passing through opponent buildings
        for node in [a, b]:
            building_owner = game.nodes[node][1][1]  # access owner from [port, owner, building]
            if building_owner not in [None, "none", player.id]:
                break  # skip this edge
        else:
            adj.setdefault(a, []).append((b, edge_id))
            adj.setdefault(b, []).append((a, edge_id))

    # Depth First Search to compute longest path without reusing edges or passing through opponent buildings
    def dfs(node, visited_edges):
        max_length = 0
        for neighbor, edge_id in adj.get(node, []):
            if edge_id in visited_edges:
                continue
            # Stop path if neighbor is blocked by opponent building
            building_owner = game.nodes[neighbor][1][1]
            if building_owner not in [None, "none", player.id]:
                continue
            visited_edges.add(edge_id)
            max_length = max(max_length, 1 + dfs(neighbor, visited_edges))
            visited_edges.remove(edge_id)
        return max_length

    longest = 0
    for node in adj:
        longest = max(longest, dfs(node, set()))
    
    print("longest = ", longest)

    if longest < 5:
        return

    if game.longest_road_player_id == "none":
        game.longest_road_player_id = player.id
        game.longest_road_length = longest
        player.vic_points += 2
        return

    for other_player in game.players:
        if other_player.id == game.longest_road_player_id:
            if longest > game.longest_road_length:
                game.longest_road_player_id = player.id
                game.longest_road_length = longest
                
                player.vic_points += 2
            return


# ------------------------------
# Test
# ------------------------------

#game = Game.Game()

#game.players[0] = Player(game.players[0])
#game.players[1] = Player(game.players[1])
#game.players[2] = Player(game.players[2])
#game.players[3] = Player(game.players[3])


#game.players[0].resource_cards['wheat'] = 10
#game.players[0].resource_cards['stone'] = 10
#game.players[0].resource_cards['wood'] = 10
#game.players[0].resource_cards['sheep'] = 10
#game.players[0].resource_cards['brick'] = 10



#p1 = game.players[0]
#p2 = game.players[1]
#p3 = game.players[2]

#game.nodes[1][1][1] = p1.id

#print("----------")
#list = search_action_start_turns(p1, game)
#for item in list:
#    print(item)

#print("----------")

#print(len(list))