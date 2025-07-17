from typing import Optional
import gymnasium as gym
import random
import numpy as np
from core import game, player, actions

class CatanAgent(gym.Env): 

    def __init__(self):
        # Max number of possible actions
        # 144 action max occurs on first turn
        num_actions = 144

        # Define observation space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(gym.obs_dim,), dtype=np.float32)

        # Define action space
        self.action_space = gym.spaces.Discrete(num_actions)

        # Initialize players
        for name in self.catan_game.PLAYER_NAMES:
            self.catan_game.players.append(player.Player(name))

        self.current_player = None

        pass
    
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
        pass

    def step(self, action=None):
        """Execute one timestep within the environment.
        Args:
            action: The action to take
        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        reward = 0.0
        done = False
        truncated = False
        info = {}

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
                    return obs, reward, done, truncated, info
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
                    return obs, reward, done, False, info
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
                done = True
                obs = self._get_obs()
                info = self._get_info()
                return obs, reward, done, truncated, info

            if is_agent_turn:
                break

        obs = self._get_obs()
        info = self._get_info()
        return obs, reward, done, False, info

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

    def _get_obs(self):
        """Convert internal state to observation format.
        Returns:
            dict: Observation with agent and target positions
        """
        pass

    def _get_info(self):
        """Compute auxiliary information for debugging.
        Returns:
            dict: Info with distance between agent and target
        """
        pass

