from enum import Enum
from dataclasses import dataclass
import random
import copy
from core.player import Player, ActionData
from core import game


# ------------------------------
# General functions
# ------------------------------
def execute_action(action_list: list, action_id: int, p: Player, g: game.Game):
    """
    Executes chosen action from action_list[action_index] by updating action_data then calling the correct execute action method through ACTIONS[action_type] dict.
    """
    # action_list: [Action(ActionType, dict)] -> action_list = search_all(p, g)
    print("Length of Action List:", len(action_list))
    print("Action ID type:", type(action_id))
    print("Action ID:", action_id)
    action_type = action_list[action_id].type

    for key, value in action_list[int(action_id)].data.items():
        p.action_data[key] = value

    ACTIONS[action_type](p, g)

    check_largest_army(p, g)
    check_longest_road(p, g)

def search_action(p: Player, g: game.Game):
    """
    Searches for all available actions and returns a list: [Action(ActionType.ACTION, {ActionData.DATA1: data1, ...}].
    """
    if g.turn_number <= 2 * len(g.players):
        actions = []
    
        # Get a list of owned edges
        owned_edges = []
        for key, data in g.edges.items():
            if data[1] == p.id:
                owned_edges.append(key)
            
        # Get a list of open nodes adjacent to owned edges
        open_nodes = set(range(1, 55))
        occupied_nodes = set()

        for node in g.nodes:
            if g.nodes[node][1][1] != "none":
                open_nodes.remove(node)
                occupied_nodes.add(node)
                
        # Remove nodes that are adjacent to occupied nodes
        for node in occupied_nodes:
            for edge in g.edges:
                if node in g.edges[edge][0]:
                    for unav_node in g.edges[edge][0]:
                        if unav_node in open_nodes:
                            open_nodes.remove(unav_node)
        
        for node in open_nodes:
            for edge in g.edges:
                if node in g.edges[edge][0] and g.edges[edge][1] == "none":
                    new_action = Action(ActionType.START_TURNS, {ActionData.BUILD_NODE_ID: node, ActionData.BUILD_EDGE_ID: edge})
                    actions.append(new_action)

        return actions

    else:
        # Flatten lists with * (unpacking operator) to get a clean list instead of a list of lists
        return [
            *search_build_road(p, g),
            *search_build_settlement(p, g),
            *search_build_city(p, g),
            *search_buy_devcard(p, g),
            *search_devcard_knight(p, g),
            *search_devcard_buildroad(p, g),
            *search_devcard_yearofplenty(p, g),
            *search_devcard_monopoly(p, g),
            *search_trade_bank(p, g),
            *search_trade_port(p, g)
    ]

# ------------------------------
# Individual execute action functions
# ------------------------------
# Start turns
def start_turns(p: Player, g: game.Game):
    """
    Execute actions on TURNS 1 & 2.
    """
    # Turn 1
    if p.pieces.get("settlements") == 5:
        p.pieces['roads'] -= 1
        g.edges[p.action_data.get(ActionData.BUILD_EDGE_ID)][1] = p.id
        p.owned_edges.add(ActionData.BUILD_EDGE_ID)

        p.vic_points += 1
        p.pieces['settlements'] -= 1
        g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = p.id
        g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'
        p.owned_nodes.add(ActionData.BUILD_NODE_ID)

    # Turn 2
    else:
        p.pieces['roads'] -= 1
        g.edges[p.action_data.get(ActionData.BUILD_EDGE_ID)][1] = p.id
        p.owned_edges.add(ActionData.BUILD_EDGE_ID)

        p.vic_points += 1
        p.pieces['settlements'] -= 1
        g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = p.id
        g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'
        p.owned_edges.add(ActionData.BUILD_NODE_ID)

        # Get resources from tiles adjacent to BUILD_NODE
        for tile in g.nodes[ActionData.BUILD_NODE_ID][0]:
            p.resource_cards[g.board[tile][0]] += 1

# Build
def build_road(p: Player, g: game.Game):
    """
    Build road on ActionData.BUILD_EDGE_ID.
    """
    p.resource_cards['wood'] -= 1
    p.resource_cards['brick'] -= 1
    g.resource_cards['wood'] += 1
    g.resource_cards['brick'] += 1

    p.pieces['roads'] -= 1
    g.edges[p.action_data.get(ActionData.BUILD_EDGE_ID)][1] = p.id
    p.owned_edges.add(ActionData.BUILD_EDGE_ID)

def build_settlement(p: Player, g: game.Game):
    """
    Build settlement on ActionData.BUILD_NODE_ID.
    """
    p.resource_cards['wood'] -= 1
    p.resource_cards['brick'] -= 1
    p.resource_cards['sheep'] -= 1
    p.resource_cards['wheat'] -= 1
    g.resource_cards['wood'] += 1
    g.resource_cards['brick'] += 1
    g.resource_cards['sheep'] += 1
    g.resource_cards['wheat'] += 1

    p.vic_points += 1
    p.pieces['settlements'] -= 1
    g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = p.id
    g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'settlement'
    p.owned_nodes.add(ActionData.BUILD_NODE_ID)

def build_city(p: Player, g: game.Game):
    """
    Build city on ActionData.BUILD_NODE_ID.
    """
    p.resource_cards['wheat'] -= 2
    p.resource_cards['stone'] -= 3
    g.resource_cards['wheat'] += 2
    g.resource_cards['stone'] += 3

    p.pieces['cities'] -= 1
    p.vic_points += 1
    g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][1] = p.id
    g.nodes[p.action_data.get(ActionData.BUILD_NODE_ID)][1][2] = 'city'

# Buy development card
def buy_devcard(p: Player, g: game.Game):
    """
    Buy a development card.
    """
    p.resource_cards['wheat'] -= 1
    p.resource_cards['sheep'] -= 1
    p.resource_cards['stone'] -= 1
    g.resource_cards['wheat'] += 1
    g.resource_cards['sheep'] += 1
    g.resource_cards['stone'] += 1

    drawn_card = g.development_cards.pop()
    p.development_cards[drawn_card] += 1
    if drawn_card == 'vic_point':
        p.vic_points += 1

# Use development cards
def use_devcard_knight(p: Player, g: game.Game):
    """
    Use Knight development card.
    """
    p.development_cards['knight'] -= 1
    p.development_cards['used_knight'] += 1
    move_robber(p, g)

def use_devcard_buildroad(p: Player, g: game.Game):
    """
    Use Road Building development card.
    """
    p.development_cards['build_road'] -= 1
    p.pieces['roads'] -= 2
    g.edges[p.action_data.get(ActionData.BUILD_EDGE_ID)][1] = p.id
    g.edges[p.action_data.get(ActionData.BUILD_EDGE_EXTRA_ID)][1] = p.id
    p.owned_edges.add(ActionData.BUILD_EDGE_ID)
    p.owned_edges.add(ActionData.BUILD_EDGE_EXTRA_ID)

def use_devcard_yearofplenty(p: Player, g: game.Game):
    """
    Use Year of Plenty development card.
    """
    p.development_cards['year_of_plenty'] -= 1

    g.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] -= 1
    g.resource_cards[p.action_data.get(ActionData.RESOURCE_GET_EXTRA)] -= 1
    p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] += 1
    p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET_EXTRA)] += 1

def use_devcard_monopoly(p: Player, g: game.Game):
    """
    Use Monopoly development card.
    """
    p.development_cards['monopoly'] -= 1
    for other_player in g.players:
        if other_player != p and other_player != "none":
            p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] += other_player.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)]
            other_player.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] = 0

# Trade
def trade_bank(p: Player, g: game.Game):
    """
    Trade 4 of ActionData.RESOURCE_GIVE with bank to get 1 of ActionData.RESOURCE_GET.
    """
    p.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] -= 4
    g.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] += 4
    p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] += 1
    g.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] -= 1

def trade_port(p: Player, g: game.Game):
    """
    Trade 2 or 3 of ActionData.RESOURCE_GIVE with port to get 1 of ActionData.RESOURCE_GET.
    """
    if p.action_data.get(ActionData.PORT) == '3:1':
        p.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] -= 3
        g.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] += 3
        p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] += 1
        g.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] -= 1
    else:
        p.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] -= 2
        g.resource_cards[p.action_data.get(ActionData.RESOURCE_GIVE)] += 2
        p.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] += 1
        g.resource_cards[p.action_data.get(ActionData.RESOURCE_GET)] -= 1

# Move robber

def move_robber(p: Player, g: game.Game):
    """
    Move robber to ActionData.ROBBER_TILE_ID and steal random resource card from ActionData.ROBBER_PLAYER_TARGET.
    """
    g.board[g.robber_id[0]][3] = False
    g.robber_id[0] = p.action_data.get(ActionData.ROBBER_TILE_ID)
    g.board[g.robber_id[0]][3] = True

    if p.action_data.get(ActionData.ROBBER_PLAYER_TARGET) != "none":
        target_player = p.action_data.get(ActionData.ROBBER_PLAYER_TARGET)
        card_list = []
        
        for item in target_player.resource_cards:
            count = target_player.resource_cards.get(item)
            for i in range(count):
                card_list.append(item)
            target_player.resource_cards[item] = 0

        random.shuffle(card_list)
        p.resource_cards[card_list.pop()] += 1

        for item in card_list:
            target_player.resource_cards[item] += 1

# End turn
def end_turn(p: Player, g: game.Game):
    """
    End turn.
    """
    g.finish_turn()


# Trade p ---

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
# Search action functions
# ------------------------------
@dataclass
class Action:
    """
    Class to store action type and related action data.
    """
    type: ActionType
    data: dict

def search_build_road(p: Player, g: game.Game):
    """
    Searches for build road actions and returns a list: [(Action(ActionType.BUILD_ROAD, {ActionData.BUILD_EDGE_ID: edge_id}), ...].
    """
    actions = []

    if p.pieces.get('roads') == 0 or p.resource_cards.get('brick') < 1 or p.resource_cards.get('wood') < 1:
        return actions
    else:
        # Edges owned by the p
        owned_edges = [eid for eid, data in g.edges.items() if data[1] == p.id]

        # Candidate edges adjacent to the p's roads
        open_edges = set()
        for id in owned_edges:
            node1, node2 = g.edges[id][0]
            for adj_id, adj_data in g.edges.items():
                if adj_data[1] == "none" and adj_id != id:
                    if node1 in adj_data[0] or node2 in adj_data[0]:
                        open_edges.add(adj_id)

        for edge_id in open_edges:
            new_action = Action(ActionType.BUILD_ROAD, {ActionData.BUILD_EDGE_ID: edge_id})
            actions.append(new_action)

        return actions

def search_build_settlement(p: Player, g: game.Game):
    """
    Searches for build settlement actions and returns a list: [(Action(ActionType.BUILD_SETTLEMENT, {ActionData.BUILD_NODE_ID: node_id}), ...].
    """
    actions = []

    if p.pieces.get('settlements') == 0 or p.resource_cards.get('brick') < 1 or p.resource_cards.get('wood') < 1 or p.resource_cards.get('sheep') or p.resource_cards.get('wheat'):
        return actions
    else:
        # Get a list of owned edges
        owned_edges = []
        for key, data in g.edges.items():
            if data[1] == p.id:
                owned_edges.append(key)
        
        # Get a list of open nodes adjacent to owned edges
        open_nodes = []
        for key in owned_edges:
            for node in g.edges[key][0]:
                if g.nodes[node][1][1] == "none":
                    if node not in open_nodes:
                        open_nodes.append(node)

        # Loop over copy of open_nodes with [:]
        for key in open_nodes[:]:
            for edge in g.edges:
                if key in g.edges[edge][0]:
                    for node in g.edges[edge][0]:
                        if node != key and g.nodes[node][1][1] != "none":
                            open_nodes.remove(key)
                            break
                    break

        for node in open_nodes:
            new_action = Action(ActionType.BUILD_SETTLEMENT, {ActionData.BUILD_EDGE_ID: node})
            actions.append(new_action)
        
        return actions

def search_build_city(p: Player, g: game.Game):
    """
    Searches for build city actions and returns a list: [(Action(ActionType.BUILD_SETTLEMENT, {ActionData.BUILD_NODE_ID: node_id}), ...].
    """
    actions = []

    if p.pieces.get('cities') == 0 or p.resource_cards.get('wheat') < 2 or p.resource_cards.get('stone') < 3:
        return actions
    else:
        for node in g.nodes:
            if g.nodes[node][1][1] == p.id and g.nodes[node][1][2] == 'settlement':
                new_action = Action(ActionType.BUILD_CITY, {ActionData.BUILD_NODE_ID: node})
                actions.append(new_action)

        return actions

def search_buy_devcard(p: Player, g: game.Game):
    """
    Searches for buying development card action and returns a list: [(Action(ActionType.BUILD_DEV_CARD, {}), ...].
    """
    actions = []

    if not g.development_cards or p.resource_cards.get('wheat') < 1 or p.resource_cards.get('stone') < 1 or p.resource_cards.get('stone') < 1:
        return actions
    else:
        new_action = Action(ActionType.BUY_DEV_CARD, {})
        actions.append(new_action)
    return actions

def search_devcard_knight(p: Player, g: game.Game): 
    """
    Searches for use Knight actions and returns a list: [(Action(ActionType.USE_KNIGHT, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: player_id}), ...].
    """
    actions = []

    if p.development_cards.get('knight') < 1:
        return actions
    else:
        # Copy of search_move_robber() with ActionType.USE_KNIGHT instead of ActionType.MOVE_ROBBER
        tiles = set(range(1, 20))
        seen_tiles = set()

        # Append tiles with adjacent players
        for node in g.nodes:
            for tile in g.nodes[node][0]:
                if tile != g.robber_id[0]:
                    if g.nodes[node][1][1] != "none" and g.nodes[node][1][1] != p.id:
                        new_action = Action(ActionType.USE_KNIGHT, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: g.nodes[node][1][1]})
                        if new_action not in actions:
                            seen_tiles.add(tile)
                            actions.append(new_action)

        # Append tiles without adjacent players
        for tile in (tiles - seen_tiles):
            if tile != g.robber_id[0]:
                new_action = Action(ActionType.USE_KNIGHT, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: "none"})
                actions.append(new_action)

        return actions

def search_devcard_buildroad(p: Player, g: game.Game):
    """
    Searches for use Road Building actions and returns a list: [(ActionType.USE_BUILDROAD, {ActionData.BUILD_EDGE_ID: edge_id, ActionData.BUILD_EDGE_EXTRA_ID: edge_id), ...].
    """
    # Helper function that returns a set of valid edge ids for placing a road
    def buildroad_helper(p, g):
        # Edges owned by the p
        owned_edges = [eid for eid, data in g.edges.items() if data[1] == p.id]

        # Open edges adjacent to the p's roads
        open_edges = set()
        for id in owned_edges:
            node1, node2 = g.edges[id][0]
            for adj_id, adj_data in g.edges.items():
                if adj_data[1] == "none" and adj_id != id:
                    if node1 in adj_data[0] or node2 in adj_data[0]:
                        open_edges.add(adj_id)

        return open_edges


    actions = []

    if p.development_cards.get('build_road') < 2:
        return actions
    else:
         # Get a set of owned nodes
        owned_nodes = set()
        for key, data in g.nodes.items():
            if data[1][1] == p.id:
                owned_nodes.add(key)

        # Store tuples of (edge_min, edge_max)
        seen_pairs = set()

        # Check open edges for first road
        first_road_ids = buildroad_helper(p, g)

        # Check open edges for second roads after first road has been placed
        for id1 in first_road_ids:
            game_copy = copy.deepcopy(g)
            game_copy.edges[id1][1] = p.id
            second_road_ids = buildroad_helper(p, game_copy)
            
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

def search_devcard_yearofplenty(p: Player, g: game.Game):
    """
    Searches for use Year of Plenty actions and returns a list: [(ActionType.USE_YEAROFPLENTY, {ActionData.RESOURCE_GET: resource, ActionData.RESOURCE_GET_EXTRA: resource}), ...].
    """
    actions = []
    if p.development_cards.get('year_of_plenty') < 1:
        return actions
    else:
        for item in p.resource_cards.items():
            for item_extra in p.resource_cards.items():
                if g.resource_cards.get(item[0]) > 1 and g.resource_cards.get(item_extra[0]) > 1:
                    new_action = Action(ActionType.USE_YEAROFPLENTY, {ActionData.RESOURCE_GET: item[0], ActionData.RESOURCE_GET_EXTRA: item_extra[0]})
                    actions.append(new_action)
        return actions

def search_devcard_monopoly(p: Player, g: game.Game):
    """
    Searches for use Monopoly actions and returns a list: [(ActionType.USE_MONOPOLY, {ActionData.RESOURCE_GET: resource}), ...].
    """
    actions = []
    if p.development_cards.get('monopoly') < 1:
        return actions
    else:
        for items in p.resource_cards.items():
            new_action = Action(ActionType.USE_MONOPOLY, {ActionData.RESOURCE_GET: items[0]})
            actions.append(new_action)
        return actions
    
def search_trade_bank(p: Player, g: game.Game):
    """
    Searches for use trade bank actions and returns a list: [(ActionType.TRADE_BANK, {ActionData.RESOURCE_GIVE: resource, ActionData.RESOURCE_GET: resource}), ...].
    """
    actions = []
    for item in p.resource_cards.items():
        if item[1] >= 4:
            for item_extra in p.resource_cards.items():
                if item[0] != item_extra[0] and g.resource_cards.get(item_extra[0]) > 1:
                    new_action = Action(ActionType.TRADE_BANK, {ActionData.RESOURCE_GIVE: item[0], ActionData.RESOURCE_GET: item_extra[0]})
                    actions.append(new_action)
    return actions

def search_trade_port(p: Player, g: game.Game):
    """
    Searches for use trade port actions and returns a list: [(ActionType.TRADE_PORT, {ActionData.RESOURCE_GIVE: resource, ActionData.RESOURCE_GET: resource}), ...].
    """
    actions = []
    port_nodes = [1, 2, 4, 5, 8, 9, 11, 12, 14, 18, 19, 21, 22, 24, 25, 28, 29]
    owned_ports = []

    # Get list of owned ports
    for node in port_nodes:
        if g.nodes[node][1][1] == p.id:
            if g.nodes[node][1][0] not in owned_ports:
                owned_ports.append(g.nodes[node][1][0])

    # 3:1 port actions
    if "3:1" in owned_ports:
        for item in p.resource_cards.items():
            if item[1] >= 3:
                for item_extra in p.resource_cards.items():
                    if item[0] != item_extra[0] and g.resource_cards.get(item_extra[0]) > 1:
                        new_action = Action(ActionType.TRADE_PORT, {ActionData.RESOURCE_GIVE: item[0], ActionData.RESOURCE_GET: item_extra[0]})
                        actions.append(new_action)

    # 2:1 port actions
    for port in owned_ports:
        if port != "3:1" and p.resource_cards.get(port) >= 2:
            for item in p.resource_cards.items():
                    if port != item[0] and g.resource_cards.get(item[0]) > 1:
                        new_action = Action(ActionType.TRADE_PORT, {ActionData.RESOURCE_GIVE: port, ActionData.RESOURCE_GET: item[0]})
                        actions.append(new_action)

    return actions

def search_move_robber(p: Player, g: game.Game):
    """
    Searches for move robber actions and returns a list: [(Action(ActionType.MOVE_ROBBER, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: player_id}), ...].
    """
    actions = []
    tiles = set(range(1, 20))
    seen_tiles = set()

    # Append tiles with adjacent players
    for node in g.nodes:
        for tile in g.nodes[node][0]:
            if tile != g.robber_id[0]:
                if g.nodes[node][1][1] != "none" and g.nodes[node][1][1] != p.id:
                    new_action = Action(ActionType.MOVE_ROBBER, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: g.nodes[node][1][1]})
                    if new_action not in actions:
                        seen_tiles.add(tile)
                        actions.append(new_action)

    # Append tiles without adjacent players
    for tile in (tiles - seen_tiles):
        if tile != g.robber_id[0]:
            new_action = Action(ActionType.MOVE_ROBBER, {ActionData.ROBBER_TILE_ID: tile, ActionData.ROBBER_PLAYER_TARGET: "none"})
            actions.append(new_action)

    return actions

def search_end_turn(p: Player, g: game.Game):
    """
    Returns a list: [(Action(ActionType.END_TURN, {})].
    """
    return [Action(ActionType.END_TURN, {})]

# ------------------------------
# Additional check functions
# ------------------------------
def check_largest_army(p: Player, g: game.Game):
    """
    Checks and updates largest army bonus.
    """
    if p.id == g.largest_army_player_id:
        return
    elif p.development_cards.get("used_knight") < 3:
        return
    elif g.largest_army_player_id == "none":
        g.largest_army_player_id = p.id
        p.has_largest_army = True
        p.vic_points += 2
        return
    else:
        num = p.development_cards.get("used_knight")
        for other_player in g.players:
            if other_player.id != g.largest_army_player_id:
                continue
            elif num > other_player.development_cards.get("used_knight"):
                g.largest_army_player_id = p.id
                p.has_largest_army = True
                p.vic_points += 2

                other_player.has_largest_army = False
                other_player.vic_points -= 2
                return
            elif num == other_player.development_cards.get("used_knight"):
                g.largest_army_player_id = "none"
                other_player.has_largest_army = False
                other_player.vic_points -= 2
                return
            else:
                return

def check_longest_road(p: Player, g: game.Game):
    """
    Checks and updates longest road bonus.
    """
    if p.id == g.longest_road_player_id:
        return

    # Build graph of the p's roads (edges)
    adj = {}
    for edge_id, (nodes, owner_id) in g.edges.items():
        if owner_id != p.id:
            continue
        a, b = nodes

        # Block roads passing through opponent buildings
        for node in [a, b]:
            building_owner = g.nodes[node][1][1]  # access owner from [port, owner, building]
            if building_owner not in [None, "none", p.id]:
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
            building_owner = g.nodes[neighbor][1][1]
            if building_owner not in [None, "none", p.id]:
                continue
            visited_edges.add(edge_id)
            max_length = max(max_length, 1 + dfs(neighbor, visited_edges))
            visited_edges.remove(edge_id)
        return max_length

    longest = 0
    for node in adj:
        longest = max(longest, dfs(node, set()))

    if longest < 5:
        return

    if g.longest_road_player_id == "none":
        g.longest_road_player_id = p.id
        g.longest_road_length = longest
        p.vic_points += 2
        return

    for other_player in g.players:
        if other_player.id == g.longest_road_player_id:
            if longest > g.longest_road_length:
                g.longest_road_player_id = p.id
                g.longest_road_length = longest
                
                p.has_longest_road = True
                p.vic_points += 2

                other_player.has_longest_road = False
                other_player.vic_points -= 2

            elif longest == g.longest_road_length:
                g.longest_road_player_id = "none"
                other_player.has_longest_road = False
                other_player.vic_points -= 2
            return

# ------------------------------
# Test
# ------------------------------

#catan_game = game.Game()

#for name in catan_game.PLAYER_NAMES:
#    catan_game.players.append(Player(name))


#catan_game.players[0].resource_cards['wheat'] = 10
#catan_game.players[0].resource_cards['stone'] = 10
#catan_game.players[0].resource_cards['wood'] = 10
#catan_game.players[0].resource_cards['sheep'] = 10
#catan_game.players[0].resource_cards['brick'] = 10



#p1 = catan_game.players[0]
#p2 = catan_game.players[1]
#p3 = catan_game.players[2]

#catan_game.nodes[1][1][1] = p1.id

#print("----------")
#list = search_action(p1, catan_game)
#for item in list:
#    print(item)

#print("----------")

#print(len(list))