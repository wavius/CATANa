import random

#Recouse Code
Development_Cards = {
    'knight': 14,
    'vic_point': 5,
    'build_road': 2,
    'year_of_plenty': 2,
    'monopoly': 2
    }

Resources = {
    'brick': 19,
    'wood': 19,
    'sheep': 19,
    'wheat': 19,
    'stone': 19
    }

#Hex Code
# Official resource allotments for 19 tiles
RESOURCE_ALLOTMENT = {
    "wood": 4,
    "brick": 3,
    "sheep": 4,
    "wheat": 4,
    "ore": 3,
    "desert": 1
}

# Official number token distribution
NUMBER_TOKENS = [2, 
                 3, 3, 
                 4, 4, 
                 5, 5,
                 6, 6, 
                 8, 8,
                 9, 9, 
                 10, 10, 
                 11, 11, 
                 12]

DOTS = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1
}

def generate_catan_board():
    # Step 1: Build resource pool
    resources = []
    for res, count in RESOURCE_ALLOTMENT.items():
        resources.extend([res] * count)
    random.shuffle(resources)

    # Step 2: Assign numbers (skip desert)
    number_tokens = NUMBER_TOKENS.copy()
    random.shuffle(number_tokens)

    board = {}
    tile_id = 1

    for res in resources:
        if res == "desert":
            # Desert has no number token, 0 dots, robber starts here
            board[(tile_id)] = [res, None, 0, True]
        else:
            number = number_tokens.pop()
            dots = DOTS[number]
            board[(tile_id)] = [res, number, dots, False]
        tile_id += 1

    return board

# Example usage (un-comment to run):
#if __name__ == "__main__":
#    board = generate_catan_board()
#    for k in sorted(board.keys()):
#        print(f"Tile {k}: {board[k]}")

#Node Constants
PORTS = [
    "brick",
    "wood",
    "sheep",
    "wheat",
    "rock",
    "3:1",
    "none"
]
#Nodes
nodes = [
    #Each node is represented as a dictionary with the following structure:
    #{(node_ID): [neighboring hex_IDs], port, building type, owner]}
    {1: [[1], ["wheat", "none", "none"]]},
    {2: [[1], ["wheat", "none", "none"]]},
    {3: [[1, 2], ["none", "none", "none"]]},
    {4: [[2], ["3:1", "none", "none"]]},
    {5: [[2, 3], ["3:1", "none", "none"]]},
    {6: [[3], ["none", "none", "none"]]},
    {7: [[3], ["none", "none", "none"]]},
    {8: [[3, 4], ["3:1", "none", "none"]]},
    {9: [[4], ["3:1", "none", "none"]]},
    {10: [[4, 5], ["none", "none", "none"]]},
    {11: [[5], ["wood", "none", "none"]]},
    {12: [[5], ["wood", "none", "none"]]},
    {13: [[5, 6], ["none", "none", "none"]]},
    {14: [[6], ["3:1", "none", "none"]]},
    {15: [[6, 7], ["none", "none", "none"]]},
    {16: [[7], ["none", "none", "none"]]},
    {17: [[7], ["none", "none", "none"]]},
    {18: [[7, 8], ["sheep", "none", "none"]]},
    {19: [[8], ["sheep", "none", "none"]]},
    {20: [[8, 9], ["none", "none", "none"]]},
    {21: [[9], ["3:1", "none", "none"]]},
    {22: [[9], ["3:1", "none", "none"]]},
    {23: [[9, 10], ["none", "none", "none"]]},
    {24: [[10], ["rock", "none", "none"]]},
    {25: [[10, 11], ["rock", "none", "none"]]},
    {26: [[11], ["none", "none", "none"]]},
    {27: [[11], ["none", "none", "none"]]},
    {28: [[11, 12], ["brick", "none", "none"]]},
    {29: [[12], ["brick", "none", "none"]]},
    {30: [[12, 1], ["none", "none", "none"]]},
    {31: [[1, 12, 13], ["none", "none", "none"]]},
    {32: [[1, 2, 13], ["none", "none", "none"]]},
    {33: [[2, 13, 14], ["none", "none", "none"]]},
    {34: [[2, 3, 14], ["none", "none", "none"]]},
    {35: [[3, 4, 14], ["none", "none", "none"]]},
    {36: [[4, 14, 15], ["none", "none", "none"]]},
    {37: [[4, 5, 15], ["none", "none", "none"]]},
    {38: [[5, 6, 15], ["none", "none", "none"]]},
    {39: [[6, 15, 16], ["none", "none", "none"]]},
    {40: [[6, 7, 16], ["none", "none", "none"]]},
    {41: [[7, 8, 16], ["none", "none", "none"]]},
    {42: [[8, 16, 17], ["none", "none", "none"]]},
    {43: [[8, 9, 17], ["none", "none", "none"]]},
    {44: [[9, 10, 17], ["none", "none", "none"]]},
    {45: [[10, 17, 18], ["none", "none", "none"]]},
    {46: [[10, 11, 18], ["none", "none", "none"]]},
    {47: [[11, 12, 18], ["none", "none", "none"]]},
    {48: [[12, 13, 18], ["none", "none", "none"]]},
    {49: [[13, 18, 19], ["none", "none", "none"]]},
    {50: [[13, 14, 19], ["none", "none", "none"]]},
    {51: [[14, 15, 19], ["none", "none", "none"]]},
    {52: [[15, 16, 19], ["none", "none", "none"]]},
    {53: [[16, 17, 19], ["none", "none", "none"]]},
    {54: [[17, 18, 19], ["none", "none", "none"]]}
]

#Edges UNFINISHED
edges = [
    #Each edge is represented as a dictionary with the following structure:
    #[{edge_ID}:[[connecting nodes], is road (bool), owner (if road)]
    {1:  [[1, 2], False, "none"]},
    {2:  [[2, 3], False, "none"]},
    {3:  [[3, 4], False, "none"]},
    {4:  [[4, 5], False, "none"]},
    {5:  [[5, 6], False, "none"]},
    {6:  [[6, 7], False, "none"]},
    {7:  [[7, 8], False, "none"]},
    {8:  [[8, 9], False, "none"]},
    {9:  [[9, 10], False, "none"]},
    {10: [[10, 11], False, "none"]},
    {11: [[11, 12], False, "none"]},
    {12: [[12, 13], False, "none"]},
    {13: [[13, 14], False, "none"]},
    {14: [[14, 15], False, "none"]},
    {15: [[0, 0], False, "none"]},
    {16: [[0, 0], False, "none"]},
    {17: [[0, 0], False, "none"]},
    {18: [[0, 0], False, "none"]},
    {19: [[0, 0], False, "none"]},
    {20: [[0, 0], False, "none"]},
    {21: [[0, 0], False, "none"]},
    {22: [[0, 0], False, "none"]},
    {23: [[0, 0], False, "none"]},
    {24: [[0, 0], False, "none"]},
    {25: [[0, 0], False, "none"]},
    {26: [[0, 0], False, "none"]},
    {27: [[0, 0], False, "none"]},
    {28: [[0, 0], False, "none"]},
    {29: [[0, 0], False, "none"]},
    {30: [[0, 0], False, "none"]},
    {31: [[0, 0], False, "none"]},
    {32: [[0, 0], False, "none"]},
    {33: [[0, 0], False, "none"]},
    {34: [[0, 0], False, "none"]},
    {35: [[0, 0], False, "none"]},
    {36: [[0, 0], False, "none"]},
    {37: [[0, 0], False, "none"]},
    {38: [[0, 0], False, "none"]},
    {39: [[0, 0], False, "none"]},
    {40: [[0, 0], False, "none"]},
    {41: [[0, 0], False, "none"]},
    {42: [[0, 0], False, "none"]},
    {43: [[0, 0], False, "none"]},
    {44: [[0, 0], False, "none"]},
    {45: [[0, 0], False, "none"]},
    {46: [[0, 0], False, "none"]},
    {47: [[0, 0], False, "none"]},
    {48: [[0, 0], False, "none"]},
    {49: [[0, 0], False, "none"]},
    {50: [[0, 0], False, "none"]},
    {51: [[0, 0], False, "none"]},
    {52: [[0, 0], False, "none"]},
    {53: [[0, 0], False, "none"]},
    {54: [[0, 0], False, "none"]},
    {55: [[0, 0], False, "none"]},
    {56: [[0, 0], False, "none"]},
    {57: [[0, 0], False, "none"]},
    {58: [[0, 0], False, "none"]},
    {59: [[0, 0], False, "none"]},
    {60: [[0, 0], False, "none"]},
    {61: [[0, 0], False, "none"]},
    {62: [[0, 0], False, "none"]},
    {63: [[0, 0], False, "none"]},
    {64: [[0, 0], False, "none"]},
    {65: [[0, 0], False, "none"]},
    {66: [[0, 0], False, "none"]},
    {67: [[0, 0], False, "none"]},
    {68: [[0, 0], False, "none"]},
    {69: [[0, 0], False, "none"]},
    {70: [[0, 0], False, "none"]},
    {71: [[0, 0], False, "none"]},
    {72: [[0, 0], False, "none"]},
]

