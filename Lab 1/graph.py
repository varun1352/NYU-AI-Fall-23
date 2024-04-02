class TreeNode:
    def __init__(self, label, value=None, children=None):
        self.label = label
        self.value = value
        self.children = children if children else []

    
def parse_graph_file(filename):
    graph = {}

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            # print(line)
            if not line or line.startswith('#'):
                continue
            
            if ':' in line:
                node, children = line.split(':')
                children = children[2:len(children)-1]
                children = children.replace(', ',' ')
                children = children.split(' ')
                # print(node, children)
                graph[node] = TreeNode(node, None, children)
                # print(Node)
                
            
            if '=' in line:
                node, value = line.split('=')
                value = int(value)
                # print(node, value)
                children = []
                graph[node] = TreeNode(node, value, children)
    return graph

def check(graph):
    root_list = []
    is_a_child = []
    for key in graph.keys():
        for child in graph[key].children:
            if child in is_a_child:
                continue
            else:
                is_a_child.append(child)
        
    
    check_list = is_a_child + root_list - graph.keys()
    root_list = graph.keys() - is_a_child
    if len(root_list) !=  1:
        print(root_list, "Multiple roots")
        exit()    
    root_list = list(root_list)
    check_list = is_a_child + root_list - graph.keys()
    
    if len(check_list) != 0 :
        print('# Error case, missing leafs, possible output')
        print('child node "', check_list, '" not found')
        exit()
    return root_list[0]
    
def get_adjacency(graph):
    check_dict = {}
    adj_list = []
    for key in graph.keys():
        check_dict[key] = graph[key].children

    check_dict = {node: set(children) for node, children in check_dict.items()}
    for key in check_dict.keys():
        for child in check_dict[key]:
            list = [key, child]
            adj_list.append(list)
    return adj_list

def cyclic_check_util(graph_neighbor, vertex, visited, recStack):
    visited[vertex] = True
    recStack[vertex] = True
    for neighbor in graph_neighbor[vertex]:
        if not visited[neighbor]:
            if cyclic_check_util(graph_neighbor, neighbor, visited, recStack):
                return True
            
        elif recStack[neighbor]:
            return True
        
    recStack[vertex] = False
    return False
   
def cyclic_check(graph_neighbor):
    length = len(graph_neighbor)
    visited = {v: False for v in graph_neighbor.keys()}
    recStack = {v : False for v in graph_neighbor.keys()}               
    for key in graph_neighbor.keys():
        if not visited[key]:
            if cyclic_check_util(graph_neighbor, key, visited, recStack):
                return True
    return False

def minimax(graph, node, is_maximizing, verbose_mode):
    if not graph[node].children:
        return graph[node].value

    if is_maximizing:
        max_child = None
        max_value = float('-inf')
        for child in graph[node].children:
            child_value = minimax(graph, child, False, verbose_mode)
            if child_value > max_value:
                max_value = child_value
                max_child = child
        if verbose_mode:
            print('max(',node,') chooses', max_child, 'for', max_value)
        if not verbose_mode:
            if node ==  graph_root:
                print('max',node,'chooses', max_child, 'for', max_value)
        return max_value
    else:
        min_value = float('inf')
        min_child = None
        for child in graph[node].children:
            child_value = minimax(graph, child, True, verbose_mode)
            if child_value < min_value:
                min_value = child_value
                min_child = child
        if verbose_mode:
            print('min',node,'chooses', min_child, 'for', min_value)
        if not verbose_mode:
            if node == graph_root:
                print('min',node,'chooses', min_child, 'for', min_value)
        return min_value

def check_range(graph, range):
    for key in graph.keys():
        if graph[key].value:
            if graph[key].value > range or graph[key].value < range*(-1):
                print('Error, Values out of bounds')
                exit()

def minimax_with_alpha_beta(graph, node, alpha, beta, maximizing_player, use_alpha_beta, verbose_mode):
    if not graph[node].children:
        return graph[node].value
  
    if maximizing_player:
        max_child = None
        pruned = False
        max_value = float('-inf')
        for child in graph[node].children:
            child_value = minimax_with_alpha_beta(graph, child, alpha, beta, False, use_alpha_beta, verbose_mode)
            if child_value > max_value:
                max_value = child_value
                max_child = child
            max_value = max(max_value, child_value)
            alpha = max(alpha, max_value)
            if use_alpha_beta and beta <= alpha:
                pruned = True
                break  # Beta pruning
        if not pruned: 
            if verbose_mode:
                print('max',node,'chooses', max_child, 'for', max_value)
            if not verbose_mode:
                if node ==  graph_root:
                    print('max',node,'chooses', max_child, 'for', max_value)
            # print('max',*node,'chooses', max_child, 'for max value', max_value)            
        return max_value
    else:
        min_child = None
        pruned = False
        min_value = float('inf')
        for child in graph[node].children:
            child_value = minimax_with_alpha_beta(graph, child, alpha, beta, True, use_alpha_beta, verbose_mode)
            # min_value = min(min_value, child_value)
            if child_value < min_value:
                min_value = child_value
                min_child = child
            beta = min(beta, min_value)
            if use_alpha_beta and beta <= alpha:
                pruned = True
                break  # Alpha pruning
        if not pruned:
            if verbose_mode:
                print('min',node,'chooses', min_child, 'for', min_value)
            if not verbose_mode:
                if node == graph_root:
                    print('min',node,'chooses', min_child, 'for', min_value)
        
            # print('min',*node,'chooses', min_child, 'for min value', min_value)
        return min_value

if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description="Graph extractor from a text file.")
    # parser.add_argument("filename", help="Path to the input text file")
    # args = parser.parse_args()
    # import argparse
    Verbose = False
    mode = False
    Range = 0


    parser = argparse.ArgumentParser(description="Minimax game tree solver with alpha-beta pruning.")
    parser.add_argument('-v', action='store_true', help="Verbose mode")
    parser.add_argument('-ab', action='store_true', help="Use alpha-beta pruning")
    parser.add_argument('-range', type=int, help="Value range")
    parser.add_argument('mode', choices=['min', 'max'], help="Specify 'min' for minimizer or 'max' for maximizer")
    parser.add_argument('graph_file', help="Path to the graph file")

    args = parser.parse_args()
    verbose_mode = args.v
    alpha_beta_pruning = args.ab
    value_range = args.range
    mode = args.mode
    graph_file = args.graph_file
    if value_range == None:
        value_range = float('inf')

    graph = parse_graph_file(args.graph_file)
    label_neighbor = {}
    for key in graph.keys():
        label_neighbor[key] = graph[key].children
    graph_root = check(graph)
    # We checked here for the case of multiple roots
    adj_list = get_adjacency(graph)
    
    # Now that we have the root and adjacency list of the graph, we can go ahead and check for 
    # validity of the graph. In this we have to check for 
    # Missing Nodes
    # Missing Leaf/leaves
    # Cyclic graph
    boolean = cyclic_check(label_neighbor)
    
    check_range(graph, value_range)
    if boolean:
        print('The given graph is cyclic')
        exit()
    if value_range == float('inf'):
        if verbose_mode:
            if alpha_beta_pruning:
                print('#', mode, '-ab -v')
            if not alpha_beta_pruning:
                print('#', mode, '-v')
        if not verbose_mode:
            print('#', mode)
    else:
        if verbose_mode:
            if alpha_beta_pruning:
                print('#', mode, '-ab -v range', value_range)
            if not alpha_beta_pruning:
                print('#', mode, '-v range', value_range)
        if not verbose_mode:
            print('# range', value_range, mode)
    
    if alpha_beta_pruning:
        if mode == 'max':
            value = minimax_with_alpha_beta(graph, graph_root, float('-inf'), float('inf'), True, alpha_beta_pruning, verbose_mode)
            
        elif mode == 'min':
            value = minimax_with_alpha_beta(graph, graph_root, float('-inf'), float('inf'), False, alpha_beta_pruning, verbose_mode)
            

    elif alpha_beta_pruning == False:
        if mode == 'max':
            minimax_value = minimax(graph, graph_root, True, verbose_mode)
            
        elif mode == 'min':
            minimax_value = minimax(graph, graph_root, False, verbose_mode)
