from modules.modulos import *
from modules.mapa import *


def inicializar_colonia():
    # Inicia a colônia
    colonia = Colonia()

    # Adição dos módulos
    colonia.adicionar_modulo(Modulo("HAB-01", "Habitação", "Acomodação da tripulação e suporte básico à sobrevivência humana", 1, 120, 40, 6.5, "ativo", (9, 5)))
    colonia.adicionar_modulo(Modulo("CTR-01", "Centro de Controle", "Monitoramento e gerenciamento das operações da colônia", 2, 100, 100, 8.0, "ativo", (5, 6)))
    colonia.adicionar_modulo(Modulo("ENE-01", "Armazenamento de Energia", "Armazenamento de energia produzida pelos sistemas da base", 3, 50, 500, 9.0, "ativo", (2, 8)))
    colonia.adicionar_modulo(Modulo("AGR-01", "Agricultura", "Produção de alimentos e suporte à sustentabilidade da colônia", 5, 130, 20, 5.0, "ativo", (8, 8)))
    colonia.adicionar_modulo(Modulo("LAB-01", "Laboratório Científico", "Pesquisas e análises de materiais e condições marcianas", 4, 100, 25, 6.0, "ativo", (2, 2)))
    colonia.adicionar_modulo(Modulo("COM-01", "Comunicação", "Troca de dados entre módulos e comunicação com a Terra", 3, 60, 20, 9.5, "ativo", (5, 3)))
    colonia.adicionar_modulo(Modulo("MED-01", "Suporte Médico", "Atendimento médico e monitoramento da saúde da tripulação", 4, 60, 50, 8.5, "ativo", (8, 2)))
    colonia.adicionar_modulo(Modulo("OXI-01", "Produção de Oxigênio", "Geração e distribuição de oxigênio para a base", 2, 180, 50, 7.0, "ativo", (1, 5)))

    return colonia