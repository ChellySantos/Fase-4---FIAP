class Modulo:
    def __init__(
        self,
        id_nome: str,
        tipo: str,
        funcao: str,
        prioridade: int,
        consumo: int,
        capacidade_armazenamento: int,
        comunicacao: float,
        status: str,
        coordenada: tuple,
    ):
        """
        id_nome = identificador (id) do módulo
        tipo = categoria do módulo
        funcao = função do módulo
        prioridade = nível de importância do módulo para a sobrevivência da colônia
        consumo = quantidade de energia necessária para o funcionamento do módulo
        capacidade_armazenamento: quantidade de recursos ou energia que o módulo consegue armazenar
        comunicacao: frequência de troca de informações entre módulos
        status: situação atual do módulo (ativo, manutenção, alerta, inativo)
        coordenadas: será utilizada para calcular rotas e eficiência de distribuição
        """
        self.id_nome = id_nome
        self.tipo = tipo
        self.funcao = funcao
        self.prioridade = prioridade # Varia de 1 (mais importante) a 5 (menos importante)
        self.consumo = consumo #Medido em watts 
        self.capacidade_armazenamento = capacidade_armazenamento #Medido em kW
        self.comunicacao = comunicacao #Medido em segundos
        self.status = status #Ativo, manutencao, alerta ou inativo
        self.coordenada = coordenada #Coordenada dentro do mapa da colonia 

class Colonia:
    def __init__(self):
        self.modulos = []  #Será usada para armazenar todos os módulos que forem adicionados dentro da colônia
        self.dict_modulos = {}  #Será usada para armazenar todos os módulos que forem adicionados dentro da colônia em um dicionário

    def adicionar_modulo(self, modulo): #Adiciona módulos na colônia
        self.modulos.append(modulo)
        self.dict_modulos[modulo.id_nome] = modulo  #Adiciona o módulo também no dicionário, usando o id_nome como chave

    def mapa_modulos(self):  #Retorna o dicionário
        return self.dict_modulos
    
    def modulos_ativo(self): #Retorna os módulos que estão ativos 
        return [m for m in self.modulos if m.status == "ativo"]
    
    def modulos_manutencao(self): #Retorna os módulos que estão em manutenção 
        return [m for m in self.modulos if m.status == "manutencao"]
    
    def modulos_alerta(self): #Retorna os módulos que estão em alerta 
        return [m for m in self.modulos if m.status == "alerta"]
    
    def modulos_inativo(self): #Retorna os módulos que estão inativos 
        return [m for m in self.modulos if m.status == "inativo"]
    
    def modulos_alta_prioridade(self): #Retorna os módulos que tem prioridade menor ou igual a 2
        return [m for m in self.modulos if m.prioridade <= 2]
    
    def modulos_baixa_prioridade(self): #Retorna os módulos que tem prioridade maior que 2
        return [m for m in self.modulos if m.prioridade > 2]
    
    def modulos_coordenadas(self): #Retorna um conjunto das coordenadas de cada módulo
        conj_coordenadas = [m.coordenada for m in self.modulos]
        return conj_coordenadas