from modules.mapa import matriz_conexoes, calcular_peso
from modules.modulos import Colonia, Modulo
from collections import deque # Classe que guarda os módulos que ainda precisam ser visitados


def bfs(colonia, id_origem):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)}  # Cria um dicionário com nome do módulo e o índice (enumerate trás o indice e o value)
    

    if id_origem not in indices:
        print(f"Modulo de origem '{id_origem}' não encontrado na colônia.")  # Valida se o nome do módulo digitado existe na colônia, caso não exista, retorna uma mensagem de erro.
        return
        
    inicio = indices[id_origem] # Obtém o índice do módulo ao invés do nome

    visitados = [False] * len(modulos)  # Lista para marcar os módulos visitados
    
    fila = deque([inicio])  # Fila para armazenas os módulos que ainda precisam ser visitados
    visitados[inicio] = True # Marca o módulo de origem como já visitado
    ordem_visita = []  # Lista para armazenar a ordem de visita dos módulos

    while fila: # <- laço de repetição que para quando a lista esvazia
        atual = fila.popleft() # Remove o módulo da frente da fila(esquerda=left)
        ordem_visita.append(modulos[atual].id_nome) # Cria uma lista com os módulos visitados (id_nome)

        for vizinho in range(len(modulos)): # percorre toda a lista de módulos
            if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]: # Se atual tiver vizinho igual a 1, se não 0
                visitados[vizinho] = True # Troca de False p True e vai para o próximo
                fila.append(vizinho) # adiciona a fila de vizinhos que ainda serão visitados
    
    print(f"\n📡 BFS a partir de {id_origem}:") # Mostra o módulo de partida
    print(" → ".join(ordem_visita)) # Caminho percorrido
    return ordem_visita

"""

 Essa função BFS (Busca em Largura) percorre os módulos da colônia a partir de um módulo de origem, visitando os módulos vizinhos antes de avançar para os próximos níveis.
 Ela utiliza uma fila para armazenar os módulos que ainda precisam ser visitados e uma lista para marcar os módulos já visitados. 
 O resultado é a ordem de visita dos módulos a partir do módulo de origem.
 
 """

def dfs(colonia, id_origem):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)}  # Cria um dicionário com nome do módulo e o índice (enumerate trás o indice e o value)
    

    if id_origem not in indices:
        print(f"Modulo de origem '{id_origem}' não encontrado na colônia.")  # Valida se o nome do módulo digitado existe na colônia, caso não exista, retorna uma mensagem de erro.
        return
        
    inicio = indices[id_origem] # Obtém o índice do módulo ao invés do nome

    visitados = [False] * len(modulos)  # Lista para marcar os módulos visitados
    
    pilha = list([inicio])  # Pilha para armazenas os módulos que ainda precisam ser visitados
    visitados[inicio] = True # Marca o módulo de origem como já visitado
    ordem_visita = []  # Pilha para armazenar a ordem de visita dos módulos

    while pilha: # <- laço de repetição que para quando a lista esvazia
        atual = pilha.pop() # Remove o módulo da frente da pilha(esquerda=left)
        ordem_visita.append(modulos[atual].id_nome) # Cria uma lista com os módulos visitados (id_nome)

        for vizinho in range(len(modulos)): # percorre toda a lista de módulos
            if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]: # Se atual tiver vizinho igual a 1, se não 0
                visitados[vizinho] = True # Troca de False p True e vai para o próximo
                pilha.append(vizinho) # adiciona a pilha de vizinhos que ainda serão visitados
    
    print(f"\n📡 DFS a partir de {id_origem}:") # Mostra o módulo de partida
    print(" → ".join(ordem_visita)) # Caminho percorrido
    return ordem_visita

"""
Essa função DFS (Busca em profundidade) faz a mesma coisa que o BFS, porém, ao invés de usar uma fila, ela utiliza uma pilha para armazenar os módulos que ainda precisam ser visitados.

"""

def dijkstra(colonia, id_origem, id_destino):
    modulos = colonia.modulos
    indices = {m.id_nome: i for i, m in enumerate(modulos)} # Faz a mesma coisa que nas funções anterirores, cria um dicionário com nome do módulo e o índice (enumerate trás o indice e o value)


    if id_origem not in indices or id_destino not in indices:
        print("Modulo de origem ou destino não encontrado na colônia.") 
        return
    

    inicio = indices[id_origem] # Obtém o índice do módulo ao invés do nome
    destino = indices[id_destino] # Obtém o índice do módulo ao invés do nome
    n = len(modulos) # Obtém o número total de módulos na colônia

    custos = [float('inf')] * n # Cria uma lista de custos, onde o custo de cada módulo é inicialmente infinito
    custos[inicio] = 0 # O custo do módulo de origem é 0
    anteriores = [None] * n # Cria uma lista de anteriores, onde o anterior de cada módulo é inicialmente None
    visitados = [False] * n # Cria uma lista de visitados, onde o módulo é inicialmente não visitado(False)
    
    while True: # laço de repetição que para quando o módulo atual for igual ao destino ou quando não houver mais módulos para visitar
        atual = -1 # Variável para armazenar o índice do módulo atual, inicialmente definida como -1 (nenhum módulo selecionado)
        for i in range(n): # Percorre todos os módulos para encontrar o módulo não visitado com o menor custo
            if not visitados[i] and (atual == -1 or custos[i] < custos[atual]): # Procura o módulo com menor custo que ainda não foi visitado
                atual = i  # Atualiza para o módulo encontrado com menor custo

        if atual == -1 or atual == destino: # Se atual for o menor ou chegar no destino, para o laço
            break 

        visitados [atual] = True # Marca o módulo atual como visitado
    
        for vizinho in range(n): # Percorre os vizinhos do módulo atual
        
         if matriz_conexoes[atual][vizinho] == 1 and not visitados[vizinho]: # Se o módulo atual tiver um vizinho conectado e esse vizinho ainda não foi visitado
            peso = calcular_peso(modulos[atual], modulos[vizinho]) # Calcula o peso da conexão entre o módulo atual e o vizinho
            if custos[atual] + peso < custos[vizinho]: # Se o custo para chegar ao vizinho através do módulo atual for menor do que o custo atualmente registrado para o vizinho
                custos[vizinho] = custos[atual] + peso # Atualiza o custo para chegar ao vizinho
                anteriores[vizinho] = atual # Mostra o passos anteriores para chegar no menor
    if custos [destino] == float('inf'): # se o custo atual for infinito, significa que não há mais caminho
        print(f"Não há caminho entre {id_origem} e {id_destino}.") # Mostra a mensagem de erro
        return
    
    caminho = [] # Cria uma lista para armazenar o caminho do módulo de origem até o módulo de destino
    atual = destino # Inicializa o módulo atual como o destino

    while atual is not None: # Enquanto o módulo atual não for None (ou seja, enquanto houver um caminho)
        caminho.append(modulos[atual].id_nome) # Adiciona o módulo atual ao caminho
        atual = anteriores[atual] # Volta para o módulo anterior no caminho  
    caminho.reverse() # Inverte a lista para mostrar o caminho do módulo de origem até o módulo de destino

    print(f"\n🛰️ Dijkstra — Caminho mais eficiente de {id_origem} até {id_destino}:")
    print(" → ".join(caminho))
    print(f"Custo total: {custos[destino]:.2f}")
    return caminho, custos[destino]

"""
Função que calcula qual é o caminho mais eficiente e barato entre os módulos
"""
