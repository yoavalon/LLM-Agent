import numpy as np 

"""
Placeholder of manual policy 
"""

class Policy():
    """
    Policy for best program choice
    """

    def __init__(self) : 
        """
        Initialize evaluation
        """
        pass

    def decide(self, features, last_features, agent_on = False) : 
        """
        Inputs: 
            features is the full set of scores for the 5 first candidates
            last_features is only the feature of the last decision program
            agent_on: Is the agent called, or simply the first option used?
        """

        if agent_on: 
            
            '''
            valid   MUST
            passed  MUST
            sim_source not relevant
            sim_last Important
            sim_target less important
            mod_last often invalid
            mod_target often invalid
            '''

            last_sim = last_features[4]

            #weights = np.array([5, 5, 0, 2, 5, 0, 0])
            #weights = np.array([5, 0, 0, 0, 0, 0, 0]) #manual policy one: only interested in varlidity
            #weights = np.array([5, 5, 0, 0, 0, 0, 0]) #manual policy two: validity and semantics
            #weights = np.array([0, 0, 0, 5, 0, 0, 0]) #manual policy three: similarity to last 
            weights = np.array([1, 1, 1, 1, 1, 1, 1]) #manual policy three: balanced policy, optimizing all features
        
            # Calculating weighted scores for each vector
            weighted_scores = np.dot(features, weights) 

            # Selecting the vector with the highest score
            best_vector_index = np.argmax(weighted_scores)
            best_vector = features[best_vector_index]
            best_vector_index, best_vector, weighted_scores

            return best_vector_index #np.random.randint(4)
        else : 
            return 0

if __name__ == '__main__':
    
    pol = Policy()

    #reference score required

    #For the policy it might also be useful to obtain the similarity distance to the 
    #original program

    """
    valid, passed_unit_tests, sim_last, sim_target, mod_last, mod_target

    [1, 1.0, 0.799, 0.533, -1, 1.0]
    [1, 1.0, 0.831, 0.781, -1, 1.0]
    [1, 1.0, 1.0, 0.729, -1, -1]
    [1, 1.0, 0.621, 0.599, -1, 0.933]
    [1, 1.0, 0.831, 0.781, -1, 1.0]

    """
    
    pol.decide(feats)


    """
    Criteria: 

    Mod is more 
    
    
    """