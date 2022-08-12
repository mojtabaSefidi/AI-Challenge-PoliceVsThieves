from src.client import GameClient
from src.model import GameView
import random
import sys



def get_thief_starting_node(view: GameView) -> int:
    # write your code here
    good_position = [143,7,144,120,155,159,113,131,123,141,158]
    return random.choice(good_position)


class G():
    def __init__(self, nodes, init_directed_graph):
        self.nodes = nodes
        self.directed_graph = self.construct_directed_graph(nodes, init_directed_graph)
        
    def construct_directed_graph(self, nodes, init_directed_graph):
        '''
        This method makes sure that the directed_graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        directed_graph = {}
        for node in nodes:
            directed_graph[node] = {}
        
        directed_graph.update(init_directed_graph)
        
        for node, edges in directed_graph.items():
            for adjacent_node, value in edges.items():
                if directed_graph[adjacent_node].get(node, False) == False:
                    directed_graph[adjacent_node][node] = value
                    
        return directed_graph
    
    def get_nodes(self):
        "Returns the nodes of the directed_graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.directed_graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.directed_graph[node1][node2]

def path2list(all_paths, all_nodes):
  init_directed_graph = {}
  for node in all_nodes:
    init_directed_graph[node.id] = {}
  for path in all_paths:
    init_directed_graph[path.first_node_id][path.second_node_id] = 1
    return init_directed_graph

def next_choice(previous_nodes, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    return (path[-2],len(path))


def dijkstra_algorithm(directed_graph, start_node):
    unvisited_nodes = list(directed_graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the directed_graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = directed_graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + directed_graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes

class Phone:
    def __init__(self, client: GameClient):
        self.client = client

    def send_message(self, message):
        self.client.send_message(message)

    
class AI:
    def __init__(self, phone: Phone):
        self.phone = phone

    def thief_move_ai(self, view: GameView) -> int:
        # write your code here
        thief_current_node_id = view.viewer.node_id
        thief_current_money = view.balance
        all_paths = view.config.graph.paths
        all_nodes = view.config.graph.nodes
        thief_curent_turn = view.turn.turn_number
        thief_visible_turns = view.config.visible_turns
        income_per_turn = view.config.thief_income_each_turn
        visible_agents = view.visible_agents
        is_visible = thief_curent_turn in thief_visible_turns
        
        thief_team = view.viewer.team
        if thief_team == "FIRST":
            opponent_team = 'SECOND'
        else:
            opponent_team = 'FIRST'

        thief_posible_paths = [thief_path for thief_path in all_paths if (thief_path.first_node_id == thief_current_node_id or thief_path.second_node_id == thief_current_node_id) and thief_path.price <= thief_current_money]
        thief_posible_paths.sort(key=lambda thief_path: thief_path.price, reverse=True)
        if not thief_posible_paths: 
            return thief_current_node_id
        else:
            output = random.choice(thief_posible_paths)
            if output.first_node_id == thief_current_node_id:
                return output.second_node_id
            else:
                return output.first_node_id
       
        # visibles =  [agent for agent in visible_agents if agent.agent_type == 'POLICE' and agent.team == opponent_team]
        
        # message = ''
        # for m in range(len(view.visible_agents)):
        #     message = message  + '0'
        # self.phone.send_message(message)


        
        # graph = Graph(all_nodes, path2list(all_paths, all_nodes))
        # previous_nodes = dijkstra_algorithm(graph=graph, start_node=thief_current_node_id)            
        
        # visibles = [(agent.id, agent.node_id) for agent in visible_agents if agent.agent_type == 'POLICE' and agent.team == opponent_team and agent.is_dead == False]
        # visible_paths = {}
        
        # for tup in visibles:
        #     next, length = next_choice(previous_nodes, start_node=thief_current_node_id, target_node=tup[-1])
        #     visible_paths[next] = length

        # if not len(visible_paths):
        #     return thief_current_node_id
        # else:
        #     return random.choice([k for k,v in visible_paths.items() if v == min(visible_paths.values())])





    def police_move_ai(self, view: GameView) -> int:
        # write your code here
        police_current_node_id = view.viewer.node_id
        police_current_money = view.balance
        all_paths = view.config.graph.paths
        all_nodes = view.config.graph.nodes
        police_curent_turn = view.turn.turn_number
        visible_turns = view.config.visible_turns
        income_per_turn = view.config.police_income_each_turn
        visible_agents = view.visible_agents
        is_visible = police_curent_turn in visible_turns
        police_team = view.viewer.team
        police_type = view.viewer.agent_type


        # num_team_police = len([agent.id for agent in visible_agents if agent.agent_type == 'POLICE' and agent.team == police_team])



        print(visible_agents)
        if is_visible:
            g = G(all_nodes, path2list(all_paths, all_nodes))
            previous_nodes = dijkstra_algorithm(directed_graph=g, start_node=police_current_node_id)            
            
            visibles = [agent.node_id for agent in visible_agents if (agent.agent_type != police_type and agent.team != police_team and agent.is_dead == 0)]
            visible_paths = {}
            
            for nodeID in visibles:
                next, length = next_choice(previous_nodes, start_node=police_current_node_id, target_node=nodeID)
                visible_paths[next] = length
            
            
            print(previous_nodes)
            # print(visibles)
            # print(visible_paths)
            
            return random.choice([k for k,v in visible_paths.items() if v == min(visible_paths.values())])

            # if not len(visible_paths):
            #     return police_current_node_id
            # else:
                # return random.choice([k for k,v in visible_paths.items() if v == min(visible_paths.values())])
        else:
            # self.phone.send_message('00101001')
            
            police_posible_paths = [police_path for police_path in all_paths if (police_path.first_node_id == police_current_node_id or police_path.second_node_id == police_current_node_id) and police_path.price <= police_current_money]
            police_posible_paths.sort(key=lambda police_path: police_path.price, reverse=True)        

            if not len(police_posible_paths):
                return police_current_node_id
            else:
                output = random.choice(police_posible_paths)
                if output.first_node_id == police_current_node_id:
                    return output.second_node_id
                else:
                    return output.first_node_id



        

