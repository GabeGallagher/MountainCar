import gym
import random
import numpy as np

"""
Mountain Car is an interesting problem because, unlike frozen lake,
there is no value function. Rather, this sim is continuous, so does
not have states similar to what I've worked with previously. My 
initial plan is to create some sort of threshold where if the car
is in a certain location, the agent will treat it as if that is
close enough to another region and round
"""

"""
returns 
"""


def get_rounded_state(rounder, n):
    n = round(n, rounder + 1)
    last_digit = (abs(n) % 10 ** (-rounder)) * 10 ** (rounder + 1)
    if last_digit != 5:
        n = round(n, rounder)

    return n


"""
returns an action when given a state and a rounding threshold.
Memories are optional and exist in the following structure:
    dict: { "location, velocity" : visit_count }
"""


def get_memory_action(state, pos_rounder, vel_rounder, mem=None):
    # apply round threshold
    key = str(get_rounded_state(pos_rounder, state[0])) + ", " + \
          str(get_rounded_state(vel_rounder, state[1]))

    if mem is None:
        mem = {}

    if key in mem:
        mem[key] += 1
        action = np.argmax(val_func[key])
    else:
        mem[key] = 1
        action = random.randint(0, 2)

    return mem, action


"""
The basic idea of a playthrough is to make a series of moves that
hopefully push the car to the top of the mountain. The agent can
push right, left, or do nothing. To make a move, it should first
look at the velocity and location of the car and decide what to do
if it is unsure what to do, it should take an action at random, and
observe the results.
"""


def playthrough(local_mem, pos_rounder, vel_rounder):
    # look at current position and velocity
    state = game.reset()
    # see if has an idea of what to do in this state
    local_mem, action = get_memory_action(state, pos_rounder, vel_rounder, local_mem)
    total_reward = 0
    is_done = False

    while not is_done:
        # if it does, decide whether to perform a previous action,
        # or a random one
        state, reward, is_done, _ = game.step(action)
        local_mem, action = get_memory_action(state, pos_rounder, vel_rounder, local_mem)

        # evaluate move
        total_reward += reward

    for state in local_mem:
        for action in state:
            key = str(state) + ", " + str(action)


if __name__ == "__main__":
    # init environment
    game = gym.make("MountainCar-v0")
    memory = {}
    val_func = {}

    # play game
    playthrough(memory, 1, 2)

    game.close()
