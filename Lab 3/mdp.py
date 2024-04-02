import argparse
import random

class MDP:
    def __init__(self, nodes, edges, rewards, probs, discount, tol, maxIter, minimizer):
        self.maxIter = maxIter
        self.nodes = nodes
        self.discount = discount
        self.tol = tol
        self.rewards = rewards if rewards else {node: 0 for node in nodes}
        self.probs = {}
        self.transitions = {}
        self.typeOfNode = {}
        self.optimize = min if minimizer else max        

        #we here check for the type of node where T denotes terminal, D for Decision, C for Chance
        for node in nodes:
            if not node in probs and not node in edges and node in rewards:
                self.typeOfNode[node] = "T"
                continue
            self.rewards[node] = rewards[node] if node in rewards else 0
            actions = edges[node]
            if not node in probs:
                self.typeOfNode[node] = "D"
                success = 1
                self.transitions[node] = dict(
                    (action, [
                        (success, action)]
                        ) for action in actions
                )
                continue
            if len(actions) == 1:
                self.typeOfNode[node] = "C"
                success = 1
                self.probs[node] = [(success, actions[0])]
                continue
            if len(probs[node]) == 1:
                self.typeOfNode[node] = "D"
                success = probs[node][0]
                failure = (1 - success) / (len(actions) - 1)
                self.transitions[node] = dict(
                    (action,
                     [(success if neighbor == action else failure,neighbor)
                      for neighbor in actions]
                      )for action in actions)
            else:
                self.typeOfNode[node] = "C"
                self.probs[node] = [(prob, outcome)for outcome, prob in zip(edges[node], probs[node])]
    
    #implementation of the bellman algorithm which simply returns the rewards in the case the node is a terminal node
    def bellman(self, node, action, values):
        if self.typeOfNode[node] == "T":
            if node in self.rewards:
                return self.rewards[node]
            return 0
        resultVal = 0
        for prob, next_node in self.TransitionFunction(node, action):
            value  = self.rewards[node] if node in self.rewards else 0
            resultVal = (resultVal +  prob * (value + self.discount * values[next_node]))*1 
        return resultVal
    
    # a transition function which provides us with the node and the probability of the next nodes from the current node
    def TransitionFunction(self, node, action = None):
        if self.typeOfNode[node] == "D":
            return self.transitions[node][action]
        if self.typeOfNode[node] == "C":
            return self.probs[node]
        return [(0, node)]

    #the main function where we start with the random policy and generate the new policies, evaluate and check them 
    #and then confirm the correctness of these policies
    def policy_iteration(self):
        #initialization of the new policy and values 
        values = {node: 0 for node in self.nodes}
        policy = {}
        #Random Policy Initialization:
        # A random policy is initialized for each state. 
        # For each state, a random action is chosen from the available actions in the state's transition probabilities.
        for node in self.transitions.keys():
            if node in self.transitions:
                selfList = list(self.transitions[node].keys())
            policy[node] = random.choice(selfList)
        
        #Policy Iteration Loop:
        # The algorithm iterates a maximum number of times (self.maxIter), updating the value function and policy in each iteration.
        # The outer loop checks for stability, and if the policy doesn't change in an iteration, the algorithm terminates and returns the final policy and values.
        for i in range(self.maxIter):
            stability = True
            for i in range(self.maxIter):
                for node in self.nodes:
                    print(node)
                    reward = self.discount * sum(
                        prob * values[next_node]
                        for prob, next_node in self.TransitionFunction(
                            node, policy[node] if node in policy else None
                        )
                    )
                    for prob, next_node in self.TransitionFunction(
                            node, policy[node] if node in policy else None
                        ):
                        print(next_node)
                        print(prob, values[next_node])
                    value  = self.rewards[node] if node in self.rewards else 0
                    values[node] = value + reward
                    print('------')

            #Policy  Improvement:
            # For each decision node in the MDP, it compares the value of the current policy with the value of other possible actions. 
            # If there is a better action, the policy is updated, and stability is set to False.
            for DecisionNode in self.transitions.keys():
                bellman = self.bellman
                DecisionNodeList = list(self.transitions[DecisionNode].keys())
                optimal_action = self.optimize(
                    DecisionNodeList,
                    key = lambda action: bellman(DecisionNode, action, values),
                )
                NewPolicyValues = 1 * bellman(DecisionNode, optimal_action, values)
                OldPolicyValues = 1 * bellman(DecisionNode, policy[DecisionNode], values)
                if NewPolicyValues > OldPolicyValues:
                    policy[DecisionNode] = optimal_action
                    stability = False

            if stability:
                return policy, values


#Parshing the cmdline arguements and the input file
parser = argparse.ArgumentParser()
parser.add_argument('-df', type=float, default=1.0)
parser.add_argument('-min', action='store_true', default=False)
parser.add_argument('-tol', type=float, default=0.01)
parser.add_argument('-iter', type=int, default=100)
parser.add_argument('inputFile')

args = parser.parse_args()
discount =args.df
maxIter=args.iter
minimizer=args.min
tolerance=args.tol
inputFile = args.inputFile
if discount < 0 or discount > 1:
    print('Error: Discount factor out of bounds')
    exit()

#processing the input file 
nodes = set()
edges = {}
values = {}
typeOfNode = {}
probs = {}
with open(args.inputFile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):  
                continue
            if not line:
                continue 
            if '%' in line:
                name, value = line.split('%')
                name = name.strip()
                nodes.add(name)
                typeOfNode[name] = 'D'
                probability = []
                value = value.strip().split(' ')
                probability = [float(val) for val in value]
                probs[name] = probability

            if '=' in line:
                name, value = line.split('=')
                name = name.strip()
                typeOfNode[name] = 'T'
                nodes.add(name)
                value = float(value.strip())
                values[name] = value

            if ':' in line:
                name, value = line.split(':')
                name = name.strip()
                nodes.add(name)
                value = value.strip()[1:-1].split(',')
                value = [val.strip() for val in value]
                edges[name] = value
transition = {}

#creating an mdp object

mdp = MDP(nodes, edges, values, probs, discount = discount, maxIter= maxIter, minimizer= minimizer, tol= tolerance)

policy, values = mdp.policy_iteration()
for key in sorted(policy.keys()):
    value = policy[key]
    print( key + ' -> ' +  value )

for key in sorted(values.keys()):
    value = values[key]
    print('{}={:<10.3f}'.format(key, value))