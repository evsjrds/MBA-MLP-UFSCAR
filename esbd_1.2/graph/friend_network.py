import random
import uuid
from graph.person import Person
from graph.models import PathType
from collections import deque

class FriendNetwork(object):
    def __init__(self, people_num, connections_num):
        self._people_num = people_num
        self._connections_num = connections_num
        self._graph = self._generate_graph()

    def _generate_graph(self):

        people = []
        for person_index in range(self._people_num):
            uid = str(uuid.uuid4())
            genre = 'female' if person_index % 2 else 'male'
            people.append(Person(uid, genre))

        conn_num = 0
        graph = {}
        graph_aux = {}  # criando um grafo auxiliar para agilizar algumas buscas

        # início - criando um caminho alternante
        person = people[conn_num]
        person_uid = person.get_uid()
        graph[person_uid] = {
            'this': person,
            'friends': []
        }
        graph_aux[person_uid] = {}

        while conn_num < self._people_num - 1:
            friend = people[conn_num + 1]
            friend_uid = friend.get_uid()
            graph[friend_uid] = {
                'this': friend,
                'friends': []
            }
            graph_aux[friend_uid] = {}

            graph[person_uid]['friends'].append(friend)
            graph[friend_uid]['friends'].append(person)
            graph_aux[person_uid][friend_uid] = True
            graph_aux[friend_uid][person_uid] = True
            conn_num += 1

            person = friend
            person_uid = friend_uid
        # fim - criando um caminho alternante

        while conn_num < self._connections_num:
            person, friend = random.sample(people, 2)
            person_uid = person.get_uid()
            friend_uid = friend.get_uid()

            if person_uid not in graph:
                graph[person_uid] = {
                    'this': person,
                    'friends': []
                }
                # criando um índice auxiliar para os vizinhos de cada vértice inserido no grafo
                graph_aux[person_uid] = {}

            if friend_uid not in graph:
                graph[friend_uid] = {
                    'this': friend,
                    'friends': []
                }
                # criando um índice auxiliar para os vizinhos de cada vértice inserido no grafo
                graph_aux[friend_uid] = {}

            if person_uid == friend_uid or \
                    friend_uid in graph_aux[person_uid]:
                continue

            graph[person_uid]['friends'].append(friend)
            graph[friend_uid]['friends'].append(person)
            # adicionar vizinho também nos índices do grafo auxiliar
            graph_aux[person_uid][friend_uid] = True
            graph_aux[friend_uid][person_uid] = True
            conn_num += 1

        return graph

    def get_person_by_uid(self, uid):
        return self._graph[uid]['this']
    
    def _regular_bfs(self, start_uid, target_uid, visited: dict) -> list:
        '''
        BFS padrão que encontra o caminho mais curto entre dois nós.
        '''
        queue = deque([start_uid])
        
        while queue:
            current_uid = queue.popleft()
            
            neighbors = self._graph[current_uid]['friends']
            
            for neighbor in neighbors:
                neighbor_uid = neighbor.get_uid()
                
                if neighbor_uid == target_uid:
                    visited[neighbor_uid] = current_uid
                    return self._reconstruct_path(target_uid, visited)
                
                if neighbor_uid not in visited:
                    visited[neighbor_uid] = current_uid
                    queue.append(neighbor_uid)
        
        return []

    def _alternating_bfs(self, start_uid, target_uid, visited: dict) -> list:
        '''
        BFS que segue apenas caminhos onde gêneros adjacentes são diferentes.
        '''
        start_genre = self._graph[start_uid]['this'].get_genre()
        queue = deque([(start_uid, start_genre)])
        
        while queue:
            current_uid, current_genre = queue.popleft()
            
            for neighbor in self._graph[current_uid]['friends']:
                neighbor_uid = neighbor.get_uid()
                neighbor_genre = neighbor.get_genre()
                
                if neighbor_genre != current_genre and neighbor_uid not in visited:
                    if neighbor_uid == target_uid:
                        visited[neighbor_uid] = current_uid
                        return self._reconstruct_path(target_uid, visited)
                    
                    visited[neighbor_uid] = current_uid
                    queue.append((neighbor_uid, neighbor_genre))
        
        return []

    def _reconstruct_path(self, target_uid, visited: dict) -> list:
        '''
        Reconstrói o caminho a partir do dicionário de nós visitados.
        '''
        path = deque()
        current = target_uid
        
        while current is not None:
            path.appendleft(current)
            current = visited[current]
            
        return list(path)

    def _search(self, person_uid, friend_uid, path_type: PathType) -> list:
        '''
        Encontra o caminho mais curto entre person_uid e friend_uid.
        
        Args:
            person_uid: ID do nó de origem
            friend_uid: ID do nó de destino
            path_type: Tipo de caminho (regular ou alternante)
        
        Returns:
            lista com o caminho mais curto (incluindo origem e destino) ou lista vazia se não houver caminho
        '''
        if person_uid == friend_uid:
            return [person_uid]
        
        visited = {person_uid: None}
        
        if path_type == PathType.regular:
            return self._regular_bfs(person_uid, friend_uid, visited)
        elif path_type == PathType.alternante:
            return self._alternating_bfs(person_uid, friend_uid, visited)
        else:
            raise ValueError(f"Tipo de caminho não suportado: {path_type}")
        
    def get_separation_degree(self, path_type: PathType):

        total_paths_len = 0
        for _ in range(100):
            person_uid, friend_uid = random.sample([*self._graph.keys()], 2)
            path = self._search(person_uid, friend_uid, path_type)
            total_paths_len += len(path) - 1
        return total_paths_len / 100