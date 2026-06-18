from modules.modulos import *
from modules.mapa import *

def main():
    #Inicia a colônia
    colonia = Colonia()

    #Adição dos módulos
    mod_habitacao = Modulo("HAB-01", "Habitação", "Acomodação da tripulação e suporte básico à sobrevivência humana", 1, 120, 40, 6.5, "ativo", (9, 5))
    mod_controle = Modulo("CTR-01", "Centro de Controle", "Monitoramento e gerenciamento das operações da colônia", 2, 100, 100, 8.0, "ativo", (5, 6))
    mod_energia = Modulo("ENE-01", "Armazenamento de Energia", "Armazenamento de energia produzida pelos sistemas da base", 3, 50, 500, 9.0, "ativo", (2, 8))
    mod_agricultura = Modulo("AGR-01", "Agricultura", "Produção de alimentos e suporte à sustentabilidade da colônia", 5, 130, 20, 5.0, "ativo", (8, 8))
    mod_laboratorio = Modulo("LAB-01", "Laboratório Científico", "Pesquisas e análises de materiais e condições marcianas", 4, 100, 25, 6.0, "ativo", (2, 2))
    mod_comunicacao = Modulo("COM-01", "Comunicação", "Troca de dados entre módulos e comunicação com a Terra", 3, 60, 20, 9.5, "ativo", (5, 3))
    mod_medico = Modulo("MED-01", "Suporte Médico", "Atendimento médico e monitoramento da saúde da tripulação", 4, 60, 50, 8.5, "ativo", (8, 2))
    mod_oxigenio = Modulo("OXI-01", "Produção de Oxigênio", "Geração e distribuição de oxigênio para a base", 2, 180, 50, 7.0, "ativo", (1, 5))
    
    #Adição dos módulos dentro da colônia
    colonia.adicionar_modulo(mod_habitacao)
    colonia.adicionar_modulo(mod_controle)
    colonia.adicionar_modulo(mod_energia)
    colonia.adicionar_modulo(mod_agricultura)
    colonia.adicionar_modulo(mod_laboratorio)
    colonia.adicionar_modulo(mod_comunicacao)
    colonia.adicionar_modulo(mod_medico)
    colonia.adicionar_modulo(mod_oxigenio)

    #Obtém as listas de módulos de acordo com seu respectivo status/prioridade
    modulos_ativo = colonia.modulos_ativo()
    modulos_manutencao = colonia.modulos_manutencao()
    modulos_alerta = colonia.modulos_alerta()
    modulos_inativo = colonia.modulos_inativo()
    modulos_alta_prioridade = colonia.modulos_alta_prioridade()
    modulos_baixa_prioridade = colonia.modulos_baixa_prioridade()
    #Obtém uma lista das coordenadas dos módulos
    modulos_coordenadas = colonia.modulos_coordenadas()
    
    #Obtém o dicionário de módulos (id_nome -> módulo) direto da colônia
    mapa_modulos = colonia.mapa_modulos()  

    #Gera o mapa visual da colônia já com as conexões entre os módulos
    mapa_colonia(colonia, matriz_conexoes)  

    #Obtém o módulo de origem e destino da conexão
    modulo_origem = input("Origem: ")
    modulo_destino = input("Destino: ")

    #Busca os módulos correspondentes dentro do dicionário
    modulo_origem = mapa_modulos[modulo_origem]
    modulo_destino = mapa_modulos[modulo_destino]
    
    #Calcula o peso da conexão entre origem e destino 
    peso, distancia_m, tempo_comunicacao, consumo_comunicacao = calcular_peso(modulo_origem, modulo_destino, detalhado=True)

    print(f"Distância real: {distancia_m:.2f} m")
    print(f"Tempo de comunicação: {tempo_comunicacao:.2f} s")
    print(f"Consumo energético: {consumo_comunicacao:.2f} W")
    print(f"Peso da conexão: {peso:.0f}")

if __name__ == "__main__":
    main()