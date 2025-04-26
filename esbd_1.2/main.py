from graph.friend_network import FriendNetwork
from graph.friend_network import PathType

NUM_VERTICES = [100, 1000]#, 10000, 100000]
NUM_MEDIO_ARESTAS_POR_VERTICES_FACTORS = ["5", "raiz(n)", "n/5"]

def get_num_medio_arestas_por_vertice(num_vertice, factor):
    if factor == "5":
        return 5
    elif factor == "raiz(n)":
        return int(num_vertice ** 0.5)
    elif factor == "n/5":
        return int(num_vertice / 5)
    
def get_separation_degree(people_num: int, connections_num: int, path_type: PathType):
    friend_network = FriendNetwork(people_num, connections_num)
    return friend_network.get_separation_degree(path_type)

if __name__ == '__main__':
    print('----------------------Graus de Separação em Redes Sociais-----------------------------------')
    print()
    #REGULAR ANALYSIS
    for people_num in NUM_VERTICES:
        print('Numero de Vertices: ', people_num)
        for connections_num_factor in NUM_MEDIO_ARESTAS_POR_VERTICES_FACTORS:
            print('Fator de Arestas: ', connections_num_factor)
            regular_connections_num = int((get_num_medio_arestas_por_vertice(people_num, connections_num_factor) * people_num) / 2)
            print('Numero de Arestas: ', regular_connections_num)
            regular_separation_degree = get_separation_degree(people_num, regular_connections_num, PathType.regular)
            print("Graus de Separação, Análise Regular", regular_separation_degree)
    print('---------------------------------------------------------------------------------------------')
     
    #ALTERNANTE ANALYSIS
    for people_num in NUM_VERTICES:
        print('Numero de Vertices: ', people_num)
        for connections_num_factor in NUM_MEDIO_ARESTAS_POR_VERTICES_FACTORS:
            print('Fator de Arestas: ', connections_num_factor)
            alternante_connections_num = int((get_num_medio_arestas_por_vertice(people_num, connections_num_factor) * people_num) / 2)
            print('Numero de Arestas: ', alternante_connections_num)
            alternante_separation_degree = get_separation_degree(people_num, alternante_connections_num, PathType.alternante)       
            print("Graus de Separação, Análise Alternante", alternante_separation_degree)
            print()
    print('---------------------------------------------------------------------------------------------')