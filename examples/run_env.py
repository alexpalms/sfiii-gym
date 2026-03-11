from sfiii_gym import Environment

env = Environment("env1", "./rom", render_mode="human", throttle=False)
obs, info = env.reset()
cumulative_reward = 0
while True:
    env.render()
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    cumulative_reward += reward
    print(f"Reward: {reward}, Cumulative Reward: {cumulative_reward}")
    if info["round_done"]:
        env.render()
    if terminated or truncated:
        env.reset()
        cumulative_reward = 0
