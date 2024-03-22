import torch
from torch import nn
from torch.distributions.normal import Normal
import numpy as np
from torch.utils.tensorboard import SummaryWriter
import tracemalloc
from agent_graphEnv import CustomEnvironment
from storage import Buffer #, Observation
from colorama import Fore

import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

import dgl
import dgl.nn.pytorch as dglnn
from dgl.nn.pytorch.conv import GATConv
from datetime import datetime

#TODO Use the code/real folder for mushroom_rl 
#TODO discount rewards
#TODO marker and multiple features

logpath = '/home/algo/code/llmfine/ba/intelligentAgent/runs/'
#writer = SummaryWriter(logpath)

ct = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
writer = SummaryWriter(logpath + ct)

tracemalloc.start(5)

class Critic(nn.Module):
    def __init__(self, ):
        super(Critic, self).__init__()
        self.layer1 = GATConv(1, 30, 1)       #feature space 7
        self.layer2 = GATConv(30, 30, 1)
        self.layer3 = GATConv(30, 30, 1)

        self.lin1 = nn.Linear(30,30)
        self.lin2 = nn.Linear(30,1)
        #self.sm = nn.Softmax(dim =1)  #TODO not necessary 

    def forward(self, g):

        h = g.ndata['value'].float()
        h = torch.unsqueeze(h, 1)

        h = self.layer1(g, h)
        h = torch.relu(h)        
        h = self.layer2(g, h, get_attention=False)        
        h = torch.relu(h)        
        h = self.layer3(g, h, get_attention=False)   
        #h = h.squeeze()   #BUG possible error, to avoid error on line g.ndata['h'] = h
        
        with g.local_scope():
            g.ndata['h'] = h            
            hg = 0
            for ntype in g.ntypes:
                hg = hg + dgl.mean_nodes(g, 'h', ntype=ntype)
                        
            res = torch.tanh(self.lin1(hg))
            res = self.lin2(res)
            #res = self.sm(self.lin2(res))

            return res #, torch.squeeze(att)

class Actor(nn.Module):
    def __init__(self, ):
        super(Actor, self).__init__()
        self.layer1 = GATConv(1, 30, 1)       #feature space 7
        self.layer2 = GATConv(30, 30, 1)
        self.layer3 = GATConv(30, 30, 1)
        
        self.lin1 = nn.Linear(30,30)
        self.lin2 = nn.Linear(30,1) #mu

        self.lin3 = nn.Linear(30,1) #sigma

        self.n = Normal(torch.tensor([0.]), torch.tensor([0.5]))

    def forward(self, g):

        #obtain h from g 
        h = g.ndata['value'].float()  #TODO value is not part of data in DGL
        h = torch.unsqueeze(h, 1)

        h = self.layer1(g, h)
        h = torch.relu(h)        

        h = self.layer2(g, h)
        h = torch.relu(h)       

        h, att = self.layer3(g, h, get_attention=True)        
        #h = h.squeeze() 
        
        with g.local_scope():
            g.ndata['h'] = h            #BUG errror here
            hg = 0
            for ntype in g.ntypes:
                hg = hg + dgl.mean_nodes(g, 'h', ntype=ntype)
                        
            res = torch.relu(self.lin1(hg))   #x1
            #res = self.sm(self.lin2(res))       #TODO should be without SM????
            #x1 = torch.tanh(self.lin2(res))
            x1 = self.lin2(res)

            res2 = torch.relu(self.lin1(hg))  #x2
            #res2 = self.sm(self.lin3(res2))
            sp = nn.Softplus()
            x2 = sp(self.lin3(res2))

        self.n = Normal(x1,x2)
        sample = self.n.rsample()

        #sample = torch.clip(sample, 0, 1)

        return sample

    def getProb(self, g, a):

        #experiment
        # x = torch.tanh(self.fc1(s))
        # x = torch.tanh(self.fc2(x))
        # x1 = torch.tanh(self.fc3(x))
        # sp = nn.Softplus()
        # x2 = sp(self.fc4(x))

        h = g.ndata['value'].float()
        h = torch.unsqueeze(h, 1)

        h = self.layer1(g, h)
        h = torch.relu(h)        

        h, att = self.layer2(g, h, get_attention=True)        
        h = h.squeeze() 
        
        with g.local_scope():
            g.ndata['h'] = h            
            hg = 0
            for ntype in g.ntypes:
                hg = hg + dgl.mean_nodes(g, 'h', ntype=ntype)
                        
            res = torch.relu(self.lin1(hg))   #x1
            #res = self.sm(self.lin2(res))       #TODO should be without SM????
            x1 = torch.tanh(self.lin2(res))

            res2 = torch.relu(self.lin1(hg))  #x2
            #res2 = self.sm(self.lin3(res2))
            sp = nn.Softplus()
            x2 = sp(self.lin3(res2))

        n = Normal(x1,x2)

        prob = torch.exp(n.log_prob(a))

        return prob

critic1 = Critic()
actor = Actor()
actor_old = Actor()

optimizer = torch.optim.Adam(critic1.parameters(), lr=0.0001)  #critic optimizer
#optimizer2 = torch.optim.Adam(critic2.parameters(), lr=0.001)
#optimizer3 = torch.optim.Adam(actor.parameters(), lr=0.00001)
optimizer3 = torch.optim.Adam(actor.parameters(), lr=0.0001)   #actors optimizer

loss_func = torch.nn.MSELoss()

env = CustomEnvironment()
buffer = Buffer()

#BUG: Action should be positive !!

for ep in range(100000) :
    time1 = tracemalloc.take_snapshot()

    s = env.reset()

    print(f'{Fore.GREEN} ep : {ep} {Fore.RESET}')

    for frame in range(40) :

        #st = torch.from_numpy(s.reshape(1,8))
        st = s
        a = np.squeeze(actor(st).detach().numpy())

        next_s, r, done, info = env.step(a)

        v1 = critic1(st)

        #overwrite with value of current node !!
        #v1 = torch.tensor(env.G.nodes[env.node]['value'])
        
        #for single critic networks this is a scalar
        advantage = np.array([r-v1.detach().numpy()], dtype=np.float32) #, r2-v2], dtype=np.float32)  #changed to v2 for r2 was a mistake before
        #advantage = np.array([r-v1], dtype=np.float32) #, r2-v2], dtype=np.float32)  #changed to v2 for r2 was a mistake before
        
        
        #advantage = np.repeat(advantage,2)  #change dimensions for advantages

        buffer.append(s, r, a, advantage)

        s = next_s

        if done :
            break

    if buffer.count > 120 :

        buffer.discount_rewards(gamma=0.9)

        #moved here for slim logs

        writer.add_scalar('1_stats/ep_length', env.t,ep)
        writer.add_scalar('1_stats/rewards', env.ep_rew, ep)
        writer.add_scalar('1_stats/level', env.level, ep)
        writer.add_scalar('2_graph/nodes', s.number_of_nodes(), ep)
        writer.add_scalar('2_graph/edges', s.number_of_edges(), ep)
        writer.add_scalar('2_graph/5sim', env.five_sim, ep)

        #writer.add_scalar('rewards/r2', env.ep_rew2, ep)

        #Critic 1 Training
        rews = torch.FloatTensor(buffer.obs.rewards) #test
        #rews2 = torch.FloatTensor(buffer.obs.rewards2)
        #rews = rews + rews2
        #rews = rews.unsqueeze(1)
        #vals = critic1(torch.FloatTensor(buffer.obs.states))
        #vals = critic1(buffer.obs.states)    #BUG change from scalars to graphs        

        stateGraphs = dgl.batch(buffer.obs.states)
        vals = critic1(stateGraphs)
        vals = torch.squeeze(vals)

        writer.add_histogram('value_estimations', vals, ep)

        c1Loss = loss_func(rews, vals)

        writer.add_scalar('0_loss/critic',c1Loss,ep)

        optimizer.zero_grad()
        c1Loss.backward()
        #[optimizer.step() for i in range(5)]
        optimizer.step() 

        #Actor Training
        #acts = torch.FloatTensor(buffer.obs.actions)
        ## Assuming buffer.obs.actions is a list of NumPy arrays
        acts = torch.tensor(np.stack(buffer.obs.actions), dtype=torch.float32) #changed
        writer.add_histogram('actions', acts, ep)

        #stats = torch.FloatTensor(buffer.obs.states)

        #stats = buffer.obs.states

        stateGraphs = dgl.batch(buffer.obs.states)
        #vals = critic1(stateGraphs)
        stats = stateGraphs

        ratio = actor.getProb(stats, acts)/(actor_old.getProb(stats, acts) + 1e-5)
        adv = torch.tensor(buffer.obs.advantages)
        surr = ratio*adv

        lossActor = -torch.mean(torch.min(surr, torch.clamp(ratio, 0.8,1.2)*adv))
        writer.add_scalar('0_loss/actor',lossActor,ep)

        optimizer3.zero_grad()
        lossActor.backward()
        #[optimizer3.step() for i in range(5)]
        optimizer3.step()

        #copy weights
        actor_old.load_state_dict(actor.state_dict())

        buffer.reset()

    if ep % 100 == 0 and ep > 0: 

        #BUG This causes a memory leak ..

        fig = plt.figure()                
        pos = graphviz_layout(env.G, prog="dot", root='0')
        
        #labels = nx.get_node_attributes(env.G, 'visited')
        labels = nx.get_node_attributes(env.G, 'value')
        
        # Get node values and colors for the colormap
        node_values = nx.get_node_attributes(env.G, 'value')
        node_colors = list(node_values.values())

        # Apply colormap to node values and convert to rgba
        cmap = plt.get_cmap('coolwarm')
        rgba_colors = [cmap(value) for value in node_colors]
        
        nx.draw(env.G, pos, labels = labels, with_labels=True, arrows = True, node_size=700, font_size=10, font_color='black', linewidths=1, alpha=0.7, edge_color="#56a6f5", connectionstyle="arc3,rad=0.1", style=':', width=2, node_color=rgba_colors)

        #nx.draw(env.G, pos, labels = labels, with_labels=True, arrows = True, node_size=700, font_size=10, font_color='black', linewidths=1, alpha=0.7, edge_color="#56a6f5", connectionstyle="arc3,rad=0.1", style=':', width=2)
        #nx.draw(env.G, pos, with_labels=True, arrows = True, node_size=700, font_size=10, font_color='black', linewidths=1, alpha=0.7, edge_color="#56a6f5", connectionstyle="arc3,rad=0.1", style=':', width=2)

        writer.add_figure("graph", fig, ep, close=True)
        plt.close()


        # #increase in similarity over the first 5 elements

        # fig = plt.figure()                

        # # Trim sublists to the first 5 elements
        # cyclic_buffer_trimmed = [sublist[:5] for sublist in env.cyclic_buffer if len(sublist) >= 5]

        # # Convert to numpy array for easier manipulation
        # cyclic_buffer_array = np.array([np.array(sublist) for sublist in cyclic_buffer_trimmed])
  
        # # Calculate the average values along axis 0 (time)
        # average_values = np.mean(cyclic_buffer_array, axis=0)

        # # Calculate the standard deviation along axis 0 (time)
        # std_deviation = np.std(cyclic_buffer_array, axis=0)

        # # Plotting
        # plt.plot(average_values, label='Average Value')
        # plt.fill_between(range(len(average_values)), average_values - std_deviation, average_values + std_deviation, color='blue', alpha=0.2, label='Standard Deviation')
        # plt.xlabel('Time')
        # plt.ylabel('Value')
        # plt.title('Average Values with Standard Deviation')
        # plt.grid()
        # plt.ylim(0, 1)
        # plt.legend()
        
        # writer.add_figure("sim_dev", fig, ep, close=True)
        # plt.close()


    time2 = tracemalloc.take_snapshot()
    mem = tracemalloc.get_traced_memory()[0]
    writer.add_scalar('3_memory/malloc', mem, ep)
