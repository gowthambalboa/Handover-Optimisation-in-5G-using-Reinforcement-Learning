import numpy as np
import random
import matplotlib.pyplot as plt
Rows = 3
Cols = 6
Start = (2,0)
# Start_Position = (2,0)
Goal = (0,5)
# Goal_Position = (0,5)
Antennas={
    "A2":{
       "position": (2,1),
       "Range":[(2,0),(1,1),(2,2),(1,0),(1,2),(2,1)]
    },
    "A1":{
        "position":(0,0),
        "Range":[(1,0),(1,1),(0,1),(0,0)]
    },
    "A3":{
        "position":(0,2),
        "Range":[(0,1),(1,1),(1,2),(1,3),(0,3),(0,2)]
    },
    "A4":{
        "position":(1,3),
        "Range":[(0,2),(1,2),(2,2),(2,3),(2,4),(1,4),(0,4),(0,3),(1,3)]
    },
    "A5":{
        "position":(0,4),
        "Range":[(0,3),(1,3),(1,4),(1,5),(0,5),(0,4)]
    },
    "A6":{
        "position":(2,5),
        "Range":[(1,4),(2,4),(1,5),(2,5)]
    }
    }
pos =[(0,0),(2,1),(0,2),(1,3),(0,4),(2,5)]
signal_availability = dict()
lis = []
for r in range(Rows):
  for c in range(Cols):
    for i in Antennas.keys():
      for j in Antennas[i]["Range"]:
       if j == (r,c):
        lis.append(i)
    signal_availability.update({(r,c):lis})
    lis = []
# print (signal_availability)
Actions = ['r','u','l','d']
# Q1 = {}
# for r in range(Rows):
#   for c in range(Cols):
#     for i in signal_availability.keys():
#       if i == (r,c):
#         for a in signal_availability[i]:
#           Q1[(r,c,a)] = {}
#           for action in Actions:
#             Q1[(r,c,a)][action] = 0

Q = {}
# for r in range(Rows):
#   for c in range(Cols):
#     Q2[(r,c)] = {}
#     for i in signal_availability.keys():
#       if i == (r,c):
#         for a in signal_availability[i]:
#           Q2[(r,c)][a] = 0

# print(Q1)
# print("Q2: {}".format(Q))

class GridWorld:

    def __init__(self):
        self.action_space = Actions
        self.rows = Rows
        self.cols = Cols
        self.state = Start
        self.Start = Start

        self.Goal = Goal

        self.Antennas = Antennas
        self.done = False
        self.grid = np.zeros((self.rows, self.cols))
        self.grid[self.Goal] = 2
        for i in pos:
            self.grid[i] = -1

    def reset(self):
        self.state = Start
        self.done = False

    def step(self, action, antenna, eps):
        r, c = self.state
        old_antenna = antenna
        if action == 'u':
            r -= 1
        elif action == 'd':
            r += 1
        elif action == 'r':
            c += 1
        elif action == 'l':
            c -= 1

        if np.random.rand() < eps:
            for i in signal_availability.keys():
                if i == (r, c):
                    antenna = random.choice(signal_availability[i])
        else:
            for i in signal_availability.keys():
                if i == (r, c):
                    antenna = max(Q[(r, c)], key=Q[(r, c)].get)

        new_antenna = antenna

        if r >= 0 and r <= self.rows - 1 and c >= 0 and c <= self.cols - 1:
            self.state = (r, c)

        # if self.state == self.Goal:
        #   reward = 100
        #   handover = 0
        #   self.done = True

        # else:

        if old_antenna != new_antenna:
            reward = -1  # Handover
            handover = 1
        else:
            reward = 1  # No Handover
            handover = 0

        return self.state, reward, handover, self.done, None

    def ShowGrid(self):
        self.grid[self.Start] = 1
        for r in range(self.rows):
            print(' -------------------------')
            output = ''
            for c in range(self.cols):
                if self.grid[r, c] == 1:
                    value = 'M'
                elif self.grid[r, c] == 0:
                    value = '0'
                elif self.grid[r, c] == -1:
                    value = 'A'
                elif self.grid[r, c] == 2:
                    # value = 'G'
                    value = '0'  # As we are not considering Goal position
                output += ' | ' + value
            print(output + ' | ')
        print(' -------------------------')


# print('Here is the grid:')
# print('M: position of the agent,  A: Antenna')
# GridWorld().ShowGrid()

class Agent:
  def __init__(self):

    #self.state = State
    self.rows = Rows
    self.cols = Cols
    self.actions = Actions
    self.Model = {}

    #Q-table initializetion

    # self.Q = {}
    # for r in range(self.rows):
    #   for c in range(self.cols):
    #     for i in signal_availability.keys():
    #       if i == (r,c):
    #         for a in signal_availability[i]:
    #           self.Q[(r,c,a)] = {}
    #           for action in self.actions:
    #             self.Q[(r,c,a)][action] = 0

    # self.Q = {}
    for r in range(Rows):
      for c in range(Cols):
        Q[(r,c)] = {}
        for i in signal_availability.keys():
          if i == (r,c):
            for ant in signal_availability[i]:
              Q[(r,c)][ant] = 0

  def antenna_selection(self, state, action, eps):
    r, c = state
    if np.random.rand() < eps:
      for i in signal_availability.keys():
        if i == (r,c):
          antenna = random.choice(signal_availability[i])
    else:
      for i in signal_availability.keys():
        if i == (r,c):
          antenna = max(Q[(r,c)],key=Q[(r,c)].get)
    print("State: {} Antenna: {} Action Performed: {}".format(state,antenna,action))
    return antenna

  def action_selection(self, state):
    r, c = state
    action = np.random.randint(len(Actions))
    action = Actions[action]
    return action

  def Q_update(self, state, antenna, next_state, reward):
    #r, c, antenna = state
    # print("Next State:{} Antenna: {}".format(next_state,antenna))
    next_max = max(list(Q[next_state].values()))
    Q[state][antenna] = (1 - lr) * Q[state][antenna] + lr * (reward + gamma* next_max)
    print(Q)


  def Model_update(self,state, antenna,next_state, reward):
    if state not in self.Model.keys():
      self.Model[state] = {}
    self.Model[state][antenna] = (next_state, reward)
    # print(self.Model)


  def n_step_Q_update(self, n):

    for _ in range(n):
      rand_s = np.random.randint(len(self.Model.keys()))
      random_state = list(self.Model)[rand_s]
      (r,c) = random_state
      rand_a = np.random.randint(len(self.Model[random_state].keys()))
      for i in signal_availability.keys():
        if i == (r,c):
          random_antenna = random.choice(signal_availability[i])
      # random_antenna = list(self.Model[random_state])[rand_a]
      #print(random_action)
      next_state_r , reward_r = self.Model[random_state][random_antenna]
      #r_ , c_ = random_state
      next_max = max(list(Q[random_state].values()))
      Q[random_state][random_antenna] = (1 - lr) * Q[random_state][random_antenna] + lr * (reward_r + gamma* next_max)


  def reset(self):
    #Q table initialisation
    Q = {}
    for r in range(Rows):
      for c in range(Cols):
        Q[(r,c)] = {}
        for i in signal_availability.keys():
          if i == (r,c):
            for ant in signal_availability[i]:
              Q[(r,c)][ant] = 0
    self.Model = {}

Episodes = 5000
lr = 0.1
gamma = 0.95
eps = 0.82  # To randomise the connection of antennas
n = 50
env = GridWorld()
agent = Agent()
agent.reset()
max_steps_per_episode = 150
Rewards = []
steps_taken = []
Handovers = []
eps_decaying_start = 0
eps_decaying_end = Episodes // 1.5
eps_decaying = eps / (eps_decaying_end - eps_decaying_start)
eps_decaying = 0

for ep in range(Episodes):
    print("Episode: ", ep)
    if eps_decaying_start < ep < eps_decaying_end:
        eps -= eps_decaying
    counter = 0
    env.reset()
    done = False
    state = env.state
    Reward_ep = 0
    Handover_ep = 0
    while not done and counter < max_steps_per_episode:
        action = agent.action_selection(state)
        antenna = agent.antenna_selection(state, action, eps)
        next_state, reward, handover, done, _ = env.step(action, antenna, eps)
        agent.Q_update(state, antenna, next_state, reward)
        Reward_ep += reward
        Handover_ep += handover
        print("Accumulated Rewards: {} Accumulated Handovers: {}".format(Reward_ep, Handover_ep))
        state = next_state
        counter += 1
        agent.Model_update(state, antenna, next_state, reward)
        # agent.n_step_Q_update(n) There is a problem with DynaQ. So using Q learning only

    Rewards.append(Reward_ep)
    Handovers.append(Handover_ep)
    steps_taken.append(counter)
    print("\n")

# plt.plot(range(Episodes),Rewards)
# plt.show()

plt.plot(range(Episodes), Handovers, label='Q Learning')
plt.legend()
plt.show()
print(Q)