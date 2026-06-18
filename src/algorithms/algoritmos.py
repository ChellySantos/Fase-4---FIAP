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

