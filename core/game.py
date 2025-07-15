import random 



class Game:
    """
    A class containining the components of a Settlers of Catan game: 
      - Development card deck
      - Resource card decks
      - Hex board layout with tokens and robber
      - Vertex (node) definitions for settlements/ports
      - Edge definitions for possible roads
    """

    # ----------------------------------------
    # Class-level constants
    # ----------------------------------------
    PLAYERS = ["p1", "p2", "p3", "p4", "none"]

    #Randomly shuffled to list of development cards stored in list called "development_cards"
    #String value is the type of card, int value is the number of cards of that type in the deck
    DEVELOPMENT_CARDS_ALLOTMENT = {
        "knight": 14,
        "vic_point": 5,
        "build_road": 2,
        "year_of_plenty": 2,
        "monopoly": 2
    }

    #String value is the type of resource, int value is the number of cards of that type in the deck
    #Assigned to individual lists for each resource type 
    #named "brick_cards", "wood_cards", "sheep_cards", "wheat_cards", "stone_cards"
    RESOURCES = {
        "brick": 19,
        "wood": 19,
        "sheep": 19,
        "wheat": 19,
        "stone": 19
    }

    RESOURCE_ALLOTMENT = {
        "wood": 4,
        "brick": 3,
        "sheep": 4,
        "wheat": 4,
        "ore": 3,
        "desert": 1
    }

    NUMBER_TOKENS = [
        2, 3, 3, 4, 4, 5, 5,
        6, 6, 8, 8, 9, 9,
        10, 10, 11, 11, 12
    ]

    DOTS = {
        2: 1, 3: 2, 4: 3, 5: 4,
        6: 5, 8: 5, 9: 4, 10: 3,
        11: 2, 12: 1
    }

    PORTS = ["brick", "wood", "sheep", "wheat", "rock", "3:1", "none"]


    # ----------------------------------------
    # Game initialization
    # ----------------------------------------

    def __init__(self):
        """
        Initialize the game by generating all decks, board, nodes, and edges.
        """
        # Shuffle and prepare decks
        self.development_cards = self.generate_development_cards()
        self.resource_cards = self.generate_resource_cards()

        # Generate board tiles + store robber tile id + turn number
        self.robber_id = [0]
        self.board = self.generate_board(self.robber_id)
        self.turn = 0

        # Static definitions for vertices and edges
        self.nodes = self.create_nodes()
        self.edges = self.create_edges()

        # Generate player names
        self.players = self.generate_player_names()

        # Store largest army and longest road
        self.longest_road_player_id = "none"
        self.longest_road_length = 0
        self.largest_army_player_id = "none"

    # ----------------------------------------
    # Card List Generation
    # ----------------------------------------

    def generate_development_cards(self):
        """
        Build and shuffle the development card deck.

        Returns:
            list[str]: shuffled list of development cards
        """
        deck = []
        for card, count in self.DEVELOPMENT_CARDS_ALLOTMENT.items():
            deck.extend([card] * count)
        random.shuffle(deck)
        return deck

    def generate_resource_cards(self):
        """
        Returns a dict of resource + int count 

        Returns:
            dict[str: int] where keys are resource names and values are amount held in deck
        """
        return self.RESOURCES.copy()

    def generate_board(self, robber_id):
        """
        Generate a standard Settlers of Catan board.

        Returns:
        dict[int, list]: Mapping tile_id → [resource, token, dots, has_robber].
            - resource (str): one of RESOURCE_ALLOTMENT keys
            - token (int|None): number token (2–12 except 7), None for desert
            - dots (int): number of probability dots (0 for desert)
            - has_robber (bool): True only on the desert tile
        """
        # 1) Build and shuffle resource pool
        resources = []
        for res, count in self.RESOURCE_ALLOTMENT.items():
            resources.extend([res] * count)
        random.shuffle(resources)

        # 2) Shuffle number tokens (desert excluded)
        tokens = self.NUMBER_TOKENS.copy()
        random.shuffle(tokens)
    
        board = {}
        for tile_id, res in enumerate(resources, start=1):
            if res == "desert":
                board[tile_id] = [res, None, 0, True]
                robber_id[0] = tile_id
            else:
                number = tokens.pop()
                board[tile_id] = [res, number, self.DOTS[number], False]
        return board
    
    # ----------------------------------------
    # Roll, Robber, and other Game Mechanics
    # ----------------------------------------
    def roll_dice(self):
        """
        Simulate rolling two dice.
        
        Awards resources for nodes that are intersected with the rolled hexes and have a player settlement or city on them.
        
        Returns "robber" if a 7 is rolled.
        """

        # Helper method
        def award_resource(self, owner, resource, amount=1):
            """
            Take `amount` of `resource` cards from the bank and give them to `owner`.

            Args:
                owner    : a Player instance (just needs a .resource_cards dict)
                resource : str, one of "brick", "wood", "sheep", "wheat", "stone"
                amount   : int, how many cards to transfer
            """
            # 1) sanity‐check the bank
            if resource not in self.resource_cards:
                raise KeyError(f"Unknown resource '{resource}' in bank.")
            if self.resource_cards[resource] < amount:
                raise ValueError(
                    f"Bank is out of {resource}! "
                    f"(has {self.resource_cards[resource]}, needs {amount})"
                )

            # 2) remove from bank
            self.resource_cards[resource] -= amount

            # 3) deposit into player’s hand
            owner.resource_cards[resource] += amount

        valid_hexs = []
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total_roll = die1 + die2

        if total_roll == 7:
            return total_roll, ["robber"]
        else:
            valid_hexs = []
            for tile_id in self.board:
                resource, token, dots, has_robber = self.board[tile_id]
                if token == total_roll and not has_robber:
                    valid_hexs.append(tile_id)
        
        for tile_id in valid_hexs:
            for node_id, node_data in self.nodes.items():
               touching_tiles, (port, owner, building) = node_data
               if tile_id in touching_tiles and owner != "none":
                    for p in self.players:
                        if p.player_id == owner:
                            if building == "settlement":
                                award_resource(self, p, self.board[tile_id], amount=1)
                            else:
                                award_resource(self, p, self.board[tile_id], amount=2)


        return total_roll

    # ----------------------------------------
    # Node (vertex) definitions
    # ----------------------------------------

    def create_nodes(self):
        return {
            # Each node is a dict: node_id → [touching_tile_ids, [port, owner, building]]
            1:  [[1],            ["wheat", "none", "none"]],
            2:  [[1],            ["wheat", "none", "none"]],
            3:  [[1, 2],         ["none",  "none", "none"]],
            4:  [[2],            ["3:1",   "none", "none"]],
            5:  [[2, 3],         ["3:1",   "none", "none"]],
            6:  [[3],            ["none",  "none", "none"]],
            7:  [[3],            ["none",  "none", "none"]],
            8:  [[3, 4],         ["3:1",   "none", "none"]],
            9:  [[4],            ["3:1",   "none", "none"]],
            10: [[4, 5],         ["none",  "none", "none"]],
            11: [[5],            ["wood",  "none", "none"]],
            12: [[5],            ["wood",  "none", "none"]],
            13: [[5, 6],         ["none",  "none", "none"]],
            14: [[6],            ["3:1",   "none", "none"]],
            15: [[6, 7],         ["none",  "none", "none"]],
            16: [[7],            ["none",  "none", "none"]],
            17: [[7],            ["none",  "none", "none"]],
            18: [[7, 8],         ["sheep", "none", "none"]],
            19: [[8],            ["sheep", "none", "none"]],
            20: [[8, 9],         ["none",  "none", "none"]],
            21: [[9],            ["3:1",   "none", "none"]],
            22: [[9],            ["3:1",   "none", "none"]],
            23: [[9, 10],        ["none",  "none", "none"]],
            24: [[10],           ["rock",  "none", "none"]],
            25: [[10, 11],       ["rock",  "none", "none"]],
            26: [[11],           ["none",  "none", "none"]],
            27: [[11],           ["none",  "none", "none"]],
            28: [[11, 12],       ["brick", "none", "none"]],
            29: [[12],           ["brick", "none", "none"]],
            30: [[12, 1],        ["none",  "none", "none"]],
            31: [[1, 12, 13],    ["none",  "none", "none"]],
            32: [[1, 2, 13],     ["none",  "none", "none"]],
            33: [[2, 13, 14],    ["none",  "none", "none"]],
            34: [[2, 3, 14],     ["none",  "none", "none"]],
            35: [[3, 4, 14],     ["none",  "none", "none"]],
            36: [[4, 14, 15],    ["none",  "none", "none"]],
            37: [[4, 5, 15],     ["none",  "none", "none"]],
            38: [[5, 6, 15],     ["none",  "none", "none"]],
            39: [[6, 15, 16],    ["none",  "none", "none"]],
            40: [[6, 7, 16],     ["none",  "none", "none"]],
            41: [[7, 8, 16],     ["none",  "none", "none"]],
            42: [[8, 16, 17],    ["none",  "none", "none"]],
            43: [[8, 9, 17],     ["none",  "none", "none"]],
            44: [[9, 10, 17],    ["none",  "none", "none"]],
            45: [[10, 17, 18],   ["none",  "none", "none"]],
            46: [[10, 11, 18],   ["none",  "none", "none"]],
            47: [[11, 12, 18],   ["none",  "none", "none"]],
            48: [[12, 13, 18],   ["none",  "none", "none"]],
            49: [[13, 18, 19],   ["none",  "none", "none"]],
            50: [[13, 14, 19],   ["none",  "none", "none"]],
            51: [[14, 15, 19],   ["none",  "none", "none"]],
            52: [[15, 16, 19],   ["none",  "none", "none"]],
            53: [[16, 17, 19],   ["none",  "none", "none"]],
            54: [[17, 18, 19],   ["none",  "none", "none"]],
        }

    # ----------------------------------------
    # Edge definitions (road slots)
    # ----------------------------------------
    
    def create_edges(self):
        return {
            # Each edge is a dict: edge_id → [[connecting_node_ids], "none" or player_id]
            1:  [[1, 2],   "none"],
            2:  [[2, 3],   "none"],
            3:  [[3, 4],   "none"],
            4:  [[4, 5],   "none"],
            5:  [[5, 6],   "none"],
            6:  [[6, 7],   "none"],
            7:  [[7, 8],   "none"],
            8:  [[8, 9],   "none"],
            9:  [[9, 10],  "none"],
            10: [[10, 11], "none"],
            11: [[11, 12], "none"],
            12: [[12, 13], "none"],
            13: [[13, 14], "none"],
            14: [[14, 15], "none"],
            15: [[15, 16], "none"],
            16: [[16, 17], "none"],
            17: [[17, 18], "none"],
            18: [[18, 19], "none"],
            19: [[19, 20], "none"],
            20: [[20, 21], "none"],
            21: [[21, 22], "none"],
            22: [[22, 23], "none"],
            23: [[23, 24], "none"],
            24: [[24, 25], "none"],
            25: [[25, 26], "none"],
            26: [[26, 27], "none"],
            27: [[27, 28], "none"],
            28: [[28, 29], "none"],
            29: [[29, 30], "none"],
            30: [[30, 1],  "none"],
            31: [[31, 32], "none"],
            32: [[32, 33], "none"],
            33: [[33, 34], "none"],
            34: [[34, 35], "none"],
            35: [[35, 36], "none"],
            36: [[36, 37], "none"],
            37: [[37, 38], "none"],
            38: [[38, 39], "none"],
            39: [[39, 40], "none"],
            40: [[40, 41], "none"],
            41: [[41, 42], "none"],
            42: [[42, 43], "none"],
            43: [[43, 44], "none"],
            44: [[44, 45], "none"],
            45: [[45, 46], "none"],
            46: [[46, 47], "none"],
            47: [[47, 48], "none"],
            48: [[48, 31], "none"],
            49: [[49, 50], "none"],
            50: [[50, 51], "none"],
            51: [[51, 52], "none"],
            52: [[52, 53], "none"],
            53: [[53, 54], "none"],
            54: [[54, 49], "none"],
            55: [[30, 31], "none"],
            56: [[3, 32],  "none"],
            57: [[5, 34],  "none"],
            58: [[8, 35],  "none"],
            59: [[10, 37], "none"],
            60: [[13, 38], "none"],
            61: [[15, 40], "none"],
            62: [[18, 41], "none"],
            63: [[20, 43], "none"],
            64: [[23, 44], "none"],
            65: [[25, 46], "none"],
            66: [[28, 47], "none"],
            67: [[48, 49], "none"],
            68: [[33, 50], "none"],
            69: [[36, 51], "none"],
            70: [[39, 52], "none"],
            71: [[42, 53], "none"],
            72: [[45, 54], "none"],
        }
    # ----------------------------------------
    # Generate Player Names
    # ----------------------------------------
    def generate_player_names(self):
        return self.PLAYERS.copy()
# ----------------------------------------
# Example usage
# ----------------------------------------
#if __name__ == "__main__":
#    game = Game()
#    # Display the board layout
#    for tid, info in sorted(game.board.items()):
#        resource, token, dots, robber = info
#        print(f"Tile {tid:2d}: {resource:6s} | Token: {str(token):2s} | Dots: {dots} | Robber: {robber}")


