import pandas as pd
from graph.friend_network import FriendNetwork
from graph.friend_network import PathType

NUM_VERTICES = [100, 1_000] #[100, 1000, 10_000, 100_00] 
FACTORS = ["5", "raiz(n)", "n/5"]

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

columns = ["# Vértices (n)", "Regular - 5", "Regular - raiz(n)", "Regular - n/5", 
           "Alternante - 5", "Alternante - raiz(n)", "Alternante - n/5"]

results = []

print('---------------- Graus de Separação em Redes Sociais ----------------\n')

for people_num in NUM_VERTICES:
    row = [people_num]

    #REGULAR ANALYSIS
    for factor in FACTORS:
        connections_num = int((get_num_medio_arestas_por_vertice(people_num, factor) * people_num) / 2)
        separation_degree = get_separation_degree(people_num, connections_num, PathType.regular)
        row.append(separation_degree)

    #ALTERNANTE ANALYSIS
    for factor in FACTORS:
        connections_num = int((get_num_medio_arestas_por_vertice(people_num, factor) * people_num) / 2)
        separation_degree = get_separation_degree(people_num, connections_num, PathType.alternante)
        row.append(separation_degree)

    results.append(row)

df = pd.DataFrame(results, columns=columns)

print(df.to_string(index=False))

print('\n---------------------------------------------------------------------')
