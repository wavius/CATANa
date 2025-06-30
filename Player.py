from Actions import *
from enum import Enum

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
        self.vic_points = int
        self.pieces = {
            'settlements': 5,
            'cities': 4,
            'roads': 15
        }


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

    ActionType.TRADE_BANK: tradebank,
    ActionType.TRADE_PORT: tradeport,
    # ActionType.TRADE_PLAYER: tradeplayer,

    # ActionType.MOVE_ROBBER: moverobber,
    # ActionType.END_TURN: end_turn
}


# Method to execute general action
def execute_action(player, board, action_data, action_type):
    ACTIONS[action_type](player, board, action_data)

