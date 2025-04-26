import random
import uuid
from graph.person import Person
from graph.models import PathType

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

    def _search(self, person_uid, friend_uid, path_type: PathType):
        '''
        TODO

        Esta função DEVE retornar uma lista com o caminho mais curto (incluindo origem e destino)
        percorrido para encontrar o friend_uid partindo do person_uid
        '''

        if path_type == PathType.regular:
            pass
        elif path_type == PathType.alternante:
            pass

        path = []

        return path

    def get_separation_degree(self, path_type: PathType):

        total_paths_len = 0
        for _ in range(100):
            person_uid, friend_uid = random.sample([*self._graph.keys()], 2)
            path = self._search(person_uid, friend_uid, path_type)
            total_paths_len += len(path) - 1

        return total_paths_len / 100