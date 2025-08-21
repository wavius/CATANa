from gym.agent import CatanAgent
from gym.env import CatanEnv
import gymnasium as gym
from tqdm import tqdm  # Progress bar


# Training hyperparameters
learning_rate = 0.01                              # How fast to learn (higher = faster but less stable)
n_episodes = 1                                    # Number of hands to practice
start_epsilon = 1.0                               # Start with 100% random actions
epsilon_decay = start_epsilon / (n_episodes / 2)  # Reduce exploration over time
final_epsilon = 0.1                               # Always keep some exploration

# Create environment and agent
env = CatanEnv()
env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)

agent = CatanAgent(
    env=env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

for episode in tqdm(range(n_episodes)):
    # Start a new game
    obs, info = env.reset()
    done = False

    print("\nAgent:", env.env.agent_player.id)
    print("-----")

    # Play setup turns
    while env.env.catan_game.turn_number <= 2 * len(env.env.catan_game.players):

        action = agent.get_action(obs)
        # Take action and observe result
        next_obs, reward, terminated, truncated, info = env.step(action)

        # Learn from this experience
        agent.update(obs, action, reward, terminated, next_obs)

        for i in range(0,5):
            next_obs, reward, terminated, truncated, info = env.step(None)
            done = terminated or truncated
            obs = next_obs

    # Play one game
    while not done:
        
        next_obs, reward, terminated, truncated, info = env.step(None)
        action = agent.get_action(obs)
        # Take action and observe result
        next_obs, reward, terminated, truncated, info = env.step(action)

        # Learn from this experience
        agent.update(obs, action, reward, terminated, next_obs)

        for i in range (0, 3):
            next_obs, reward, terminated, truncated, info = env.step(None)

        # Move to next state
        done = terminated or truncated
        obs = next_obs


    # Reduce exploration rate (agent becomes less random over time)
    agent.decay_epsilon()