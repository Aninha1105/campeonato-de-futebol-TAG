import networkx as nx  # Importa a biblioteca NetworkX para trabalhar com grafos
from itertools import combinations  # Importa para gerar combinações de elementos
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para visualização de gráficos
from collections import defaultdict  # Importa defaultdict para contagem de rodadas de forma eficiente
import matplotlib.patches as mpatches # Importa mpatches para visualização da tabela

def is_valid_assignment(node, round_assignment, graph, round_count, max_games_per_round):
    """
    Verifica se a atribuição de rodada para o jogo (node) respeita as restrições:
      - O jogo não pode ser alocado em uma rodada proibida (ver restricoes_rodadas);
      - A rodada já não deve ter atingido o limite de jogos;
      - Jogos que conflitam (por compartilharem times ou por restrições de mandante)
        não podem ocorrer na mesma rodada.
    
    Parâmetros:
      - node (tuple): O jogo a ser alocado (exemplo: ('TFC', 'AFC'))
      - round_assignment (dict): Atribuição de rodadas atual para os jogos
      - graph (networkx.Graph): O grafo que representa os jogos e as conexões entre eles
      - round_count (dict): Contagem do número de jogos por rodada
      - max_games_per_round (int): Número máximo de jogos permitidos por rodada
    
    Retorna:
      - bool: True se a atribuição for válida, False caso contrário.
    """
    rodada = round_assignment[node]
    
    # Verifica restrições específicas de rodadas
    restricoes = []
    if node in restricoes_rodadas:
        restricoes = restricoes_rodadas[node]
    elif (node[1], node[0]) in restricoes_rodadas:
        restricoes = restricoes_rodadas[(node[1], node[0])]
    if restricoes and int(rodada[1:]) in restricoes:
        return False

    # Verifica se a rodada já atingiu o limite de jogos
    if round_count[rodada] >= max_games_per_round:
        return False

    # Verifica conflitos com jogos adjacentes (jogos que compartilham times ou por restrição de mandante)
    for neighbor in graph[node]:
        if neighbor in round_assignment and round_assignment[neighbor] == rodada:
            return False

    return True

def backtracking_coloring(graph, max_colors=14, max_games_per_round=3):
    """
    Algoritmo de backtracking para atribuir rodadas (cores) aos jogos,
    respeitando as restrições impostas.
    
    Parâmetros:
      - graph (networkx.Graph): O grafo representando os jogos e as restrições entre eles
      - max_colors (int): Número máximo de rodadas (cores) a serem utilizadas
      - max_games_per_round (int): Número máximo de jogos permitidos por rodada
    
    Retorna:
      - dict: Atribuição de rodadas (cores) para os jogos ou None se não for possível alocar.
    """
    # Seleciona apenas os nós referentes a jogos (tuplas)
    jogos = [node for node in graph if isinstance(node, tuple)]
    round_assignment = {}  # Armazena a rodada atribuída a cada jogo
    round_count = {f"R{i}": 0 for i in range(1, max_colors + 1)}  # Contagem de jogos por rodada

    def solve(index):
        if index == len(jogos):
            return True  # Todos os jogos foram alocados com sucesso
        node = jogos[index]
        for rodada in round_count:
            round_assignment[node] = rodada
            if is_valid_assignment(node, round_assignment, graph, round_count, max_games_per_round):
                round_count[rodada] += 1
                if solve(index + 1):
                    return True
                round_count[rodada] -= 1  # Backtracking
            del round_assignment[node]
        return False

    if solve(0):
        return round_assignment
    else:
        return None

def visualizar_grafo_coloring(G, coloring):
    """
    - Visualiza o grafo normal (apenas nós de jogos) com as cores representando as rodadas.
    - Adiciona uma legenda com a cor e o número da rodada.
    
    Parâmetros:
      - G (networkx.Graph): O grafo de jogos
      - coloring (dict): Atribuição de rodadas para os jogos
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42)  # Layout "spring" para visualização orgânica

    # Define normalização para os valores das rodadas (1 a 14)
    norm = plt.Normalize(vmin=1, vmax=14)
    node_colors = []
    for node in G.nodes():
        if node in coloring:
            try:
                round_number = int(coloring[node][1:])
                # Obtém a cor correspondente à rodada
                node_colors.append(plt.cm.rainbow(norm(round_number)))
            except:
                node_colors.append("gray")
        else:
            node_colors.append("gray")
    
    # Desenha os nós e arestas
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax, node_size=800)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")
    
    # Renomeia os nós para o formato "A X B"
    labels = {node: f"{node[0]} X {node[1]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax)
    
    # Cria legendas para cada rodada de 1 a 14
    patches = []
    for r in range(1, 15):
        color = plt.cm.rainbow(norm(r))
        patch = mpatches.Patch(color=color, label="Rodada " + str(r))
        patches.append(patch)
    ax.legend(handles=patches, title="Rodadas", bbox_to_anchor=(1, 1))
    
    plt.title("Grafo do Campeonato de Futebol com Atribuição de Jogos por Rodadas")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def add_edge_for_restrictions(jogos, restricoes_mandante, G):
    """
    Adiciona arestas ao grafo com base nas restrições gerais e específicas de mandante.
    
    Parâmetros:
      - jogos (list): Lista de todos os jogos possíveis.
      - restricoes_mandantes (dict): Dicionário contendo as restrições de mandante (tupla de times).
      - G (Graph): Grafo onde as arestas serão adicionadas.
    """
    for jogo1, jogo2 in combinations(jogos, 2):
        # Restrição geral: um time não pode jogar mais de uma vez na mesma rodada
        if jogo1[0] in jogo2 or jogo1[1] in jogo2: 
            G.add_edge(jogo1, jogo2)

        # Restrição específica: dois times não podem ser mandantes simultaneamente
        for (time1, time2), tipo in restricoes_mandante.items(): 
            if (jogo1[0] == time1 and jogo2[0] == time2) or (jogo1[0] == time2 and jogo2[0] == time1):
                G.add_edge(jogo1, jogo2)

def print_schedule(schedule):
    """
    Imprime o cronograma de jogos, organizado por rodada.
    
    Parâmetros:
      - schedule (dict): Dicionário com as rodadas como chave e os jogos como valor.
    """
    # Organiza os jogos por rodada
    for rodada, jogos_list in sorted(schedule.items(), key=lambda x: int(x[0][1:])):
        print(f"Rodada {rodada[1:]}: ")
        for (t1, t2) in jogos_list:
            print(f"{t1} X {t2}")
        print()

# Lista de times
times = ["DFC", "TFC", "AFC", "LFC", "FFC", "OFC", "CFC"]

# Criar todos os jogos possíveis (ida e volta)
jogos = [(t1, t2) for t1, t2 in combinations(times, 2)]  # Gera todas as combinações de jogos
jogos += [(t2, t1) for t1, t2 in jogos]  # Adiciona os jogos de volta

# Cria o grafo normal com apenas nós de jogos
G = nx.Graph()
G.add_nodes_from(jogos)

# Restrições Específicas do Projeto
restricoes_mandante = {
    ("TFC", "OFC"): "mandante",  # Restrição de mandante para TFC e OFC
    ("AFC", "FFC"): "mandante",  # Restrição de mandante para AFC e FFC
}

restricoes_rodadas = {
    ("DFC", "CFC"): [1, 14],  # Jogo proibido nas rodadas 1 e 14
    ("LFC", "FFC"): [7, 13],  # LFC x FFC proibido nas rodadas 7 e 13
    ("OFC", "LFC"): [10, 11],  # OFC x LFC proibido nas rodadas 10 e 11
    ("AFC", "FFC"): [12, 13],  # AFC x FFC proibido nas rodadas 12 e 13
    ("CFC", "TFC"): [2, 3]  # CFC x TFC proibido nas rodadas 2 e 3
}

# Adicionar as restrições como arestas
add_edge_for_restrictions(jogos, restricoes_mandante, G)

# Gerar a coloração com Backtracking
coloracao = backtracking_coloring(G)

# Organizar os jogos por rodada
schedule = defaultdict(list)
for jogo, rodada in coloracao.items():
    schedule[rodada].append(jogo)
print_schedule(schedule)

# Exibe o grafo
visualizar_grafo_coloring(G, coloracao)