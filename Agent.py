#!/usr/bin/python
# coding=UTF-8
import random

class Agent:
    """The learning agent"""
    def __init__(self, pieces):
        self.available_actions = [
            "move_eye_one_step_north",
            "move_eye_one_step_south",
            "move_eye_one_step_east",
            "move_eye_one_step_west"
        ]
        self.pieces = pieces

if __name__ == "__main__":
    agent = Agent()
    
    random_action = random.randint(0, len(agent.available_actions) - 1)
    print "Chosen random action: " + agent.available_actions[random_action]
