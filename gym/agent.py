import collections as defaultdict
import gymnasium as gym
import numpy as np
import random

class CatanAgent:
    def __init__(
        self,
        env: gym.Env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95
    ):
        """Initialize a Q-Learning agent.
        Args:
            env: The training environment
            learning_rate: How quickly to update Q-values (0-1)
            initial_epsilon: Starting exploration rate (usually 1.0)
            epsilon_decay: How much to reduce epsilon each episode
            final_epsilon: Minimum exploration rate (usually 0.1)
            discount_factor: How much to value future rewards (0-1)
        """

        self.env = env

        # Q-table: maps (state, action) to expected reward
        # defaultdict automatically creates entries with zeros for new states
        ### MUST BE CHANGED
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))

        self.learning_rate = learning_rate
        self.initial_epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.discount_factor = discount_factor

        self.training_error = []

    def get_action(self, obs: dict) -> int:
        """Choose an action using epsilon-greedy strategy.

        Returns:
            action: Index of chosen action vector 
        """
        legal_actions = obs["actions"]
        state_key = self.encode_state(obs)

        # Explore
        if np.random.random() < self.epsilon:
            return random.choice(legal_actions)

        # Exploit
        q_values = []
        for action in legal_actions:
            action_key = tuple(action)
            q_values.append(self.q_values[(state_key, action_key)])

        best_idx = int(np.argmax(q_values))
        action_idx = obs["actions"].index(legal_actions[best_idx])

        return action_idx
            
    def update(
            self,
            obs: dict,
            action: np.ndarray,
            reward: float,
            terminated: bool,
            next_obs: dict,
        ):
            """Update Q-value based on experience with vector actions and dict obs."""

            # Convert to hashable keys
            state_key = self.encode_state(obs)
            next_state_key = self.encode_state(next_obs)
            action_key = tuple(action)

            # Get best Q-value for next state
            future_q_value = 0.0
            if not terminated:
                next_actions = next_obs["actions"]
                future_q_value = max(
                    self.q_values[(next_state_key, tuple(a))] for a in next_actions
                )

            # Target Q-value using Bellman equation
            target = reward + self.discount_factor * future_q_value

            # TD error and Q-value update
            q_key = (state_key, action_key)
            td_error = target - self.q_values[q_key]
            self.q_values[q_key] += self.lr * td_error

            # Track training error
            self.training_error.append(td_error)

    def encode_state(self, obs: dict) -> tuple:
        """Turn dict obs into a hashable state key."""
        return (
            tuple(obs["player_state"])
        )

    def decay_epsilon(self):
        """Reduce exploration rate after each episode."""
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)