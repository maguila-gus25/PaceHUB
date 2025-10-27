from typing import Dict, List, Any, Optional
from entidade.resultado import Resultado, separar_resultados_por_genero, separar_resultados_por_categoria
from persistencia.resultado_dao import ResultadoDAO


class ControladorRanking:
    """
    Controlador responsável pela organização de dados para visualização de rankings.
    Organiza resultados por categoria e gênero para exibição nas interfaces.
    """
    
    def __init__(self):
        """
        Inicializa o controlador com instância do DAO.
        """
        self.dao = ResultadoDAO()
    
    def obter_rankings_evento(self, evento_id: int) -> Dict[str, Any]:
        """
        Obtém todos os rankings de um evento organizados por categoria e gênero.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Dicionário com rankings organizados
        """
        # Buscar resultados do evento
        resultados = self.dao.buscar_resultados_por_evento(evento_id)
        
        if not resultados:
            return self._estrutura_vazia()
        
        # Organizar por categoria e gênero
        rankings = self._organizar_rankings(resultados)
        
        # Adicionar estatísticas
        rankings['estatisticas'] = self._calcular_estatisticas(resultados)
        
        return rankings
    
    def _estrutura_vazia(self) -> Dict[str, Any]:
        """
        Retorna estrutura vazia de rankings.
        
        Returns:
            Dicionário com estrutura vazia
        """
        return {
            'geral_masculino': [],
            'geral_feminino': [],
            'junior_masculino': [],
            'junior_feminino': [],
            'adulto_masculino': [],
            'adulto_feminino': [],
            'master_masculino': [],
            'master_feminino': [],
            'pcd_masculino': [],
            'pcd_feminino': [],
            'estatisticas': {
                'total_resultados': 0,
                'por_genero': {'Masculino': 0, 'Feminino': 0},
                'por_categoria': {},
                'tem_categoria_pcd': False
            }
        }
    
    def _organizar_rankings(self, resultados: List[Resultado]) -> Dict[str, List[Resultado]]:
        """
        Organiza resultados em rankings por categoria e gênero.
        
        Args:
            resultados: Lista de resultados
            
        Returns:
            Dicionário com rankings organizados
        """
        rankings = {
            'geral_masculino': [],
            'geral_feminino': [],
            'junior_masculino': [],
            'junior_feminino': [],
            'adulto_masculino': [],
            'adulto_feminino': [],
            'master_masculino': [],
            'master_feminino': [],
            'pcd_masculino': [],
            'pcd_feminino': []
        }
        
        # Separar por gênero primeiro
        masculino, feminino = separar_resultados_por_genero(resultados)
        
        # Processar masculino
        self._processar_genero(masculino, rankings, 'masculino')
        
        # Processar feminino
        self._processar_genero(feminino, rankings, 'feminino')
        
        return rankings
    
    def _processar_genero(self, resultados: List[Resultado], rankings: Dict[str, List[Resultado]], genero: str):
        """
        Processa resultados de um gênero específico.
        
        Args:
            resultados: Lista de resultados do gênero
            rankings: Dicionário de rankings para atualizar
            genero: Gênero ('masculino' ou 'feminino')
        """
        # Classificação geral (top 5)
        geral_key = f'geral_{genero}'
        rankings[geral_key] = [r for r in resultados if r.tem_classificacao_geral()]
        
        # Separar por categoria
        categorias = separar_resultados_por_categoria(resultados)
        
        for categoria, resultados_categoria in categorias.items():
            categoria_key = f'{categoria.lower()}_{genero}'
            if categoria_key in rankings:
                rankings[categoria_key] = resultados_categoria
    
    def _calcular_estatisticas(self, resultados: List[Resultado]) -> Dict[str, Any]:
        """
        Calcula estatísticas dos resultados.
        
        Args:
            resultados: Lista de resultados
            
        Returns:
            Dicionário com estatísticas
        """
        # Contar por gênero
        masculino, feminino = separar_resultados_por_genero(resultados)
        por_genero = {
            'Masculino': len(masculino),
            'Feminino': len(feminino)
        }
        
        # Contar por categoria
        categorias = separar_resultados_por_categoria(resultados)
        por_categoria = {categoria: len(resultados_cat) for categoria, resultados_cat in categorias.items()}
        
        # Verificar se tem categoria PCD
        tem_categoria_pcd = 'PCD' in categorias
        
        return {
            'total_resultados': len(resultados),
            'por_genero': por_genero,
            'por_categoria': por_categoria,
            'tem_categoria_pcd': tem_categoria_pcd
        }
    
    def obter_ranking_geral(self, evento_id: int) -> Dict[str, List[Resultado]]:
        """
        Obtém apenas a classificação geral (top 5 de cada gênero).
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Dicionário com classificação geral
        """
        rankings = self.obter_rankings_evento(evento_id)
        
        return {
            'masculino': rankings['geral_masculino'],
            'feminino': rankings['geral_feminino']
        }
    
    def obter_ranking_categoria(self, evento_id: int, categoria: str) -> Dict[str, List[Resultado]]:
        """
        Obtém ranking de uma categoria específica.
        
        Args:
            evento_id: ID do evento
            categoria: Categoria ('Júnior', 'Adulto', 'Master', 'PCD')
            
        Returns:
            Dicionário com ranking da categoria por gênero
        """
        rankings = self.obter_rankings_evento(evento_id)
        
        categoria_key = categoria.lower()
        
        return {
            'masculino': rankings.get(f'{categoria_key}_masculino', []),
            'feminino': rankings.get(f'{categoria_key}_feminino', [])
        }
    
    def obter_resultado_atleta(self, evento_id: int, cpf_atleta: str) -> Optional[Dict[str, Any]]:
        """
        Obtém resultado específico de um atleta.
        
        Args:
            evento_id: ID do evento
            cpf_atleta: CPF do atleta
            
        Returns:
            Dicionário com informações do resultado ou None
        """
        resultado = self.dao.buscar_resultado_por_cpf(cpf_atleta, evento_id)
        
        if not resultado:
            return None
        
        return {
            'resultado': resultado,
            'posicao_geral': resultado.classificacao_geral,
            'posicao_categoria': resultado.classificacao_categoria,
            'tem_classificacao_geral': resultado.tem_classificacao_geral(),
            'tem_classificacao_categoria': resultado.tem_classificacao_categoria()
        }
    
    def obter_estatisticas_evento(self, evento_id: int) -> Dict[str, Any]:
        """
        Obtém estatísticas detalhadas de um evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Dicionário com estatísticas
        """
        return self.dao.obter_estatisticas_evento(evento_id)
    
    def verificar_evento_tem_resultados(self, evento_id: int) -> bool:
        """
        Verifica se um evento possui resultados importados.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            True se tem resultados, False caso contrário
        """
        count = self.dao.contar_resultados_evento(evento_id)
        return count > 0
    
    def obter_categorias_disponiveis(self, evento_id: int) -> List[str]:
        """
        Obtém lista de categorias que possuem resultados no evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Lista de categorias disponíveis
        """
        rankings = self.obter_rankings_evento(evento_id)
        estatisticas = rankings['estatisticas']
        
        categorias_disponiveis = []
        for categoria, count in estatisticas['por_categoria'].items():
            if count > 0:
                categorias_disponiveis.append(categoria)
        
        return categorias_disponiveis
    
    def formatar_ranking_para_tabela(self, resultados: List[Resultado], incluir_categoria: bool = False) -> List[List[str]]:
        """
        Formata uma lista de resultados para exibição em tabela.
        
        Args:
            resultados: Lista de resultados
            incluir_categoria: Se deve incluir coluna de categoria
            
        Returns:
            Lista de linhas formatadas para tabela
        """
        linhas = []
        
        for i, resultado in enumerate(resultados, 1):
            linha = [str(i), resultado.nome_atleta, resultado.tempo_final]
            
            if incluir_categoria:
                linha.append(resultado.categoria)
            
            linhas.append(linha)
        
        return linhas
    
    def obter_cabecalhos_tabela(self, incluir_categoria: bool = False) -> List[str]:
        """
        Obtém cabeçalhos para tabelas de ranking.
        
        Args:
            incluir_categoria: Se deve incluir cabeçalho de categoria
            
        Returns:
            Lista de cabeçalhos
        """
        cabecalhos = ['Pos.', 'Nome do Atleta', 'Tempo']
        
        if incluir_categoria:
            cabecalhos.append('Categoria')
        
        return cabecalhos
    
    def obter_resumo_rankings(self, evento_id: int) -> Dict[str, Any]:
        """
        Obtém resumo dos rankings de um evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Dicionário com resumo
        """
        rankings = self.obter_rankings_evento(evento_id)
        estatisticas = rankings['estatisticas']
        
        # Contar categorias com resultados
        categorias_com_resultados = len([cat for cat, count in estatisticas['por_categoria'].items() if count > 0])
        
        return {
            'total_atletas': estatisticas['total_resultados'],
            'categorias_disponiveis': categorias_com_resultados,
            'tem_categoria_pcd': estatisticas['tem_categoria_pcd'],
            'distribuicao_genero': estatisticas['por_genero'],
            'distribuicao_categoria': estatisticas['por_categoria']
        }


if __name__ == "__main__":
    # Teste do controlador
    print("=== Teste do ControladorRanking ===")
    
    controlador = ControladorRanking()
    
    # Teste de estrutura vazia
    print("Teste de estrutura vazia:")
    estrutura_vazia = controlador._estrutura_vazia()
    print(f"  Total de categorias: {len(estrutura_vazia) - 1}")  # -1 para estatísticas
    print(f"  Tem categoria PCD: {estrutura_vazia['estatisticas']['tem_categoria_pcd']}")
    
    # Teste de formatação para tabela
    print("\nTeste de formatação para tabela:")
    from entidade.resultado import Resultado
    
    resultados_teste = [
        Resultado("11111111111", "Atleta A", "Masculino", "01:30:00", "Adulto"),
        Resultado("11111111112", "Atleta B", "Masculino", "01:25:00", "Adulto"),
    ]
    
    # Definir classificações
    resultados_teste[0].definir_classificacao_categoria(1)
    resultados_teste[1].definir_classificacao_categoria(2)
    
    linhas_tabela = controlador.formatar_ranking_para_tabela(resultados_teste, incluir_categoria=True)
    cabecalhos = controlador.obter_cabecalhos_tabela(incluir_categoria=True)
    
    print(f"  Cabeçalhos: {cabecalhos}")
    print("  Linhas:")
    for linha in linhas_tabela:
        print(f"    {linha}")
    
    # Teste de estatísticas
    print("\nTeste de cálculo de estatísticas:")
    estatisticas = controlador._calcular_estatisticas(resultados_teste)
    print(f"  Estatísticas: {estatisticas}")
    
    print("\nTeste do controlador concluído!")
