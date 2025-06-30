import random

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

# Example usage
if __name__ == "__main__":
    board = generate_catan_board()
    for k in sorted(board.keys()):
        print(f"Tile {k}: {board[k]}")
