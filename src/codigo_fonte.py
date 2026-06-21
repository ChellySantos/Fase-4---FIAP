from modules.mapa import matriz_conexoes, mapa_colonia
from algorithms.algoritmos import bfs, dfs, dijkstra
from sistema import inicializar_colonia
import matplotlib.pyplot as plt


def selecionar_modulo(colonia, mensagem, excluir=[]):
    # Exibe a lista de módulos disponíveis para seleção, excluindo os módulos offline
    print(f"\n{mensagem}")
    modulos_disponiveis = [m for m in colonia.modulos if m.id_nome not in excluir]
    for i, modulo in enumerate(modulos_disponiveis):
        print(f"  {i + 1}. {modulo.id_nome} — {modulo.tipo}")

    while True:
        escolha = input("Escolha o número do módulo: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(modulos_disponiveis):
            return modulos_disponiveis[int(escolha) - 1].id_nome
        print("Opção inválida. Tente novamente.")


def simular_falha_na_rede(colonia):
    # Exibe o submenu de simulação
    print("\n╔══════════════════════════════════════════╗")
    print("║        Simular Falha na Rede             ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Simular remoção de conexão           ║")
    print("║  2. Simular módulo(s) offline            ║")
    print("║  0. Voltar                               ║")
    print("╚══════════════════════════════════════════╝")

    sub_opcao = input("\nEscolha uma opção: ")

    match sub_opcao:
        case "1":
            # Simula a remoção temporária de uma conexão e analisa o impacto na rede
            origem = selecionar_modulo(colonia, "Selecione o módulo de origem da conexão:")
            destino = selecionar_modulo(colonia, "Selecione o módulo de destino da conexão:")
            indices = {m.id_nome: i for i, m in enumerate(colonia.modulos)}

            if origem in indices and destino in indices:
                i, j = indices[origem], indices[destino]

                # Verifica se a conexão existe antes de remover
                if matriz_conexoes[i][j] == 0:
                    print(f"\n❌ Não existe conexão entre {origem} e {destino}.")
                else:
                    # Remove a conexão temporariamente
                    matriz_conexoes[i][j] = 0
                    matriz_conexoes[j][i] = 0
                    print(f"\n🔌 Conexão {origem} ↔ {destino} removida temporariamente.")

                    # Usa BFS para verificar quais módulos ainda são alcançáveis
                    visitados_sim = bfs(colonia, origem)

                    # Verifica quais módulos ficaram isolados
                    todos = [m.id_nome for m in colonia.modulos]
                    isolados = [m for m in todos if m not in visitados_sim]

                    if isolados:
                        print(f"\n⚠️  ALERTA: Os seguintes módulos ficaram ISOLADOS da rede:")
                        for m in isolados:
                            print(f"  ❌ {m}")
                        print(f"\n🚨 Essa é uma conexão CRÍTICA para a infraestrutura!")
                    else:
                        print(f"\n✅ Rede ainda conectada — todos os módulos permanecem acessíveis.")
                        print(f"   A conexão {origem} ↔ {destino} NÃO é crítica.")

                        # Mostra o caminho alternativo entre os dois módulos
                        print(f"\n🔁 Caminho alternativo entre {origem} e {destino}:")
                        dijkstra(colonia, origem, destino)

                    # Restaura a conexão original
                    matriz_conexoes[i][j] = 1
                    matriz_conexoes[j][i] = 1
                    print(f"\n🔧 Conexão {origem} ↔ {destino} restaurada.")
            else:
                print("Módulo não encontrado.")

        case "2":
            # Simula múltiplos módulos offline e analisa o impacto na rede
            print("\nQuantos módulos deseja desativar?")
            qtd = input("Quantidade: ")

            if not qtd.isdigit() or int(qtd) < 1:
                print("Quantidade inválida.")
            else:
                qtd = int(qtd)
                modulos_offline = []
                conexoes_salvas = {}
                indices = {m.id_nome: i for i, m in enumerate(colonia.modulos)}
                n = len(colonia.modulos)

                # Seleciona os módulos a desativar
                for k in range(qtd):
                    modulo_id = selecionar_modulo(colonia, f"Selecione o módulo {k + 1} para desativar:", excluir=modulos_offline)
                    if modulo_id not in modulos_offline:
                        modulos_offline.append(modulo_id)

                # Remove as conexões de todos os módulos offline
                for modulo_id in modulos_offline:
                    idx = indices[modulo_id]
                    conexoes_salvas[modulo_id] = []
                    for j in range(n):
                        if matriz_conexoes[idx][j] == 1:
                            conexoes_salvas[modulo_id].append(j)
                            matriz_conexoes[idx][j] = 0  # Remove conexão do módulo offline
                            matriz_conexoes[j][idx] = 0
                    print(f"⛔ Módulo {modulo_id} desativado.")

                # Escolhe o módulo de origem pra testar conectividade, excluindo os offline
                origem_teste = selecionar_modulo(colonia, "Selecione o módulo de origem para testar conectividade:", excluir=modulos_offline)

                # Usa BFS pra verificar quais módulos ainda são alcançáveis
                visitados_sim = bfs(colonia, origem_teste)

                # Verifica quais módulos ficaram isolados
                modulos_restantes = [m.id_nome for m in colonia.modulos if m.id_nome not in modulos_offline]
                isolados = [m for m in modulos_restantes if m not in visitados_sim]

                if isolados:
                    print(f"\n⚠️  ALERTA: Os seguintes módulos ficaram ISOLADOS:")
                    for m in isolados:
                        print(f"  ❌ {m}")
                    print(f"\n🚨 A combinação de módulos offline é CRÍTICA para a infraestrutura!")
                else:
                    print(f"\n✅ Rede ainda conectada — todos os módulos permanecem acessíveis.")

                # Restaura todas as conexões originais
                for modulo_id in modulos_offline:
                    idx = indices[modulo_id]
                    for j in conexoes_salvas[modulo_id]:
                        matriz_conexoes[idx][j] = 1
                        matriz_conexoes[j][idx] = 1
                    print(f"🔧 Módulo {modulo_id} restaurado.")

        case "0":
            # Volta ao menu principal
            pass

        case _:
            print("Opção inválida.")


def menu():
    colonia = inicializar_colonia()

    while True:
        print("\n╔══════════════════════════════════════════╗")
        print("║     SIGIC — Sistema de Gerenciamento     ║")
        print("║        da Infraestrutura da Colônia      ║")
        print("╠══════════════════════════════════════════╣")
        print("║  1. Visualizar rede da colônia           ║")
        print("║  2. Consultar módulos                    ║")
        print("║  3. Executar BFS                         ║")
        print("║  4. Executar DFS                         ║")
        print("║  5. Executar Dijkstra                    ║")
        print("║  6. Simular falha na rede                ║")
        print("║  7. Sair                                 ║")
        print("╚══════════════════════════════════════════╝")

        opcao = input("\nEscolha uma opção: ")

        match opcao:
            case "1":
                # Gera o mapa visual da colônia e abre na tela
                mapa_colonia(colonia, matriz_conexoes)
                plt.show()
                print("Mapa gerado! Verifique o arquivo Mapa_Colonia.png")

            case "2":
                # Lista todos os módulos da colônia com suas informações principais
                print("\n📋 Módulos da colônia:")
                for modulo in colonia.modulos:
                    print(f"  {modulo.id_nome} — {modulo.tipo} | Status: {modulo.status} | Prioridade: {modulo.prioridade}")

            case "3":
                # Executa o BFS a partir de um módulo de origem
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem para o BFS:")
                bfs(colonia, origem)

            case "4":
                # Executa o DFS a partir de um módulo de origem
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem para o DFS:")
                dfs(colonia, origem)

            case "5":
                # Executa o Dijkstra entre dois módulos para encontrar o caminho mais eficiente
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem:")
                destino = selecionar_modulo(colonia, "Selecione o módulo de destino:")
                dijkstra(colonia, origem, destino)

            case "6":
                # Abre o submenu de simulação de falha na rede
                simular_falha_na_rede(colonia)

            case "7":
                # Encerra o sistema
                print("\nEncerrando o SIGIC. Até logo!")
                break

            case _:
                # Opção inválida
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()