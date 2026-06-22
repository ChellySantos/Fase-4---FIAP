from modules.mapa import matriz_conexoes, mapa_colonia
from algorithms.algoritmos import bfs, dfs, dijkstra, conexoes_criticas
from sistema import inicializar_colonia
import matplotlib.pyplot as plt


def selecionar_modulo(colonia, mensagem, excluir=[]):
    # Exibe a mensagem recebida como instrução para o usuário
    print(f"\n{mensagem}")

    # Monta a lista de módulos que podem ser escolhidos, removendo os que estão na lista de exclusão
    # (usado, por exemplo, para não deixar escolher de novo um módulo já desativado)
    modulos_disponiveis = [m for m in colonia.modulos if m.id_nome not in excluir]

    # Numera e exibe cada módulo disponível, junto com seu tipo
    for i, modulo in enumerate(modulos_disponiveis):
        print(f"  {i + 1}. {modulo.id_nome} — {modulo.tipo}")

    # Fica pedindo uma escolha até o usuário digitar um número válido dentro da lista
    while True:
        escolha = input("Escolha o número do módulo: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(modulos_disponiveis):
            return modulos_disponiveis[int(escolha) - 1].id_nome  # Retorna o id_nome do módulo escolhido
        print("Opção inválida. Tente novamente.")

"""
Essa função exibe uma lista numerada de módulos disponíveis (podendo excluir alguns, como módulos offline)
e fica aguardando o usuário digitar uma escolha válida. Ela é reutilizada por várias outras funções do menu
sempre que é necessário perguntar "qual módulo você quer usar?", evitando repetir esse código várias vezes.
"""


def simular_falha_na_rede(colonia):
    # Exibe o submenu com as opções de simulação de falha
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
            # Pede ao usuário os dois módulos cuja conexão será testada
            origem = selecionar_modulo(colonia, "Selecione o módulo de origem da conexão:")
            destino = selecionar_modulo(colonia, "Selecione o módulo de destino da conexão:")
            indices = {m.id_nome: i for i, m in enumerate(colonia.modulos)}  # Mapeia nome -> índice na matriz

            if origem in indices and destino in indices:
                i, j = indices[origem], indices[destino]

                # Verifica se a conexão realmente existe antes de tentar removê-la
                if matriz_conexoes[i][j] == 0:
                    print(f"\n❌ Não existe conexão entre {origem} e {destino}.")
                else:
                    # Remove a conexão dos dois lados da matriz (grafo não-direcionado)
                    matriz_conexoes[i][j] = 0
                    matriz_conexoes[j][i] = 0
                    print(f"\n🔌 Conexão {origem} ↔ {destino} removida temporariamente.")

                    # Roda o BFS a partir da origem para ver quais módulos ainda são alcançáveis sem essa conexão
                    visitados_sim = bfs(colonia, origem)

                    # Compara a lista de todos os módulos com os que o BFS conseguiu visitar
                    todos = [m.id_nome for m in colonia.modulos]
                    isolados = [m for m in todos if m not in visitados_sim]

                    if isolados:
                        # Se sobrou algum módulo de fora, significa que ele ficou sem rota até a origem
                        print(f"\n⚠️  ALERTA: Os seguintes módulos ficaram ISOLADOS da rede:")
                        for m in isolados:
                            print(f"  ❌ {m}")
                        print(f"\n🚨 Essa é uma conexão CRÍTICA para a infraestrutura!")
                    else:
                        # Se todo mundo continua acessível, a conexão removida não era essencial
                        print(f"\n✅ Rede ainda conectada — todos os módulos permanecem acessíveis.")
                        print(f"   A conexão {origem} ↔ {destino} NÃO é crítica.")

                        # Mostra qual seria o caminho alternativo usado no lugar da conexão removida
                        print(f"\n🔁 Caminho alternativo entre {origem} e {destino}:")
                        dijkstra(colonia, origem, destino)

                    # Restaura a conexão original nos dois sentidos, voltando a matriz ao estado normal
                    matriz_conexoes[i][j] = 1
                    matriz_conexoes[j][i] = 1
                    print(f"\n🔧 Conexão {origem} ↔ {destino} restaurada.")
            else:
                print("Módulo não encontrado.")

        case "2":
            # Pergunta quantos módulos o usuário quer desativar de uma vez
            print("\nQuantos módulos deseja desativar?")
            qtd = input("Quantidade: ")

            if not qtd.isdigit() or int(qtd) < 1:
                print("Quantidade inválida.")
            else:
                qtd = int(qtd)
                modulos_offline = []  # Guarda os nomes dos módulos que serão desativados
                conexoes_salvas = {}  # Guarda as conexões removidas de cada módulo, para poder restaurar depois
                indices = {m.id_nome: i for i, m in enumerate(colonia.modulos)}
                n = len(colonia.modulos)

                # Pede um a um os módulos que serão desativados, sem deixar escolher o mesmo duas vezes
                for k in range(qtd):
                    modulo_id = selecionar_modulo(colonia, f"Selecione o módulo {k + 1} para desativar:", excluir=modulos_offline)
                    if modulo_id not in modulos_offline:
                        modulos_offline.append(modulo_id)

                # Para cada módulo offline, remove todas as conexões dele na matriz e guarda quais eram, pra restaurar depois
                for modulo_id in modulos_offline:
                    idx = indices[modulo_id]
                    conexoes_salvas[modulo_id] = []
                    for j in range(n):
                        if matriz_conexoes[idx][j] == 1:
                            conexoes_salvas[modulo_id].append(j)  # Salva o índice do vizinho antes de remover
                            matriz_conexoes[idx][j] = 0  # Remove a conexão do módulo offline
                            matriz_conexoes[j][idx] = 0  # Remove também o sentido inverso
                    print(f"⛔ Módulo {modulo_id} desativado.")

                # Escolhe a partir de qual módulo ainda ativo vai testar a conectividade da rede
                origem_teste = selecionar_modulo(colonia, "Selecione o módulo de origem para testar conectividade:", excluir=modulos_offline)

                # Roda o BFS para ver quais módulos restantes ainda são alcançáveis com os módulos offline
                visitados_sim = bfs(colonia, origem_teste)

                # Compara os módulos que deveriam estar ativos com os que o BFS realmente alcançou
                modulos_restantes = [m.id_nome for m in colonia.modulos if m.id_nome not in modulos_offline]
                isolados = [m for m in modulos_restantes if m not in visitados_sim]

                if isolados:
                    print(f"\n⚠️  ALERTA: Os seguintes módulos ficaram ISOLADOS:")
                    for m in isolados:
                        print(f"  ❌ {m}")
                    print(f"\n🚨 A combinação de módulos offline é CRÍTICA para a infraestrutura!")
                else:
                    print(f"\n✅ Rede ainda conectada — todos os módulos permanecem acessíveis.")

                # Restaura todas as conexões que foram salvas, devolvendo a matriz ao estado original
                for modulo_id in modulos_offline:
                    idx = indices[modulo_id]
                    for j in conexoes_salvas[modulo_id]:
                        matriz_conexoes[idx][j] = 1
                        matriz_conexoes[j][idx] = 1
                    print(f"🔧 Módulo {modulo_id} restaurado.")

        case "0":
            # Volta para o menu principal sem fazer nada
            pass

        case _:
            print("Opção inválida.")

"""
Essa função simula falhas na infraestrutura da colônia de duas formas: removendo uma única conexão
entre dois módulos, ou desativando vários módulos de uma vez. Em ambos os casos, ela usa o BFS para
verificar se a rede continua conectada após a falha, identificando quais módulos ficariam isolados.
No final, a matriz de conexões é sempre restaurada ao estado original, já que essa é apenas uma simulação.
"""


def analisar_eficiencia(colonia):
    # Pede os módulos de origem e destino que serão usados na comparação dos algoritmos
    origem = selecionar_modulo(colonia, "Selecione o módulo de origem para análise:")
    destino = selecionar_modulo(colonia, "Selecione o módulo de destino para análise:")

    print(f"\n📊 Análise de Eficiência — {origem} até {destino}")
    print("=" * 50)

    # Roda o BFS e mostra quantos módulos ele visitou (deve ser sempre a rede toda, já que ele explora tudo)
    print("\n🔵 BFS (Busca em Largura):")
    ordem_bfs = bfs(colonia, origem)
    print(f"   Módulos visitados: {len(ordem_bfs)}")
    print(f"   Complexidade: O(V + E)")

    # Roda o DFS e mostra quantos módulos ele visitou (também explora a rede toda, só muda a ordem)
    print("\n🟢 DFS (Busca em Profundidade):")
    ordem_dfs = dfs(colonia, origem)
    print(f"   Módulos visitados: {len(ordem_dfs)}")
    print(f"   Complexidade: O(V + E)")

    # Roda o Dijkstra e mostra o tamanho e o custo do caminho mais eficiente encontrado
    print("\n🛰️ Dijkstra (Caminho Mínimo):")
    resultado = dijkstra(colonia, origem, destino)
    if resultado:
        caminho, custo = resultado
        print(f"   Módulos no caminho: {len(caminho)}")
        print(f"   Custo total: {custo:.2f}")
        print(f"   Complexidade: O(V²)")

    # Mostra uma conclusão comparando o tamanho da exploração de BFS/DFS com a eficiência do Dijkstra
    print("\n" + "=" * 50)
    print("💡 Conclusão:")
    print(f"   BFS e DFS exploram TODA a rede ({len(ordem_bfs)} módulos)")
    if resultado:
        print(f"   Dijkstra encontrou o caminho MAIS EFICIENTE com apenas {len(caminho)} módulos e custo {custo:.2f}")

"""
Essa função compara, lado a lado, o comportamento de BFS, DFS e Dijkstra para o mesmo par de módulos.
A ideia é mostrar na prática a diferença entre algoritmos de exploração total da rede (BFS e DFS, que
visitam todos os módulos alcançáveis) e um algoritmo de caminho mínimo (Dijkstra, que busca apenas a
rota mais eficiente entre dois pontos específicos), reforçando por que cada um serve para um propósito diferente.
"""


def menu():
    # Cria a colônia com seus 8 módulos já inicializados, antes de abrir o menu
    colonia = inicializar_colonia()

    while True:
        # Exibe o menu principal do sistema com todas as funcionalidades disponíveis
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
        print("║  7. Análise de eficiência                ║")
        print("║  8. Identificar conexões críticas        ║")
        print("║  9. Sair                                 ║")
        print("╚══════════════════════════════════════════╝")

        opcao = input("\nEscolha uma opção: ")

        match opcao:
            case "1":
                # Gera o mapa visual da colônia (módulos + conexões) e salva como imagem
                mapa_colonia(colonia, matriz_conexoes)
                plt.show()
                print("Mapa gerado! Verifique o arquivo Mapa_Colonia.png")

            case "2":
                # Lista todos os módulos da colônia com suas informações principais
                print("\n📋 Módulos da colônia:")
                for modulo in colonia.modulos:
                    print(f"  {modulo.id_nome} — {modulo.tipo} | Status: {modulo.status} | Prioridade: {modulo.prioridade}")

            case "3":
                # Pede o módulo de origem e executa o BFS a partir dele
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem para o BFS:")
                bfs(colonia, origem)

            case "4":
                # Pede o módulo de origem e executa o DFS a partir dele
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem para o DFS:")
                dfs(colonia, origem)

            case "5":
                # Pede origem e destino e executa o Dijkstra para achar o caminho mais eficiente entre eles
                origem = selecionar_modulo(colonia, "Selecione o módulo de origem:")
                destino = selecionar_modulo(colonia, "Selecione o módulo de destino:")
                dijkstra(colonia, origem, destino)

            case "6":
                # Abre o submenu de simulação de falhas na rede (conexão única ou módulos offline)
                simular_falha_na_rede(colonia)

            case "7":
                # Executa a análise comparativa de eficiência entre BFS, DFS e Dijkstra
                analisar_eficiencia(colonia)

            case "8":
                # Identifica automaticamente todas as conexões críticas da rede,
                # ou seja, conexões cuja remoção isolaria algum módulo da colônia
                print("\n🔎 Analisando conexões críticas da rede...")
                conexoes_criticas(colonia)

            case "9":
                # Encerra o programa, saindo do loop principal
                print("\nEncerrando o SIGIC. Até logo!")
                break

            case _:
                # Trata qualquer entrada que não corresponda a nenhuma opção válida
                print("Opção inválida. Tente novamente.")

"""
Essa é a função principal do sistema SIGIC. Ela inicializa a colônia e mantém um loop contínuo exibindo
o menu de navegação no terminal, lendo a opção escolhida pelo usuário e chamando a função correspondente
a cada funcionalidade (visualização da rede, algoritmos de busca, simulações e análises). O loop só é
interrompido quando o usuário escolhe a opção de sair (9).
"""


if __name__ == "__main__":
    menu()