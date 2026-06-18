import matplotlib.pyplot as plt
import math as math
from modules.modulos import  *

matriz_conexoes = [
    # HAB CTR ENE AGR LAB COM MED OXI
    [0, 1, 0, 1, 0, 0, 1, 0],  # HAB
    [1, 0, 1, 1, 1, 1, 1, 1],  # CTR
    [0, 1, 0, 1, 0, 0, 0, 1],  # ENE
    [1, 1, 1, 0, 0, 0, 0, 0],  # AGR
    [0, 1, 0, 0, 0, 1, 0, 1],  # LAB
    [0, 1, 0, 0, 1, 0, 1, 0],  # COM
    [1, 1, 0, 0, 0, 1, 0, 0],  # MED
    [0, 1, 1, 0, 1, 0, 0, 0],  # OXI
]

def mapa_colonia(colonia, matriz_conexoes):
    #Obtém a lista de módulos da colônia e a quantidade total de módulos
    modulos = colonia.modulos
    n = len(modulos)

    #Cria o mapa
    plt.figure()
    plt.xlim(0, 10)
    plt.ylim(0, 10)

    #Percorre a matriz de conexões e ilustra as redes da colônia
    for i in range(n):
        for j in range(i + 1, n):
            if matriz_conexoes[i][j] == 1:
                x1, y1 = modulos[i].coordenada
                x2, y2 = modulos[j].coordenada
                plt.plot([x1, x2], [y1, y2], "-", color="gray", linewidth=1, zorder=1)

    #Representa cada módulo como um ponto no mapa
    for modulo in modulos:
        x = modulo.coordenada[0]
        y = modulo.coordenada[1]
        plt.plot(x, y, "o", markersize=10, zorder=2)
        plt.text(x + 0.1, y + 0.1, modulo.id_nome)

    #Salva o mapa
    plt.title("Mapa da Colônia")
    plt.grid(True)
    plt.savefig("Mapa_Colonia.png")

def calcular_distancia(modulo_origem,modulo_destino):
    #Calcula a menor distância entre o módulo de origem e destino
    x1, y1 = modulo_origem.coordenada
    x2, y2 = modulo_destino.coordenada
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia

def calcular_peso(modulo_origem, modulo_destino, detalhado=False):
    #Converte a distância do mapa para metros reais e calcula o tempo e o consumo da transmissão
    distancia_mapa = calcular_distancia(modulo_origem, modulo_destino)
    distancia_m = distancia_mapa * 500
    tempo_comunicacao = distancia_mapa * 0.5
    consumo_comunicacao = tempo_comunicacao * 5
    peso = distancia_m + tempo_comunicacao + consumo_comunicacao
    if detalhado:
        return peso, distancia_m, tempo_comunicacao, consumo_comunicacao
    return peso