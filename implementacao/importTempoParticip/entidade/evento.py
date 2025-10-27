from typing import List, Optional

class Evento:
    """
    Classe que representa um evento de corrida no sistema PaceHub.
    Contém informações básicas do evento e métodos auxiliares.
    """
    
    def __init__(self, id: int, nome: str, data: str, status: str, distancia: str):
        """
        Inicializa um evento.
        
        Args:
            id: ID único do evento
            nome: Nome do evento
            data: Data do evento no formato DD/MM/YYYY
            status: Status do evento ('Planejado', 'Inscrições Abertas', 'Concluído')
            distancia: Distância da corrida ('5km', '10km', '21km', '42km')
        """
        self.id = id
        self.nome = nome
        self.data = data  # DD/MM/YYYY
        self.status = status
        self.distancia = distancia
    
    def pode_importar_resultados(self) -> bool:
        """
        Verifica se o evento permite importação de resultados.
        Apenas eventos 'Concluído' permitem importação.
        
        Returns:
            True se pode importar resultados, False caso contrário
        """
        return self.status == 'Concluído'
    
    def pode_visualizar_resultados(self) -> bool:
        """
        Verifica se o evento permite visualização de resultados.
        Eventos 'Concluído' sempre permitem, outros dependem de ter resultados.
        
        Returns:
            True se pode visualizar resultados, False caso contrário
        """
        return self.status in ['Concluído', 'Inscrições Abertas']
    
    def obter_ano_evento(self) -> int:
        """
        Extrai o ano do evento.
        
        Returns:
            Ano do evento
        """
        try:
            return int(self.data.split('/')[2])
        except (ValueError, IndexError):
            raise ValueError(f"Formato de data inválido: {self.data}")
    
    def obter_data_formatada(self) -> str:
        """
        Retorna a data formatada para exibição.
        
        Returns:
            Data no formato DD/MM/YYYY
        """
        return self.data
    
    def obter_distancia_numerica(self) -> int:
        """
        Extrai a distância numérica em km.
        
        Returns:
            Distância em quilômetros
        """
        try:
            return int(self.distancia.replace('km', ''))
        except ValueError:
            raise ValueError(f"Formato de distância inválido: {self.distancia}")
    
    def to_dict(self) -> dict:
        """
        Converte o evento para dicionário.
        Útil para operações de banco de dados.
        
        Returns:
            Dicionário com os dados do evento
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'data': self.data,
            'status': self.status,
            'distancia': self.distancia
        }
    
    @classmethod
    def from_dict(cls, dados: dict) -> 'Evento':
        """
        Cria um evento a partir de um dicionário.
        Útil para operações de banco de dados.
        
        Args:
            dados: Dicionário com os dados do evento
            
        Returns:
            Objeto Evento
        """
        return cls(
            id=dados['id'],
            nome=dados['nome'],
            data=dados['data'],
            status=dados['status'],
            distancia=dados['distancia']
        )
    
    def __str__(self):
        return f"{self.nome} - {self.data} ({self.distancia}) - {self.status}"
    
    def __repr__(self):
        return f"Evento(id={self.id}, nome='{self.nome}', data='{self.data}', status='{self.status}')"
    
    def __eq__(self, other):
        """
        Comparação de igualdade por ID.
        """
        if not isinstance(other, Evento):
            return NotImplemented
        return self.id == other.id


# Mockdata: 4 eventos para testes
EVENTOS_MOCK = [
    Evento(1, "Meia Maratona de Inverno", "10/08/2025", "Concluído", "21km"),
    Evento(2, "Corrida Solidária", "30/09/2025", "Inscrições Abertas", "10km"),
    Evento(3, "Maratona de Floripa", "25/10/2025", "Concluído", "42km"),
    Evento(4, "Night Run Halloween", "31/10/2025", "Concluído", "5km"),
]


def obter_evento_por_id(evento_id: int) -> Optional[Evento]:
    """
    Busca um evento no mockdata pelo ID.
    
    Args:
        evento_id: ID do evento
        
    Returns:
        Objeto Evento se encontrado, None caso contrário
    """
    for evento in EVENTOS_MOCK:
        if evento.id == evento_id:
            return evento
    
    return None


def obter_eventos_por_status(status: str) -> List[Evento]:
    """
    Lista eventos por status.
    
    Args:
        status: Status dos eventos ('Planejado', 'Inscrições Abertas', 'Concluído')
        
    Returns:
        Lista de eventos com o status especificado
    """
    return [evento for evento in EVENTOS_MOCK if evento.status == status]


def obter_eventos_concluidos() -> List[Evento]:
    """
    Lista todos os eventos concluídos.
    
    Returns:
        Lista de eventos concluídos
    """
    return obter_eventos_por_status('Concluído')


def obter_eventos_para_importacao() -> List[Evento]:
    """
    Lista eventos que permitem importação de resultados.
    
    Returns:
        Lista de eventos concluídos
    """
    return [evento for evento in EVENTOS_MOCK if evento.pode_importar_resultados()]


def obter_eventos_para_visualizacao() -> List[Evento]:
    """
    Lista eventos que permitem visualização de resultados.
    
    Returns:
        Lista de eventos que permitem visualização
    """
    return [evento for evento in EVENTOS_MOCK if evento.pode_visualizar_resultados()]


def contar_eventos_por_status() -> dict:
    """
    Conta eventos por status.
    
    Returns:
        Dicionário com contadores por status
    """
    contadores = {}
    
    for evento in EVENTOS_MOCK:
        status = evento.status
        contadores[status] = contadores.get(status, 0) + 1
    
    return contadores


def listar_eventos_por_distancia(distancia: str) -> List[Evento]:
    """
    Lista eventos por distância.
    
    Args:
        distancia: Distância da corrida ('5km', '10km', '21km', '42km')
        
    Returns:
        Lista de eventos com a distância especificada
    """
    return [evento for evento in EVENTOS_MOCK if evento.distancia == distancia]


if __name__ == "__main__":
    # Teste da classe Evento
    print("=== Teste da Classe Evento ===")
    
    # Teste de busca por ID
    evento = obter_evento_por_id(1)
    if evento:
        print(f"Evento encontrado: {evento}")
        print(f"Pode importar resultados: {evento.pode_importar_resultados()}")
        print(f"Ano do evento: {evento.obter_ano_evento()}")
        print(f"Distância numérica: {evento.obter_distancia_numerica()} km")
    
    # Teste de contagem por status
    contadores = contar_eventos_por_status()
    print(f"\nContadores por status: {contadores}")
    
    # Teste de listagem
    concluidos = obter_eventos_concluidos()
    print(f"\nEventos concluídos: {len(concluidos)}")
    for evento in concluidos:
        print(f"  - {evento}")
    
    # Teste de eventos para importação
    para_importacao = obter_eventos_para_importacao()
    print(f"\nEventos para importação: {len(para_importacao)}")
    
    # Teste de conversão para dicionário
    if evento:
        dados = evento.to_dict()
        print(f"\nDados do evento: {dados}")
        
        evento_recriado = Evento.from_dict(dados)
        print(f"Evento recriado: {evento_recriado}")
