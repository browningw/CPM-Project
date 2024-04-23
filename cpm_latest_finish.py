"""
Critical Path Latest Finish Calculator

  File: cpm_latest_finish.py
  Description: This program helps find the earliest finish time via the 
              Critical Path method of business tasks.

  Student Name: Warren Browning
  Student UT EID: wjb2243

  Partner Name: Aaron Gangoso
  Partner UT EID: ajg5397

  Course Name: CS 313E
  Unique Number: 50775
  Date Created: 04/14/2024
  Date Last Modified: 04/22/2024

"""
import sys

class Graph():
    """Graph class"""
    def __init__(self):
        """constructor"""
        #list of node objects
        self.nodes = []
        #list of start node objects
        self.start = []
    def add_node(self, new_node):
        self.nodes.append(new_node)
    def set_start(self):
        #check if graph is empty
        if len(self.nodes) != 0:
            for i in self.nodes:
                if len(i.predecessors) == 0:
                    #append the nodes
                    self.start.append(i)
        else:
            print('Error: graph is empty.')
    def copy_graph(self):
        graph_copy = self.__init__()
        for i in self.nodes:
            graph_copy.nodes.append(i)
        
    

class Task_Node():
    """Location/Task node class"""
    def __init__(self, label, duration):
        """constructor"""
        self.label = label
        self.duration = duration
        #LIST OF LABELS
        self.predecessor_labels = []
        self.predecessors = []
        
        self.next_nodes = []
        
        self.start_time = 0
        
        self.end_time=float('-inf')
        
# =============================================================================
#         #critical_next is the node that is next in the critical path, if self
#         #is in the critical path
#         self.critical_next = None
# =============================================================================
        
    
    #add predecessors for a node
    def add_predecessors(self, graph):
        if len(self.predecessor_labels) > 0:
            for c in graph.nodes:
                if self == c:
                    continue
                for j in self.predecessor_labels:
                    if c.label == j:
                        self.predecessors.append(c)
    
    def print_predecessors(self):
        print(f'\n{self.label}: ', end=' ')
        for pred in self.predecessors:
            print(pred.label, end=' ')

    def print_next_nodes(self):
        print(f'\n{self.label}: ', end= ' ')
        for suc in self.next_nodes:
            print(suc.label, end=' ')
    

    
def set_next_nodes(current_node, graph):
    """set the next_node values for each node"""
    #search through node labels in predecessors
    for pred in current_node.predecessors:
        #search through all nodes in graph
        for node in graph.nodes:
            #if node in graph is the same as predecessor of current node, add
            #current node to the list of next_nodes for the predecessor
            if node.label == pred.label:
                pred.next_nodes.append(current_node)


def check_for_predecessors(node_info):
    """checks if a node has predecessors"""
    if len(node_info)>2:
#        print(node_info)
        return True
    else:
#        print(node_info)
        return False
    

            
def modify_paths(current_node, max_end_duration):
    """changes the start and end time attributes for each node and also helps
    identify the earliest finish time"""
    #if reached an end node, add corresponding end time to possible_end_time list
    if len(current_node.next_nodes) == 0:
        max_end_duration.append(current_node.end_time)

    #iterate through nodes, modifying the start and end times accordingly
    for suc in current_node.next_nodes:
#        print(suc.label, suc.start_time, current_node.end_time)
        suc.start_time = max(suc.start_time, current_node.end_time)
        suc.end_time = max(suc.end_time, suc.duration + suc.start_time)
        #print(suc.label, suc.duration + suc.start_time)
        print(suc.label, suc.start_time, suc.end_time)
#        print('####\n')
        modify_paths(suc, max_end_duration)
#    print('End of path. \n#######\n')
        

def search_for_critical_path(graph):
    """search through graph to find critical path"""
    #loop through starting node objects
    possible_critical_paths = []
    possible_end_times = []
    for i in graph.start:
        print('\n########')
        print(f'\nPath(s) starting at node {i.label}:')
    #check if starting node has a longer duration than the current
    #starting max duration, and if node i's next_nodes 
        i.end_time = i.duration
        #modify start and end times, also find all possible end times
        modify_paths(i, possible_end_times)
        #find maximum duration of path(s) starting from node i
        last_node_duration = max(possible_end_times)
        #add this maximum duration to the list of maximum durations respective
        #to each starting node
        possible_critical_paths.append(last_node_duration)
    
    critical_path_duration = max(possible_critical_paths)
    return critical_path_duration

    

def main():
    """main function"""

#number of nodes is the first line
    line = sys.stdin.readline()
    line = line.strip()
    num_nodes = int(line)

    new_graph = Graph()

    for _ in range(num_nodes):
        
        line = sys.stdin.readline()
        node_info = line.strip().split()
        #initialize node.label and node.duration
        new_node = Task_Node(node_info[0], int(node_info[1]))
        
        #check if predecessors exist
        if check_for_predecessors(node_info) is True:
            #loop through predecessors and add them to node.predecessors
            for i in node_info[2:]:
                new_node.predecessor_labels.append(i)
            new_graph.add_node(new_node)
        else:
            new_graph.add_node(new_node)
            #add new_node object to start
            new_graph.start.append(new_node)

    #set values for node.predecessors
    for i in new_graph.nodes:
        i.add_predecessors(new_graph)

    #add values for node.next_nodes (successors)
    for i in new_graph.nodes:
#        print(i.label, i.start_time, i.end_time)
        set_next_nodes(i, new_graph)
#        print('End of path.\n########\n')

    critical_path_duration = search_for_critical_path(new_graph)
    print(f'\nThe critical path duration is: {critical_path_duration} time units.')
    
    
    
    # =============================================================================
    # ####################################################
    #     #testing code
    #     for node in new_graph.nodes:
    #         node.print_predecessor_labels()
    #         
    #     print('####################')
    #     
    #     for node in new_graph.nodes:
    #         node.print_predecessors()
    #         
    #     print('####################\n')
    #         
    #     for node in new_graph.nodes:
    #         node.print_next_nodes()
    # ####################################################
    # =============================================================================

    
main()