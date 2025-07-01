from enum import Enum

# Enumerate ActionType
class ActionType(Enum):
    BUILD_NODE_ID = "build_node_id"
    BUILD_EDGE_ID = "build_edge_id"

    RESOURCE_GIVE = "resource_give"
    RESOURCE_GET = "resource_get"
    RESOURCE_GET_EXTRA = "resource_get_extra"

    TARGET_PLAYER = "target_player"
    PORT = "port"
    SPECIAL_RESOURCE_GIVE = "special_resource_give"

    ROBBER_NODE_ID = "robber_node_id"

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cards = {
            # Resource cards
            'brick': 0,
            'wood': 0,
            'sheep': 0,
            'wheat': 0,
            'stone': 0,

            # Development cards
            'knight': 0,
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
        ActionType.BUILD_NODE_ID: int,
        ActionType.BUILD_EDGE_ID: int,

        # Development card data
        ActionType.RESOURCE_GIVE: '',
        ActionType.RESOURCE_GET: '',
        ActionType.RESOURCE_GET_EXTRA: '',

        # Trade data
        ActionType.TARGET_PLAYER: '',
        ActionType.PORT: '',
        ActionType.SPECIAL_RESOURCE_GIVE: '',

        # Other data
        ActionType.ROBBER_NODE_ID: int
        }

