import random
import numpy as np
import copy
import matplotlib.pyplot as plt

def IsDuplicate(point,point_list):

    symbol = True
    for p in point_list:
        if point[0] == p[0] and point[1] == p[1]:
            symbol = False
            break

    return  symbol

def iniLoc(length,forbidden_):

    while True:

        x = random.randint(0, length[0] - 1)
        y = random.randint(0, length[1] - 1)

        if IsDuplicate([x,y],forbidden_) == False:
            x = random.randint(0, length[0] - 1)
            y = random.randint(0, length[1] - 1)
        else:
            break


    loc = [x,y]
    return loc

def iniGridState():

    state_dict = dict()
    pit_loc = [[2, 2], [2, 3], [3, 1], [3, 5], [4, 2], [4, 3], [4, 4]]
    goal_loc = [[3, 2]]
    forbidden_ = pit_loc + goal_loc

    #the grid is a 6*7
    for i in range(7):
        for j in range(6):
            if IsDuplicate([i,j],forbidden_) == True:
                key = (i,j)
                value = [0,0,0,0,-3]
                state_dict[key] = value

    return state_dict

def gridBoundary():
    list_ = []
    for i in range(7):
        list_.append([6,i])
    for j in range(7):
        list_.append([j,7])
    return list_

def isOutBoundary(point):

    flag = False

    if point[0] < 0 or point[0] > 6 or point[1] <0 or point[1] > 5:
        flag = True

    return flag



class Agent:
    def __init__(self):
        self.actions = [0,1,2,3,4]
        self.ACTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0),(0, 0)] #up,down,left,right,giveup

        self.goal_reward = 5
        self.pit_reward = -2
        self.move_reward = -0.1
        self.giveup_reward = -3

        self.trial_number = 100000
        self.epsilon = 1

        self.gamma = 1 # no settings of this

        self.alpha = 0.5 # learning rate alpha
        self.q_table = iniGridState()


        self.pit_loc = [[2,2],[2,3],[3,1],[3,5],[4,2],[4,3],[4,4]]
        self.goal_loc = [[3, 2]]
        self.length = [7,6]
        self.forbidden = self.pit_loc + self.goal_loc
        self.isOver = False
        self.gridBoundry = gridBoundary()


    # Need to judge the state here
    def sarsa_learning(self,state, action, reward, next_state, next_action, type):

        if type == 0:
            state_ = (state[0],state[1])
            next_state_ = (next_state[0],next_state[1])

            current_q = self.q_table[state_][action]
            next_state_q = self.q_table[next_state_][next_action]

            new_q = (current_q + self.alpha *(reward + self.gamma * next_state_q - current_q))
            self.q_table[state_][action] = new_q

        elif type == 2:
            state_ = (state[0], state[1])
            current_q = self.q_table[state_][action]
            new_q = (current_q + self.alpha * (reward - current_q))
            self.q_table[state_][action] = new_q

        else:

            pass



    def Q_learning(self,state,action,reward,next_state,next_action):
        current_q = self.q_table[state][action]
        next_state_q = self.q_table[next_state][next_action]
        new_q = (current_q + self.alpha *(reward + self.epislon * next_state_q - current_q))
        self.q_table[state][action] = new_q

    ## epsilon-greedy and other methods to select the action

    def get_action(self,state):

        # if random.random() < self.epsilon:
        #      action = np.random.choice(self.actions)
        #
        # else:
        state_ = (state[0],state[1])
        state_action = self.q_table[state_]
        #action = self.arg_max(state_action)
        action = state_action.index(max(state_action))

        return action

    def arg_max(self,state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)

    def Move(self,state,action):
        alter_act_prob = [0.7,0.1,0.1,0.1]
        result_ = np.random.choice(len(alter_act_prob),1,p = alter_act_prob)[0]

        #print("move result",result_,"action",action)

        state_ = copy.deepcopy(state)

        next_state = copy.deepcopy(state)
        reward = self.move_reward

        type = 0
        if action == 0: #up
            if result_ == 0: # keep old direction
                next_state[1] = next_state[1] - 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 0
            elif result_ == 1: # moves to the right
                next_state[0] = next_state[0] + 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 6
            elif result_ == 2: # moves to the left
                next_state[0] = next_state[0] - 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 0
            else: # move forward 2
                next_state[1] = next_state[1] - 2
                if isOutBoundary(next_state) == True:
                    next_state[1] = 0
        elif action == 1: #down
            if result_ == 0: # keep old direction
                next_state[1] = next_state[1] + 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 5
            elif result_ == 1: # moves to the left
                next_state[0] = next_state[0] - 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 0
            elif result_ == 2: # moves to the right
                next_state[0] = next_state[0] + 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 6
            else: # move forward 2, down 2
                next_state[1] = next_state[1] + 2
                if isOutBoundary(next_state) == True:
                    next_state[1] = 5
        elif action == 2: # Move to right
            if result_ == 0: # keep old direction
                next_state[0] = next_state[0] + 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 6
            elif result_ == 1: # down
                next_state[1] = next_state[1] + 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 5
            elif result_ == 2: # up
                next_state[1] = next_state[1] - 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 0
            else: # move forward 2, right 2
                next_state[0] = next_state[0] + 2
                if isOutBoundary(next_state) == True:
                    next_state[0] = 6
        elif action == 3: # Move to left
            if result_ == 0:  # keep old direction
                next_state[0] = next_state[0] - 1
                if isOutBoundary(next_state) == True:
                    next_state[0] = 0
            elif result_ == 1:  # up
                next_state[1] = next_state[1] - 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 0
            elif result_ == 2:  # down
                next_state[1] = next_state[1] + 1
                if isOutBoundary(next_state) == True:
                    next_state[1] = 5
            else:  # move forward 2, left 2
                next_state[0] = next_state[0] - 2
                if isOutBoundary(next_state) == True:
                    next_state[0] = 0
        else: #give up

            self.isOver = True
            next_state = copy.deepcopy(state_)
            reward = reward + self.giveup_reward
            type = 1

        if next_state[0] == self.goal_loc[0][0] and next_state[1] == self.goal_loc[0][1]:
            reward = reward + self.goal_reward
            next_state = copy.deepcopy(state_)
            self.isOver = True
            type = 2

        if IsDuplicate(next_state,self.pit_loc) == False:
            reward = reward + self.pit_reward
            next_state = copy.deepcopy(state_)
            self.isOver = True
            type = 2

        return next_state, reward, type


# goal_reward = 5
# pit_reward = -2
# move_reward = -0.1
# giveup_reward = -3
# trial_number = 10000
# epsilon = 0.1
# alpha = 0.5

actions = ["up","down","left","right","gu"]
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1),(0, 0)]
pit_loc = [[2,2],[2,3],[3,1],[3,5],[4,2],[4,3],[4,4]]
goal_loc = [[3,2]]

# length = [6,7] # It's 6*7 grid world
#
# forbidden_ = pit_loc + goal_loc

### Initialize the function
# loc_r = iniLoc(length,forbidden_)
# print(loc_r)


###
agent = Agent()

# print(agent.q_table.keys())
# print(agent.pit_loc)

result = []
for i in range(10000):

    #print("iteration ", i)
    agent.isOver = False
    state = iniLoc(agent.length,agent.forbidden)
    action = agent.get_action(state)

    reward_ = 0
    step = 0
    while True:

        next_state, reward, type = agent.Move(state,action)
        next_action = agent.get_action(next_state)
        agent.sarsa_learning(state,action,reward,next_state,next_action,type)
        state = copy.deepcopy(next_state)
        action = next_action

        reward_ = reward_ + reward
        step = step + 1

        if agent.isOver == True:
            result.append([step,reward_])
            #print("reward",reward_)
            break

print(agent.q_table.values())
r_ = []
for i in range(len(result)):
    r_.append(result[i][1])

r2 = np.zeros(200)

for i in range(200):
    temp = np.array(r_[i * 50 : i*50 + 50])
    r2[i] = np.median(temp)


plt.figure()
plt.plot(r2)
plt.show()