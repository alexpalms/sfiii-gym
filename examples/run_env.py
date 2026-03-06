import random

from sfiii_gym.environment import Environment

env = Environment("env1")
env.start()
while True:
    move_action = random.randint(0, 8)
    attack_action = random.randint(0, 9)
    frames, reward, round_done, stage_done, game_done = env.step(
        move_action, attack_action
    )
    if game_done:
        env.new_game()
    elif stage_done:
        env.next_stage()
    elif round_done:
        env.next_round()
