import gymnasium as gym
import numpy as np
from Game import Game
from Actions import search_action, execute_action, ActionType

class CatanEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.game = None
        self.current_player = None

        # 1) Define fixed action space size
        #    e.g. max number of legal actions you’ll ever return from search_action
        self.max_actions = 200  
        self.action_space = gym.spaces.Discrete(self.max_actions)

        # 2) Define your observation space
        #    Here’s a simple example: a flat vector of
        #      - board tokens (19 ints), robber position (1 int)
        #      - for each player: 5 resource counts, victory points
        #    You’ll want to normalize or one-hot encode as appropriate.
        low  = np.zeros(19 + 1 + 4*(5+1), dtype=np.int32)
        high = np.full_like(low, 12)  # arbitrary cap
        self.observation_space = gym.spaces.Box(low, high, dtype=np.int32)

    def reset(self):
        # start a fresh game
        self.game = Game()
        # assign Player instances (your existing init logic in Main.py)
        for i in range(4):
            self.game.players[i] = Player.Player(self.game.players[i])
        self.current_player = 0

        # run the “start turns” phases automatically if you like,
        # or let the agent learn them too
        # …
        return self._get_obs()

    def step(self, action_idx):
        """Apply one action for the current player, advance turn or phase."""
        player = self.game.players[self.current_player]
        legal = search_action(player, self.game)
        if action_idx >= len(legal):
            # illegal action: you can either raise or treat as a no-op
            reward = -1
            done = False
            return self._get_obs(), reward, done, {"illegal": True}

        # execute it
        execute_action(legal, action_idx, player, self.game)
        # optionally check end-of-turn or forced phases:
        if not player.turn:
            # move to next player
            self.current_player = (self.current_player + 1) % 4

        # compute reward
        reward = self._compute_reward(player)

        # check for game over
        done = any(p.vic_points >= 10 for p in self.game.players)

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """Turn your game state into a single numeric vector."""
        obs = []
        # board tokens
        for tid in sorted(self.game.board):
            _, token, _, has_robber = self.game.board[tid]
            obs.append(token or 0)
        # robber position
        obs.append(self.game.robber_id[0])

        # player resources & VP
        for p in self.game.players[:4]:
            obs.extend([p.resource_cards[r] for r in ("brick","wood","sheep","wheat","stone")])
            obs.append(p.vic_points)

        return np.array(obs, dtype=np.int32)

    def _compute_reward(self, player):
        """Sparse: +1 on win, else 0.  You can shape more if you like."""
        if player.vic_points >= 10:
            return 1
        return 0
