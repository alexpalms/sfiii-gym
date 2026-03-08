from sfiii_gym.environment import Environment

env = Environment("env1", "./assets/rom", render_mode="human")
obs, info = env.reset()
while True:
    env.render()
    action = env.action_space.sample()
    frames, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        env.reset()
