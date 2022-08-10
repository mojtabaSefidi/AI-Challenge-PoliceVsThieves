from src.client import GameClient
from src.model import GameView
import random
from collections import deque,ChainMap



def get_thief_starting_node(view: GameView) -> int:
    # write your code here
    good_position = [143,7,144,120,155,159,113,131,123,141,158]
    return random.choice(good_position)


def isNotVisited(x, path):
    if (x in path):
        return 0		
    else: 
        return 1

# Utility function for finding paths in graph
# from source to destination

def findpaths(g, src, dst, v):
                
    # Create a queue which stores
    # the paths
    q = deque()
    result = []
    # Path vector to store the current path
    path = []
    path.append(src)
    q.append(path.copy())
    
    while q:
        path = q.popleft()
        last = path[len(path) - 1]

        # If last vertex is the desired destination
        # then print the path
        if (last == dst):
            result.append(path)

        # Traverse to all the nodes connected to
        # current vertex and push new path to queue
        for i in range(len(g[last])):
            if (isNotVisited(g[last][i], path)):
                newpath = path.copy()
                newpath.append(g[last][i])
                q.append(newpath)
    # return [x for x in result if  
    result = [x for x in result if len(x) == len(min(result, key=len))]
    return random.choice(result)[1], len(result[0])

def path2list(all_paths, n):
    path_matrix = [[] for _ in range(n)]
    for path in all_paths:
        path_matrix[path.first_node_id-1].append(path.second_node_id-1)
        path_matrix[path.second_node_id-1].append(path.first_node_id-1)
    return path_matrix


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
        thief_all_paths = view.config.graph.paths
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

        thief_posible_paths = [thief_path for thief_path in thief_all_paths if (thief_path.first_node_id == thief_current_node_id or thief_path.second_node_id == thief_current_node_id) and thief_path.price <= thief_current_money]
        thief_posible_paths.sort(key=lambda thief_path: thief_path.price, reverse=True)
       
        # visibles =  [agent for agent in visible_agents if agent.agent_type == 'POLICE' and agent.team == opponent_team]
        
        # message = ''
        # for m in range(len(view.visible_agents)):
        #     message = message  + '0'
        # self.phone.send_message(message)

        if not thief_posible_paths: 
            return thief_current_node_id
        else:
            output = random.choice(thief_posible_paths)
            if output.first_node_id == thief_current_node_id:
                return output.second_node_id
            else:
                return output.first_node_id

    def police_move_ai(self, view: GameView) -> int:
        # write your code here
        police_current_node_id = view.viewer.node_id
        police_current_money = view.balance
        police_all_paths = view.config.graph.paths
        num_all_nodes = len(view.config.graph.nodes)
        police_curent_turn = view.turn.turn_number
        police_visible_turns = view.config.visible_turns
        income_per_turn = view.config.police_income_each_turn
        visible_agents = view.visible_agents
        is_visible = police_curent_turn in police_visible_turns
        police_team = view.viewer.team
        
        if police_team == "FIRST":
            opponent_team = 'SECOND'
        else:
            opponent_team = 'FIRST'

        # num_team_police = len([agent.id for agent in visible_agents if agent.agent_type == 'POLICE' and agent.team == police_team])

        
        if is_visible:
            
            path_list = path2list(view.config.graph.paths, len(view.config.graph.nodes))
            visibles = [{agent.id:agent.node_id} for agent in visible_agents if agent.agent_type == 'THIEF' and agent.team == opponent_team]
            visibles = dict(ChainMap(*visibles))
            visible_paths = {}
            for id in [*visibles]:
                next, length = findpaths(g=path_list, src=police_current_node_id-1, dst=visibles.get(id)-1, v=num_all_nodes)
                visible_paths[next+1] = length
            if not len(visible_paths):
                return police_current_node_id
            else:
                return min(visible_paths, key=visible_paths.get)
        else:
            # self.phone.send_message('00101001')
            police_posible_paths = [police_path for police_path in police_all_paths if (police_path.first_node_id == police_current_node_id or police_path.second_node_id == police_current_node_id) and police_path.price <= police_current_money]
            police_posible_paths.sort(key=lambda police_path: police_path.price, reverse=True)        

            if not len(police_posible_paths):
                return police_current_node_id
            else:
                output = random.choice(police_posible_paths)
                if output.first_node_id == police_current_node_id:
                    return output.second_node_id
                else:
                    return output.first_node_id



        

