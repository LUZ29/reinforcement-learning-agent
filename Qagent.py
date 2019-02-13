from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w, K_a, K_F15
import ast
import os


# import random


class NaiveAgent():
    def __init__(self, actions):
        self.actions = actions
        self.step = 0
        self.NOOP = K_F15

        self.alpha = 0.99
        self.gamma = 0.9
        self.const = 0.1
        self.strolling = 5000

    def init(self, obs):

        current_state = AgentState(obs)
        if os.path.exists("NTABLE.txt"):
            old_table = open("NTABLE.txt", 'r')
            data = old_table.read()
            self.current_n_table = ast.literal_eval(data)
            old_table.close()
        else:
            self.current_n_table = {}
            for act in self.actions:
                state = str((current_state.getState(), act))
                self.current_n_table[state] = 1
            # print self.current_n_table

        if os.path.exists("QTABLE.txt"):
            old_table = open("QTABLE.txt", 'r')
            data = old_table.read()
            self.current_q_table = ast.literal_eval(data)
            old_table.close()
        else:
            self.current_q_table = {}
            for act in self.actions:
                state = str((current_state.getState(), act))
                self.current_q_table[state] = 0 + self.const / self.current_n_table[state]
            # print self.current_q_table

    # choose an action which has highest value in table
    def pickAction(self, reward, obs):
        # if random.random()>0.98:
        #     return self.actions[np.random.randint(0, len(self.actions))]

        current_state = AgentState(obs)
        next_act = self.actions[np.random.randint(0, len(self.actions))]
        next_state = str((current_state.getState(), next_act))
        for act in self.actions:
            state = str((current_state.getState(), act))
            if self.current_q_table[state] > self.current_q_table[next_state]:
                next_state = state
                next_act = act
        self.current_n_table[next_state] += 0.5
        # self.step += 1
        # return self.actions[4]
        return next_act

        # return self.NOOP
        # Uncomment the following line to get random actions
        # return self.actions[np.random.randint(0,len(self.actions))]

    # revise q/n table
    def learning(self, a, reward, obs, next_r, next_s):
        current_state = AgentState(obs)
        # if self.step > self.strolling:
        #     current_state.tooMuchSteps = True
        #     s = str(((current_state.getState()), a))
        #     old_q_table = self.current_q_table
        #     q_sample = next_r + self.gamma * next_s
        #     self.alpha = 1.000000 / self.current_n_table[s]
        #     self.current_q_table[s] = old_q_table[s] + self.alpha * (q_sample - old_q_table[s])
        #     self.current_n_table[s] += 1
        #     agent.save_table()
        #     self.step = 0
        #     p.reset_game()
        #     return
        s = str(((current_state.getState()), a))
        old_q_table = self.current_q_table
        q_sample = reward + self.gamma * next_s
        # print "qsample",q_sample
        # print "n",self.current_n_table[s]
        self.alpha = 1.000000 / self.current_n_table[s]
        # print "alpha",float(self.alpha)
        self.current_q_table[s] = old_q_table[s] + self.alpha * (q_sample - old_q_table[s])
        # print "sample-old", (q_sample - old_q_table[s]) #0.01
        # print "self.q last", self.alpha * (q_sample - old_q_table[s])
        # print "old", old_q_table[s]
        self.current_n_table[s] += 1
        # self.save_table()
        return

    # get s2, if there is not, create one.
    def getNextState(self, obs):
        current_state = AgentState(obs)
        next_act = self.actions[np.random.randint(0, len(self.actions))]
        next_r = 0
        # if agent.step > self.strolling:
        #     next_r = -1.0
        #     current_state.tooMuchSteps = True
        next_state = str((current_state.getState(), next_act))

        if next_state not in self.current_q_table.keys():
            self.current_n_table[next_state] = 1
            self.current_q_table[next_state] = 0 + self.const / self.current_n_table[next_state]
        for act in self.actions:
            state = str((current_state.getState(), act))
            if state not in self.current_q_table.keys():
                self.current_n_table[state] = 1
                self.current_q_table[state] = 0 + self.const / self.current_n_table[state]
            if self.current_q_table[state] > self.current_q_table[next_state]:
                next_state = state
        return self.current_q_table[next_state], next_r

    # see do we need to create the next state
    def observeState(self, next_obs, a):
        next_state = AgentState(next_obs)
        state = str((next_state.getState(), a))
        # print "observeState",state
        if state in self.current_q_table.keys():
            return True, state
        return False, state

    # save the revised q/n table
    def save_table(self):
        new_table = open("QTABLE.txt", 'w')
        new_table.write(str(self.current_q_table))
        new_table.close()
        new_table = open("NTABLE.txt", 'w')
        new_table.write(str(self.current_n_table))
        new_table.close()
        return


class AgentState():
    def __init__(self, obs):
        # x = obs['frog_x']

        self.right = 5
        self.left = 5
        self.front = True
        self.back = True
        # self.tooMuchSteps = False

        # detect agent's surrounding
        if obs['frog_y'] > 260:  # int(obs['cars'][-1][1] / 2) + int(obs['rivers'][0][1] / 2): # 229.0:
            self.water = False
            # self.home_entry = []
            for car in obs['cars']:
                # dist_y = car[1] - obs['frog_y']
                # absdist_y = abs(car[1] - obs['frog_y'])
                if abs(car[1] - obs['frog_y']) < 40:
                    if abs(car[1] - obs['frog_y']) < 10:
                        if car[0] < obs['frog_x']:
                            self.left = min(int((obs['frog_x'] - car[0] - car[2]) / 24), self.left)
                        else:
                            self.right = min(int((car[0] - obs['frog_x'] - 24) / 24), self.right)
                    else:
                        if car[1] - obs['frog_y'] < 0:
                            if (car[0] < obs['frog_x']) and (obs['frog_x'] - car[0] - car[2] <= 24):
                                self.front = False
                            if (car[0] >= obs['frog_x']) and (car[0] - obs['frog_x'] <= 24):
                                self.front = False
                        else:
                            if (car[0] < obs['frog_x']) and (obs['frog_x'] - car[0] - car[2] <= 24):
                                self.back = False
                            if (car[0] >= obs['frog_x']) and (car[0] - obs['frog_x'] <= 24):
                                self.back = False
        else:
            self.water = True
            # self.home_entry = obs['homes']
            for obj in obs['rivers']:
                # dist_y = obj[1] - obs['frog_y']
                # absdist_y = abs(obj[1] - obs['frog_y'])
                if abs(obj[1] - obs['frog_y']) < 40:
                    if abs(obj[1] - obs['frog_y']) < 10:
                        if obj[0] < obs['frog_x']:
                            self.left = min(int((obs['frog_x'] - obj[0]) / 24), self.left)
                        if obj[0] + obj[2] > obs['frog_x']:
                            self.right = min(int((obj[0] + obj[2] - obs['frog_x']) / 24), self.right)
                    else:
                        if (obj[1] - obs['frog_y']) < 0:
                            if (obj[0] < obs['frog_x']) and (obs['frog_x'] - obj[0] + 24 <= obj[2]):
                                self.front = False
                        else:
                            if (obj[0] < obs['frog_x']) and (obs['frog_x'] - obj[0] + 24 <= obj[2]):
                                self.back = False

        # detect homes situation when agent is close
        self.home_entry = None
        if obs['frog_y'] < 130.0:  # (obs['homeR'][0][1]*2):  # 101.0
            temp = 500
            for home in obs['homeR']:
                if (home[0] < obs['frog_x']) and (obs['frog_x'] < home[0] + home[2]):  # whether there is a door
                    self.front = False
                for i in obs['homes']:
                    if abs((home[0] + home[2] / 2) - obs['frog_x']) < temp:
                        temp = abs((home[0] + home[2] / 2) - obs['frog_x'])
                        self.home_entry = i
                    if abs((home[0] + home[2] / 2) - obs['frog_x']) == temp:
                        self.home_entry = None

    def getState(self):
        return (self.water, self.left, self.right, self.front, self.back, self.home_entry)#, self.tooMuchSteps)


game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps, force_fps=False)
obs = game.getGameState()
agent = NaiveAgent(p.getActionSet())
agent.init(obs)
# print type(p.getActionSet())
reward = 0.0
fail = 0
win = 0
# p.init()


while True:
    if p.game_over():
        # agent.step = 0
        print game.score
        p.reset_game()

    obs = game.getGameState()
    # print obs
    action = agent.pickAction(reward, obs)
    reward = p.act(action)
    # print reward
    next_obs = game.getGameState()
    # print "next", next_obs
    # next_r, next_s = agent.getNextState(next_obs)
    next_s, next_r = agent.getNextState(next_obs)
    agent.learning(action, reward, obs, next_r, next_s)

    # print reward
    # print game.score
