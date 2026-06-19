from modules.mapa import matriz_conexoes, calcular_peso
from modules.modulos import Colonia, Modulo
from collections import deque  # Classe que guarda os módulos que ainda precisam ser visitados


def bfs(colonia, id_origem):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)}  # Cria um dicionário com nome do módulo como chave e índice como valor

    if id_origem not in indices:  # Valida se o módulo digitado existe na colônia
        print(f"Módulo de origem '{id_origem}' não encontrado na colônia.")
        return

    inicio = indices[id_origem]  # Traduz o nome do módulo para o índice na matriz

    visitados = [False] * len(modulos)  # Lista de controle de visita, todos começam como False
    fila = deque([inicio])  # Fila de módulos que ainda precisam ser visitados, começa com a origem
    visitados[inicio] = True  # Marca o módulo de origem como já visitado
    ordem_visita = []  # Lista que armazena a ordem de visita dos módulos

    while fila:  # Continua enquanto houver módulos na fila
        atual = fila.popleft()  # Remove o módulo da frente da fila (primeiro a entrar, primeiro a sair)
        ordem_visita.append(modulos[atual].id_nome)  # Adiciona o módulo atual à ordem de visita

        for vizinho in range(len(modulos)):  # Percorre todos os possíveis vizinhos do módulo atual
            if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]:  # Se há conexão e o vizinho ainda não foi visitado
                visitados[vizinho] = True  # Marca o vizinho como visitado
                fila.append(vizinho)  # Adiciona o vizinho na fila para ser explorado depois

    print(f"\n📡 BFS a partir de {id_origem}:")
    print(" → ".join(ordem_visita))  # Exibe o caminho percorrido separado por →
    return ordem_visita

"""

 Essa função BFS (Busca em Largura) percorre os módulos da colônia a partir de um módulo de origem, visitando os módulos vizinhos antes de avançar para os próximos níveis.
 Ela utiliza uma fila para armazenar os módulos que ainda precisam ser visitados e uma lista para marcar os módulos já visitados. 
 O resultado é a ordem de visita dos módulos a partir do módulo de origem.
 
 """

def dfs(colonia, id_origem):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)}  # Cria um dicionário com nome do módulo como chave e índice como valor

    if id_origem not in indices:  # Valida se o módulo digitado existe na colônia
        print(f"Módulo de origem '{id_origem}' não encontrado na colônia.")
        return

    inicio = indices[id_origem]  # Traduz o nome do módulo para o índice na matriz

    visitados = [False] * len(modulos)  # Lista de controle de visita, todos começam como False
    pilha = [inicio]  # Pilha de módulos que ainda precisam ser visitados, começa com a origem
    visitados[inicio] = True  # Marca o módulo de origem como já visitado
    ordem_visita = []  # Lista que armazena a ordem de visita dos módulos

    while pilha:  # Continua enquanto houver módulos na pilha
        atual = pilha.pop()  # Remove o módulo do topo da pilha (último a entrar, primeiro a sair)
        ordem_visita.append(modulos[atual].id_nome)  # Adiciona o módulo atual à ordem de visita

        for vizinho in range(len(modulos)):  # Percorre todos os possíveis vizinhos do módulo atual
            if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]:  # Se há conexão e o vizinho ainda não foi visitado
                visitados[vizinho] = True  # Marca o vizinho como visitado
                pilha.append(vizinho)  # Adiciona o vizinho na pilha para ser explorado depois

    print(f"\n📡 DFS a partir de {id_origem}:")
    print(" → ".join(ordem_visita))  # Exibe o caminho percorrido separado por →
    return ordem_visita

"""
Essa função DFS (Busca em profundidade) faz a mesma coisa que o BFS, porém, ao invés de usar uma fila, ela utiliza uma pilha para armazenar os módulos que ainda precisam ser visitados.

"""

def dijkstra(colonia, id_origem, id_destino):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)}  # Cria um dicionário com nome do módulo como chave e índice como valor

    if id_origem not in indices or id_destino not in indices:  # Valida se os módulos de origem e destino existem na colônia
        print("Módulo de origem ou destino não encontrado na colônia.")
        return

    inicio = indices[id_origem]  # Traduz o nome do módulo de origem para o índice na matriz
    destino = indices[id_destino]  # Traduz o nome do módulo de destino para o índice na matriz
    n = len(modulos)  # Total de módulos na colônia

    custos = [float('inf')] * n  # Lista de custos, todos começam como infinito
    custos[inicio] = 0  # O custo para chegar na origem é zero
    anteriores = [None] * n  # Armazena o módulo anterior no caminho mais barato para cada módulo
    visitados = [False] * n  # Lista de controle de visita, todos começam como False

    while True:  # Continua até chegar no destino ou não restar módulos para visitar
        atual = -1  # Inicializa como -1 (nenhum módulo selecionado)
        for i in range(n):  # Procura o módulo não visitado com menor custo
            if not visitados[i] and (atual == -1 or custos[i] < custos[atual]):
                atual = i  # Atualiza para o módulo com menor custo encontrado

        if atual == -1 or atual == destino:  # Para quando chegar no destino ou não houver mais módulos
            break

        visitados[atual] = True  # Marca o módulo atual como visitado

        for vizinho in range(n):  # Percorre os vizinhos do módulo atual
            if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]:  # Se há conexão e o vizinho não foi visitado
                peso = calcular_peso(modulos[atual], modulos[vizinho])  # Calcula o peso da conexão
                if custos[atual] + peso < custos[vizinho]:  # Se encontrou um caminho mais barato
                    custos[vizinho] = custos[atual] + peso  # Atualiza o custo do vizinho
                    anteriores[vizinho] = atual  # Registra por qual módulo chegou mais barato

    if custos[destino] == float('inf'):  # Se o custo ainda for infinito, não existe caminho
        print(f"Não há caminho entre {id_origem} e {id_destino}.")
        return

    caminho = []  # Lista para reconstruir o caminho do destino até a origem
    atual = destino  # Começa a reconstrução pelo destino

    while atual is not None:  # Volta pelo caminho usando a lista de anteriores
        caminho.append(modulos[atual].id_nome)  # Adiciona o módulo atual ao caminho
        atual = anteriores[atual]  # Vai para o módulo anterior
    caminho.reverse()  # Inverte para mostrar da origem ao destino

    print(f"\n🛰️ Dijkstra — Caminho mais eficiente de {id_origem} até {id_destino}:")
    print(" → ".join(caminho))
    print(f"Custo total: {custos[destino]:.2f}")
    return caminho, custos[destino]

"""
Função que calcula qual é o caminho mais eficiente e barato entre os módulos
"""

def conexoes_criticas(colonia):
    modulos = colonia.modulos
    n = len(modulos)

    visitados = [False] * n  # Lista de controle de visita, todos começam como False
    descoberta = [-1] * n  # Registra em qual tempo cada módulo foi descoberto
    baixo = [-1] * n  # Registra o menor tempo de descoberta alcançável por aquele módulo
    criticas = []  # Lista que armazenará as conexões críticas encontradas
    timer = [0]  # Contador de tempo, incrementa a cada módulo visitado

    def dfs_critica(v, pai):
        visitados[v] = True  # Marca o módulo atual como visitado
        descoberta[v] = baixo[v] = timer[0]  # Define o tempo de descoberta e o menor tempo alcançável
        timer[0] += 1  # Incrementa o timer

        for vizinho in range(n):
            if matriz_conexoes[v][vizinho] == 1:  # Se há conexão entre o módulo atual e o vizinho
                if not visitados[vizinho]:  # Se o vizinho ainda não foi visitado
                    dfs_critica(vizinho, v)  # Explora o vizinho recursivamente
                    baixo[v] = min(baixo[v], baixo[vizinho])  # Atualiza o menor tempo alcançável do módulo atual
                    if baixo[vizinho] > descoberta[v]:  # Se o vizinho não alcança o módulo atual por outro caminho
                        criticas.append((modulos[v].id_nome, modulos[vizinho].id_nome))  # Conexão é crítica
                elif vizinho != pai:  # Se o vizinho já foi visitado e não é o módulo pai
                    baixo[v] = min(baixo[v], descoberta[vizinho])  # Atualiza o menor tempo alcançável

    for i in range(n):  # Garante que todos os módulos sejam visitados
        if not visitados[i]:  # Se o módulo ainda não foi visitado
            dfs_critica(i, -1)  # Inicia o DFS a partir dele, -1 indica que não tem módulo pai

    if not criticas:  # Se a lista de conexões críticas estiver vazia
        print("Nenhuma conexão crítica encontrada na rede.")
    else:
        print(f"Conexões críticas encontradas ({len(criticas)}):")
        for a, b in criticas:  # Percorre cada conexão crítica encontrada
            print(f"  {a} ↔ {b}")  # Exibe os dois módulos que formam a conexão crítica
    return criticas