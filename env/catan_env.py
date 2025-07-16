from typing import Optional
import gymnasium as gym
import random
from core import game, player, actions

class CatanEnv(gym.Env):

    def __init__(self):
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

        # Initialize players
        for i in range(4):
            self.catan_game.players[i] = player.Player(self.catan_game.players[i])
        
        self.current_player = None
        self.agent_player = self.cata_game.players[random.randint(0, 3)]

        # Turn game state into numeric vector
        pass

  
    def step(self, action=None):
        reward = 0.0
        done = False
        info = {}

        # Setup phase
        if self.catan_game.turn_number < 2 * len(self.catan_game.players):
            self.catan_game.turn_number += 1
            return self.snake_setup_logic()

        current_player = self.catan_game.players[self.catan_game.current_player_idx]
        is_agent_turn = current_player == self.agent_player

        # Begin turn (once per turn)
        if not self.catan_game.turn_started:
            self.catan_game.begin_turn()
            roll = self.catan_game.last_roll 
            if is_agent_turn:
                # Agent must now decide action on next step()
                obs = self.catan_game.get_observation()
                return obs, reward, done, False, info
        else:
            roll = self.catan_game.last_roll  # Already rolled

        # Robber turn
        if roll == "robber":
            if is_agent_turn:
                action_list = actions.search_move_robber(current_player, self.catan_game)
                actions.execute_action(action_list, action, current_player, self.catan_game)
            else:
                action_list = actions.search_move_robber(current_player, self.catan_game)
                bot_action = random.randint(0, len(action_list) - 1)
                actions.execute_action(action_list, bot_action, current_player, self.catan_game)

        # Normal turn
        else:
            if is_agent_turn:
                action_list = actions.search_action(current_player, self.catan_game)
                actions.execute_action(action_list, action, current_player, self.catan_game)
            else:
                action_list = actions.search_action(current_player, self.catan_game)
                bot_action = random.randint(0, len(action_list) - 1)
                actions.execute_action(action_list, bot_action, current_player, self.catan_game)

        # Victory check
        if self.catan_game.check_victory(current_player):
            reward = 1.0 if is_agent_turn else -1.0
            done = True

        obs = self.catan_game.get_observation()
        return obs, reward, done, False, info





    def setup_turns_logic(self):
        pass

