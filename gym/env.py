from typing import Optional
import gymnasium as gym
import random
import numpy as np
from core import game, player, actions

class CatanEnv(gym.Env): 

    def __init__(self):
        # Max number of possible actions
        # CHANGE
        num_actions = 1000

        # Define observation space
        self.observation_space = gym.spaces.Dict({
            "player_state": gym.spaces.Box(low=0, high=100, shape=(14,), dtype=np.int32),
            "nodes": gym.spaces.Box(low=0, high=10, shape=(54,), dtype=np.int32),
            "edges": gym.spaces.Box(low=0, high=10, shape=(72,), dtype=np.int32),
            "tiles": gym.spaces.Box(low=0, high=10, shape=(19,), dtype=np.int32),
            "turn_index": gym.spaces.Discrete(200),
            "actions": gym.paces.Box(low=0, high=100, shape=(1000, 6), dtype=np.int32)
        })

        # Define action space
        self.action_space = gym.spaces.Discrete(num_actions)

        # Initialize players
        for name in self.catan_game.PLAYER_NAMES:
            self.catan_game.players.append(player.Player(name))
        
        # Initialize game
        self.catan_game = game.Game()

        self.current_player = None
    
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode.
        Args:
            seed: Random seed for reproducible episodes
            options: Additional configuration (unused in this example)
        Returns:
            tuple: (observation, info) for the initial state
        """
        # Initialize game
        self.catan_game = game.Game()
        
        self.agent_player = self.catan_game.players[random.randint(0, 3)]

        # Turn game state into numeric vector
        obs = self._get_obs()
        info = self._get_info()
        reward = 0.0
        terminated = False
        truncated = False

        return obs, reward, terminated, truncated, info

    def step(self, action=None):
        """Execute one timestep within the environment.
        Args:
            action: The action to take
        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        reward = 0.0
        terminated = False
        truncated = False

        # Setup phase
        if self.catan_game.turn_number <= 2 * len(self.catan_game.players):
            return self.setup_turns_logic(self, action)

        # Loop until agent's turn OR game is done
        while True:
            current_player = self.catan_game.players[self.catan_game.current_player_idx]
            is_agent_turn = current_player == self.agent_player

            # Begin turn (once per player)
            if not self.catan_game.turn_started:
                self.catan_game.begin_turn()
                roll = self.catan_game.last_roll
                if is_agent_turn:
                    obs = self._get_obs()
                    info = self._get_info()
                    return obs, reward, terminated, truncated, info
            else:
                roll = self.catan_game.last_roll

            # Robber turn
            if roll == "robber":
                action_list = actions.search_move_robber(current_player, self.catan_game)
            else:
                action_list = actions.search_action(current_player, self.catan_game)

            if is_agent_turn:
                if action is None:
                    # Agent needs to be given an action next step()
                    obs = self._get_obs()
                    info = self._get_info()
                    return obs, reward, terminated, False, info
                else:
                    # Wait for agent to act
                    actions.execute_action(action_list, action, current_player, self.catan_game)
            else:
                # Bot randomly selects
                bot_action = random.randint(0, len(action_list) - 1)
                actions.execute_action(action_list, bot_action, current_player, self.catan_game)

            # Check victory
            if self.catan_game.check_victory(current_player):
                reward = 1.0 if is_agent_turn else -1.0
                terminated = True
                obs = self._get_obs()
                info = self._get_info()
                return obs, reward, terminated, truncated, info
            
            # Check turn limit
            if self.catan_game.turn_number > 200:
                reward = 0.0
                terminated = True
                obs = self._get_obs()
                info = self._get_info()
                return obs, reward, terminated, truncated, info

            if is_agent_turn:
                break

        obs = self._get_obs()
        info = self._get_info()
        return obs, reward, terminated, truncated, info

    def _get_obs(self):
        """Convert internal state to observation format.
        Returns:
            dict
        """
        game = self.catan_game
        player = game.players[game.current_player_idx]

        return {
            # Player state: [pieces, resource cards, development cards, victory points, largest army, longest road]
            "player_state": self.encode_player_state(player),

            # Board state
            "nodes": self.encode_node_data(game.nodes),
            "edges": self.encode_edge_data(game.edges),
            "tiles": self.encode_board_data(game.board),

            # Game state
            "turn_index": game.turn_number,
            "actions": self.encode_action_data(actions.search_action(player, game))
        }

    def _get_info(self):
        """Compute auxiliary information for debugging.
        Returns:
            dict: 
        """
        pass


    # Helpers
    def setup_turns_logic(self, action=None):
        """Execute one timestep for the first two setup turns in Catan.
        Args:
            action: The action to take
        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        reward = 0.0
        done = False
        truncated = False
        info = {}

        while True:
            current_player = self.catan_game.players[self.catan_game.current_player_idx]
            is_agent_turn = current_player == self.agent_player

            if is_agent_turn:
                if action is None:
                    # Agent needs to be given an action next step()
                    obs = self.catan_game.get_observation()
                    return obs, reward, done, truncated, info
                else:
                    # Agent acts now
                    action_list = actions.search_action(current_player, self.catan_game)
                    actions.execute_action(action_list, action, current_player, self.catan_game)
                    self.catan_game.finish_turn()
            else:
                # Bot acts
                action_list = actions.search_action(current_player, self.catan_game)
                bot_action = random.randint(0, len(action_list) - 1)
                actions.execute_action(action_list, bot_action, current_player, self.catan_game)
                self.catan_game.finish_turn()

            # Setup is finished after 2N turns
            if self.catan_game.turn_number > 2 * len(self.catan_game.players):
                break

        obs = self.catan_game.get_observation()
        return obs, reward, done, truncated, info
    
    def encode_player_state(self, p: player.Player):
        """Numerically encodes player state to an array.
        Args:
            p: Player
        Returns:
            Array: [total cities/settlements, total resource cards, total development cards, victory points]
        """

        total_pieces = 0
        for name, data in p.pieces:
            if name != "roads":
                total_pieces += data

        total_resources = 0
        for name, data in p.resource_cards:
            total_resources += data
        
        total_development_cards = 0
        for name, data in p.development_cards:
            total_development_cards += data

        player_state = [total_pieces, total_resources, total_development_cards, p.vic_points]

        return np.array(player_state)

    def encode_node_data(nodes_dict: dict):
        """Numerically encodes node dictionary to an array.
        Args:
            nodes_dict: Nodes dictionary
        Returns:
            2DArray: [tile_1, tile_2, tile_3, port, owner, building]
        """

        PORT_MAP = {
            "none": 0, "3:1": 1, "wheat": 2, "wood": 3,
            "sheep": 4, "brick": 5, "rock": 6
        }
        BUILDING_MAP = {
            "none": 0, "settlement": 1, "city": 2
        }
        OWNER_MAP = {
            "none": 0, "p1": 1, "p2": 2, "p3": 3, "p4": 4
        }

        node_data = []

        for i in range(1, 55):  # Node ids 1 to 54
            tiles, [port, owner, building] = nodes_dict[i]

            tiles_encoded = tiles + [-1] * (3 - len(tiles))  # pad to 3 tiles
            port_encoded = PORT_MAP[port]
            owner_encoded = OWNER_MAP[owner]
            building_encoded = BUILDING_MAP[building]

            node_vector = tiles_encoded + [port_encoded, owner_encoded, building_encoded]
            node_data.append(node_vector)

        return np.array(node_data)
    
    def encode_edge_data(edges_dict: dict):
        """Numerically encodes edge dictionary to an array.
        Args:
            edges_dict: Edges dictionary
        Returns:
            2DArray: [int, resource, token, dots, has_robber]
        """

        OWNER_MAP = {
            "none": 0, "p1": 1, "p2": 2, "p3": 3, "p4": 4
        }
        
        edge_data = []

        for i in range(1, 73):  # Edge ids 1 to 72
            nodes, owner = edges_dict[i]

            nodes_encoded = nodes
            owner_encoded = OWNER_MAP[owner]
            

            edge_vector = nodes_encoded + [owner_encoded]
            edge_data.append(edge_vector)

        return np.array(edge_data)
    
    def encode_board_data(board_dict: dict):
        """Numerically encodes board dictionary to an array.
        Args:
            board_dict: board dictionary
        Returns:
            2DArray: [int, resource, token, dots, has_robber]
        """
        
        RESOURCE_MAP = {
            "wheat": 1, "wood": 2,
            "sheep": 3, "brick": 4, "rock": 5
        }

        tile_data = []

        for i in range(1, 73):  # Edge ids 1 to 72
            int, [resource, token, dots, has_robber] = board_dict[i]

            int_encoded = int
            resource_encoded = RESOURCE_MAP[resource]
            token_encoded = token
            dots_encoded = dots
            robber_encoded = int(has_robber)

            tile_vector = [int_encoded, resource_encoded, token_encoded, dots_encoded, robber_encoded]
            tile_data.append(tile_vector)

        return np.array(tile_data)
    
    def encode_action_data(action_list: list):
        ACTION_TYPE_MAP = {
            'ActionType.START_TURNS': 1,

            'ActionType.BUILD_ROAD': 2,
            'ActionType.BUILD_SETTLEMENT': 3,
            'ActionType.BUILD_CITY': 4,
            'ActionType.BUY_DEV_CARD': 5,

            'ActionType.USE_KNIGHT': 6,
            'ActionType.USE_BUILDROAD': 7,
            'ActionType.USE_MONOPOLY': 8,
            'ActionType.USE_YEAROFPLENTY': 9,

            'ActionType.TRADE_BANK': 10,
            'ActionType.TRADE_PORT': 11,
            # 'ActionType.TRADE_PLAYER': trade_player,

            'ActionType.MOVE_ROBBER': 12,
            'ActionType.END_TURN': 13
        }
        
        ACTION_DATA_MAP = {
            'BUILD_NODE_ID': 1,
            'BUILD_EDGE_ID': 2,
            'BUILD_EDGE_EXTRA_ID': 3,

            'RESOURCE_GIVE': 4,
            'RESOURCE_GET': 5,
            'RESOURCE_GET_EXTRA': 6,

            'TARGET_PLAYER': 7,
            'PORT': 8,

            'ROBBER_TILE_ID': 9,
            'ROBBER_PLAYER_TARGET': 10
        }
        actions_list_encoded = []
        
        for action in action_list:
            
            action_type = ACTION_TYPE_MAP[action.type]
            action_data = []

            for key, value in action.data:
                action_data.append(ACTION_DATA_MAP[key])
                action_data.append(value)

            action_vector = [action_type] + action_data

            if len(action_vector) < 5:
                action_vector += [0, 0]

            actions_list_encoded.append(action_vector)
        
        return np.array(actions_list_encoded)
    