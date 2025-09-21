class Evento:
    def __init__(self, nome: str, data: str, distancia: str, tempo_corte: str, data_limite_cancelamento: str, kit_corrida: str):
        self.nome = nome
        self.data = data
        self.distancia = distancia  # Em km
        self.tempo_corte = tempo_corte  # Em horas
        self.data_limite_cancelamento = data_limite_cancelamento
        self.kit_de_corrida = kit_corrida
        self.lista_de_inscritos = []  # Começa vazia

    def __str__(self):
        return (f"  - Nome do Evento: {self.nome}\n"
                f"  - Data: {self.data}\n"
                f"  - Distância: {self.distancia} km\n"
                f"  - Tempo de Corte: {self.tempo_corte} horas")