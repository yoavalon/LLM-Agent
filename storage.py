import numpy as np

class Observation() :
    def __init__(self) :

        self.states = []
        self.rewards = []
        #self.rewards2 = []
        self.actions = []
        self.advantages = []

class Buffer() :
    def __init__(self):

        self.count = 0
        self.obs = Observation()

    def reset(self) :

        self.count = 0
        self.obs = Observation()
        #maybe invoke garbage collector

    def append(self, s, r1,a, ad) :

        self.count += 1

        self.obs.states.append(s)
        self.obs.rewards.append(r1)
        #self.obs.rewards2.append(r2)
        self.obs.actions.append(a)
        self.obs.advantages.append(ad)

    def discount_rewards(self, gamma=0.99):
        discounted_rewards = np.zeros_like(self.obs.rewards, dtype=np.float32)
        running_add = 0
        for t in reversed(range(len(self.obs.rewards))):
            running_add = running_add * gamma + self.obs.rewards[t]
            discounted_rewards[t] = running_add
        self.obs.rewards = discounted_rewards