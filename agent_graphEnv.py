import gym
import numpy as np
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import dgl 
from colorama import Fore

from gym.spaces import Box, Discrete
#Don't allow recap to be executed again

class CustomEnvironment(gym.Env):
    def __init__(self):
        super(CustomEnvironment, self).__init__()

        self.action_space = Box(-1, 1, shape=(2,), dtype=np.float32)
        self.observation_space = Box(0, 1, shape=(16,), dtype=np.float32)
        self.horizon = 200
        self.gamma = 0.99
        self.info = {'horizon' : 200, 'gamma' : 0.99}


        self.cyclic_buffer = [[],[],[],[],[],[],[],[],[],[]]
        self.ep = 0

    def rec(self, level=0, n=5, sigma=0.15):
        """
        Simulation of similarity values
        Taking into account the level
        """
        
        r = np.random.normal(0.5 + level * 0.1, sigma, n)
        r = np.clip(r, 0, 1)

        return r

    def recap(self, node, level):  
        
        #self.G.nodes[node]['visited'] += 1  #TODO for now works somehow, but later..

        r = self.rec(level)   
        for i in range(1, 6): 
            new_node = str(node) + str(i)

            #if self.G.has_node(node) : 
            #    self.G.nodes[node]['revisited'] = 1

            if self.G.has_node(new_node):
                # If it exists, update the value attribute
                #self.G.nodes[new_node]['revisited'] = 1
                pass
            else : 
                self.G.add_node(new_node, value=np.round(r[i-1], 3), valid  = 1, visited = 0)
            
            self.G.add_edge(node, new_node)

            #print(new_node, np.round(r[i-1], 3))
            #print(node, new_node)

    def getLevel(self) : 
        
        if self.node == '0' : 
            return 0
        else : 
            return len(self.node)

    #def reset(self, s):
    def reset(self) :
        # Reset the environment to the initial state

        self.G = nx.Graph()
        startvalue = np.round(np.random.normal(0.4, 0.1,1)[0],3)
        self.G.add_node('0', value=startvalue, valid  = 1, visited = 0)
                
        self.G_dgl = dgl.from_networkx(self.G, node_attrs=['valid', 'value', 'visited'])
        self.G_dgl = dgl.add_self_loop(self.G_dgl)  #TODO Check if this is ok was a fix

        #node_attributes = {node: self.G.nodes[node] for node in self.G.nodes}
        #self.G_dgl.ndata.update(node_attributes)
        
        self.level = 0

        self.node = '0' #start from root node

        self.recap(self.node, self.level)
        self.ep_rew = 0
        self.t = 0
        self.ep_vals = []
        self.ep += 1

        self.five_sim = 0.4
        #TODO reset has to add the first 5 options already, otherwise how to decide

        return self.G_dgl

    def step(self, action):

        done = False

        #step penalty
        reward = -0.01

        action = np.clip(action, 0,1 ) #BUG resolve issue when returning negative numbers
 
        #0 is back, 1 to 5 candidate nodes
        act = int(np.round(action*5))

        current_node_value = self.G.nodes[self.node]['value']
        self.ep_vals.append(current_node_value)

        if self.t == 5 : 
            self.five_sim = current_node_value

        self.node = self.node + str(act)
        if self.G.has_node(self.node): 
            if self.G.nodes[self.node]['value'] == 1 : 
                done = True         #TODO when done, no need for further branch generation
                reward += 10
                #print(f'{Fore.RED} DONE {Fore.RESET}')

        #penalty for moving back when in root
        if act == 0 :
            #print(f'{Fore.MAGENTA}back event{Fore.RESET}')
            if self.node[:-1] == '0': 
                reward -= 1
                self.node = '0' #bug fix
            else : 
                #return to previous node
                self.node = self.node[:-2]
                #self.recap(self.node, self.getLevel())  #added
                self.G.nodes[self.node]['visited'] += 1

                #discovery reward
                #reward += 0.015  #moving backwards is slightly more rewarded (later remove)
        else : 
            if not done : 
                self.recap(self.node, self.getLevel())
            #self.node = self.node + str(act)
            
            #discovery reward
            #reward += 0.01

            #TODO check this

            #TODO add parameter to check if visited

        if self.getLevel() == 10 : 
            done = True
        
        #self.G_dgl = dgl.from_networkx(self.G)

        #print(f'{Fore.GREEN} action : {act} {Fore.RESET}')
        #print(f'{Fore.GREEN} action : {act} {Fore.RESET}{Fore.YELLOW} reward : {reward:0.2f} {Fore.RESET}{Fore.WHITE} node : {self.node}{Fore.RESET}{Fore.BLUE} graph : {self.G} {Fore.RESET}')
        #print(f'{Fore.BLUE} graph : {self.G} {Fore.RESET}')

        self.ep_rew += reward
        self.t += 1

        if done : 
            self.level = self.getLevel()
            self.ep_rew = self.ep_rew / self.t
            #cyc_counter = self.ep % 10 
            #self.cyclic_buffer[cyc_counter] = self.ep_vals

        self.G_dgl = dgl.from_networkx(self.G, node_attrs=['valid', 'value', 'visited'])
        self.G_dgl = dgl.add_self_loop(self.G_dgl)  #TODO Check if this is ok was a fix

        return self.G_dgl, reward, done, {}


def main():

    # Example usage:
    env = CustomEnvironment()

    # Main loop for interacting with the environment
    for episode in range(10):
        state = env.reset()
        done = False

        while not done:
            action = np.random.rand()  # Choose an action based on your RL algorithm
            next_state, reward, done, info = env.step(action)

        # #unit test actions
        # actions = [0,0,2,4,0,1,2]
        # for i in range(6) : 
        #     action = actions[i]/5
        #     print(f'{Fore.CYAN}Starting action {int(np.round(action*5))}-------------------- {Fore.RESET}')
        #     next_state, reward, done, info = env.step(action)


        #render
        from networkx.drawing.nx_pydot import graphviz_layout
        import matplotlib.pyplot as plt
        pos = graphviz_layout(env.G, prog="dot", root='0')
        
        #labels = nx.get_node_attributes(env.G, 'visited')
        labels = nx.get_node_attributes(env.G, 'value')
        nx.draw(env.G, pos, labels = labels, with_labels=True, arrows = True, node_size=700, font_size=10, font_color='black', linewidths=1, alpha=0.7, edge_color="#56a6f5", connectionstyle="arc3,rad=0.1", style=':', width=2)
        #nx.draw(env.G, pos, with_labels=True, arrows = True, node_size=700, font_size=10, font_color='black', linewidths=1, alpha=0.7, edge_color="#56a6f5", connectionstyle="arc3,rad=0.1", style=':', width=2)
        plt.show()

    env.close()  


if __name__ == "__main__":
    main()

