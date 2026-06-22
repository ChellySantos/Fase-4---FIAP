"""
Script de testes do SIGIC.
Roda direto: python3 testes.py

A ideia: chamamos cada função do sistema diretamente (sem passar pelo menu)
e usamos 'assert' para checar se o resultado é o que esperamos.
Se algum assert falhar, o Python para e mostra exatamente qual checagem quebrou.
"""

from sistema import inicializar_colonia
from algorithms.algoritmos import bfs, dfs, dijkstra, conexoes_criticas
from modules.mapa import matriz_conexoes


def teste_bfs():
    colonia = inicializar_colonia()
    resultado = bfs(colonia, "HAB-01")

    # Esperamos que o BFS visite TODOS os 8 módulos, já que a rede é conectada
    assert len(resultado) == 8, f"Esperava 8 módulos visitados, veio {len(resultado)}"

    # O primeiro módulo visitado tem que ser sempre a origem
    assert resultado[0] == "HAB-01", f"Esperava começar em HAB-01, veio {resultado[0]}"

    print("✅ teste_bfs passou")


def teste_bfs_origem_invalida():
    colonia = inicializar_colonia()
    resultado = bfs(colonia, "MODULO-FANTASMA")

    # Módulo que não existe deve retornar None, não quebrar o programa
    assert resultado is None, f"Esperava None para módulo inválido, veio {resultado}"

    print("✅ teste_bfs_origem_invalida passou")


def teste_dfs():
    colonia = inicializar_colonia()
    resultado = dfs(colonia, "HAB-01")

    assert len(resultado) == 8, f"Esperava 8 módulos visitados, veio {len(resultado)}"
    assert resultado[0] == "HAB-01"

    print("✅ teste_dfs passou")


def teste_dijkstra_caminho_direto():
    colonia = inicializar_colonia()
    # HAB-01 e CTR-01 têm conexão direta na matriz (posição [0][1] = 1)
    resultado = dijkstra(colonia, "HAB-01", "CTR-01")

    assert resultado is not None, "Dijkstra não deveria retornar None aqui"
    caminho, custo = resultado

    # Caminho direto = só 2 módulos (origem e destino)
    assert len(caminho) == 2, f"Esperava caminho direto de 2 módulos, veio {len(caminho)}"
    assert custo > 0, "Custo não pode ser zero ou negativo"

    print(f"✅ teste_dijkstra_caminho_direto passou (custo={custo:.2f})")


def teste_dijkstra_mesmo_modulo():
    colonia = inicializar_colonia()
    resultado = dijkstra(colonia, "HAB-01", "HAB-01")

    assert resultado is not None
    caminho, custo = resultado

    # Origem igual ao destino: custo deve ser zero
    assert custo == 0, f"Esperava custo 0 para mesmo módulo, veio {custo}"

    print("✅ teste_dijkstra_mesmo_modulo passou")


def teste_conexoes_criticas_rede_real():
    colonia = inicializar_colonia()
    criticas = conexoes_criticas(colonia)

    # Sabemos (testamos manualmente) que a rede da colônia não tem conexão crítica
    assert criticas == [], f"Esperava lista vazia, veio {criticas}"

    print("✅ teste_conexoes_criticas_rede_real passou")


def teste_conexoes_criticas_rede_em_linha():
    # Rede artificial A-B-C: aqui SABEMOS que A-B e B-C são críticas
    from modules.modulos import Colonia, Modulo
    import modules.mapa as mapa_module

    colonia_teste = Colonia()
    colonia_teste.adicionar_modulo(Modulo("A", "t", "f", 1, 1, 1, 1, "ativo", (0, 0)))
    colonia_teste.adicionar_modulo(Modulo("B", "t", "f", 1, 1, 1, 1, "ativo", (1, 0)))
    colonia_teste.adicionar_modulo(Modulo("C", "t", "f", 1, 1, 1, 1, "ativo", (2, 0)))

    matriz_original = mapa_module.matriz_conexoes
    mapa_module.matriz_conexoes = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]

    criticas = conexoes_criticas(colonia_teste)
    assert len(criticas) == 2, f"Esperava 2 conexões críticas, veio {len(criticas)}"

    # Restaura a matriz original para não afetar outros testes
    mapa_module.matriz_conexoes = matriz_original

    print("✅ teste_conexoes_criticas_rede_em_linha passou")


def teste_matriz_simetrica():
    # Conexão entre A e B implica conexão entre B e A (grafo não-direcionado)
    n = len(matriz_conexoes)
    for i in range(n):
        for j in range(n):
            assert matriz_conexoes[i][j] == matriz_conexoes[j][i], \
                f"Matriz não é simétrica na posição [{i}][{j}]"

    print("✅ teste_matriz_simetrica passou")


if __name__ == "__main__":
    print("Executando bateria de testes do SIGIC...\n")

    teste_bfs()
    teste_bfs_origem_invalida()
    teste_dfs()
    teste_dijkstra_caminho_direto()
    teste_dijkstra_mesmo_modulo()
    teste_conexoes_criticas_rede_real()
    teste_conexoes_criticas_rede_em_linha()
    teste_matriz_simetrica()

    print("\n🎉 Todos os testes passaram!")