import random


class CatanGame:
    """
    A class encapsulating the components of a Settlers of Catan game:
      - Development card deck
      - Resource card decks
      - Hex board layout with tokens and robber
      - Vertex (node) definitions for settlements/ports
      - Edge definitions for possible roads
    """

    # ----------------------------------------
    # Class-level constants
    # ----------------------------------------
    PLAYERS = ["P1", "P2", "P3", "P4", "none"]

    DEVELOPMENT_CARDS_ALLOTMENT = {
        "knight": 14,
        "vic_point": 5,
        "build_road": 2,
        "year_of_plenty": 2,
        "monopoly": 2
    }

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

    def __init__(self):
        """
        Initialize the game by generating all decks, board, nodes, and edges.
        """
        # Shuffle and prepare decks
        self.development_cards = self._generate_development_cards()
        self.resource_cards = self._generate_resource_cards()

        # Generate board layout (tiles)
        self.board = self.generate_board()

        # Static definitions for vertices and edges
        self.nodes = self._init_nodes()
        self.edges = self._init_edges()

    def _generate_development_cards(self):
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

    def _generate_resource_cards(self):
        """
        Build separate decks for each resource type.

        Returns:
            dict[str, list[str]]: mapping resource name to its card list
        """
        decks = {}
        for resource, count in self.RESOURCES.items():
            decks[f"{resource}_cards"] = [resource] * count
        return decks

    def generate_board(self):
        """
        Generate a standard Catan board with resources, tokens, dots, and robber.

        Returns:
            dict[int, list]: tile_id → [resource, token, dots, has_robber]
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
            else:
                number = tokens.pop()
                board[tile_id] = [res, number, self.DOTS[number], False]
        return board

    def _init_nodes(self):
        """
        Return the static list of vertices (nodes) for settlement placement.

        Each node dict: node_id → [touching_tile_ids, [port, owner, building]]
        """
        return [
            {1:  [[1],            ["wheat", "none", "none"]]},
            {2:  [[1],            ["wheat", "none", "none"]]},
            {3:  [[1, 2],         ["none",  "none", "none"]]},
            # ... continued through node 54 ...
            {54: [[17, 18, 19],   ["none",  "none", "none"]]}
        ]

    def _init_edges(self):
        """
        Return the static list of edges (roads) between nodes.

        Each edge dict: edge_id → [[node_a, node_b], owner]
        """
        return [
            {1:  [[1, 2],   "none"]},
            {2:  [[2, 3],   "none"]},
            {3:  [[3, 4],   "none"]},
            # ... continued through edge 72 ...
            {72: [[45, 54], "none"]},
        ]

# ----------------------------------------
# Example usage
# ----------------------------------------
if __name__ == "__main__":
    game = CatanGame()
    # Display the board layout
    for tid, info in sorted(game.board.items()):
        resource, token, dots, robber = info
        print(f"Tile {tid:2d}: {resource:6s} | Token: {str(token):2s} | Dots: {dots} | Robber: {robber}")
