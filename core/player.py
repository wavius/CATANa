from enum import Enum

# Enumerate ActionData
class ActionData(Enum):
    """
    A class containining action enums
    """
    BUILD_NODE_ID = "build_node_id"
    BUILD_EDGE_ID = "build_edge_id"
    BUILD_EDGE_EXTRA_ID = "build_edge_extra_id"

    RESOURCE_GIVE = "resource_give"
    RESOURCE_GET = "resource_get"
    RESOURCE_GET_EXTRA = "resource_get_extra"

    TARGET_PLAYER = "target_player"
    PORT = "port"

    ROBBER_TILE_ID = "robber_tile_id"
    ROBBER_PLAYER_TARGET = "robber_player_target"

class Player:
    """
    A class containining player information:
      - Player ID
      - Turn
      - Resource cards
      - Development cards
      - Victory points
      - Pieces
      - Action data
    """

    def __init__(self, player_id):
        self.id = player_id
        self.turn = True
        self.resource_cards = {
            # Resource cards
            'brick': 0,
            'wood': 0,
            'sheep': 0,
            'wheat': 0,
            'stone': 0,
        }
        self.development_cards = {
            # Development cards
            'knight': 0,
            'used_knight': 0,
            'vic_point': 0,
            'build_road': 0,
            'year_of_plenty': 0,
            'monopoly': 0
        }
        self.vic_points = 0
        self.pieces = {
            'settlements': 5,
            'cities': 4,
            'roads': 15
        }

        # Data for all possible actions
        self.action_data = {
            # Building data
            ActionData.BUILD_NODE_ID: int,
            ActionData.BUILD_EDGE_ID: int,
            ActionData.BUILD_EDGE_EXTRA_ID: int,

            # Development card data
            ActionData.RESOURCE_GIVE: str,
            ActionData.RESOURCE_GET: str,
            ActionData.RESOURCE_GET_EXTRA: str,

            # Trade data
            ActionData.TARGET_PLAYER: str,
            ActionData.PORT: str,
            ActionData.SPECIAL_RESOURCE_GIVE: str,

            # Other data
            ActionData.ROBBER_TILE_ID: int,
            ActionData.ROBBER_PLAYER_TARGET: str
        }

