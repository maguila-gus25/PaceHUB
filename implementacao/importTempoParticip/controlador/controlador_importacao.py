import csv
import os
from typing import List, Tuple, Dict, Any
from entidade.atleta import obter_atleta_por_cpf, Atleta
from entidade.resultado import Resultado, criar_resultado_para_atleta, ordenar_resultados_por_tempo, separar_resultados_por_genero
from entidade.evento import obter_evento_por_id
from persistencia.resultado_dao import ResultadoDAO


class ControladorImportacao:
    """
    Controlador responsável pelo processamento de arquivos CSV e cálculo de rankings.
    Implementa as regras de negócio RN04, RN06 e RN07.
    """
    
    def __init__(self):
        """
        Inicializa o controlador com instância do DAO.
        """
        self.dao = ResultadoDAO()
    
    def processar_csv(self, caminho_arquivo: str, evento_id: int) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Processa um arquivo CSV de resultados e salva no banco.
        
        Args:
            caminho_arquivo: Caminho para o arquivo CSV
            evento_id: ID do evento
            
        Returns:
            Tupla (total_importados, lista_erros)
        """
        print(f"\n[CONTROLADOR] Processando CSV: {caminho_arquivo}")
        print(f"[CONTROLADOR] Evento ID: {evento_id}")
        
        # Validar arquivo
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        # Buscar evento
        evento = obter_evento_por_id(evento_id)
        if not evento:
            print(f"[CONTROLADOR] ERRO: Evento ID {evento_id} não encontrado no mockdata!")
            raise ValueError(f"Evento com ID {evento_id} não encontrado")
        
        print(f"[CONTROLADOR] Evento encontrado: {evento.nome}")
        
        if not evento.pode_importar_resultados():
            raise ValueError(f"Evento '{evento.nome}' não permite importação de resultados")
        
        # Ler e processar CSV
        resultados = []
        erros = []
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo)
                
                # Pular cabeçalho se existir
                primeira_linha = next(leitor, None)
                if primeira_linha and not self._eh_linha_dados(primeira_linha):
                    # É cabeçalho, continuar
                    pass
                else:
                    # Primeira linha é dados, processar
                    if primeira_linha:
                        resultado, erro = self._processar_linha(primeira_linha, evento.data)
                        if resultado:
                            resultados.append(resultado)
                        if erro:
                            erros.append(erro)
                
                # Processar demais linhas
                for num_linha, linha in enumerate(leitor, start=2):
                    resultado, erro = self._processar_linha(linha, evento.data)
                    if resultado:
                        resultados.append(resultado)
                    if erro:
                        erro['linha'] = num_linha
                        erros.append(erro)
        
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo CSV: {e}")
        
        print(f"[CONTROLADOR] Linhas processadas: {len(resultados)} válidas, {len(erros)} com erro")
        
        if not resultados:
            print("[CONTROLADOR] ERRO: Nenhum resultado válido encontrado!")
            raise ValueError("Nenhum resultado válido encontrado no arquivo")
        
        # Calcular rankings
        print(f"[CONTROLADOR] Calculando rankings...")
        resultados_com_rankings = self.calcular_rankings(resultados)
        
        # Limpar resultados anteriores do evento
        print(f"[CONTROLADOR] Limpando resultados anteriores do evento {evento_id}...")
        removidos = self.dao.limpar_resultados_evento(evento_id)
        print(f"[CONTROLADOR] {removidos} resultados anteriores removidos")
        
        # Definir evento_id nos resultados
        print(f"[CONTROLADOR] Definindo evento_id={evento_id} em {len(resultados_com_rankings)} resultados")
        for resultado in resultados_com_rankings:
            resultado.evento_id = evento_id
        
        # Salvar no banco
        print(f"[CONTROLADOR] Salvando resultados no banco...")
        total_salvos = self.dao.salvar_lote_resultados(resultados_com_rankings)
        print(f"[CONTROLADOR] Total salvo: {total_salvos}")
        
        return total_salvos, erros
    
    def _eh_linha_dados(self, linha: List[str]) -> bool:
        """
        Verifica se uma linha contém dados válidos (não é cabeçalho).
        
        Args:
            linha: Lista de strings da linha
            
        Returns:
            True se é linha de dados, False caso contrário
        """
        if len(linha) < 2:
            return False
        
        # Verificar se o segundo campo parece ser um tempo
        tempo = linha[1].strip()
        return self._validar_formato_tempo(tempo)
    
    def _processar_linha(self, linha: List[str], data_evento: str) -> Tuple[Resultado, Dict[str, Any]]:
        """
        Processa uma linha do CSV.
        
        Args:
            linha: Lista de strings da linha
            data_evento: Data do evento
            
        Returns:
            Tupla (resultado, erro)
        """
        erro = None
        
        # Validar formato da linha
        if len(linha) < 2:
            erro = {
                'tipo': 'formato_invalido',
                'mensagem': 'Linha deve ter pelo menos 2 colunas (CPF, Tempo)',
                'dados': linha
            }
            return None, erro
        
        cpf = linha[0].strip()
        tempo = linha[1].strip()
        
        # Validar CPF
        if not self._validar_cpf(cpf):
            erro = {
                'tipo': 'cpf_invalido',
                'mensagem': f'CPF inválido: {cpf}',
                'dados': {'cpf': cpf, 'tempo': tempo}
            }
            return None, erro
        
        # Validar tempo
        if not self._validar_formato_tempo(tempo):
            erro = {
                'tipo': 'tempo_invalido',
                'mensagem': f'Formato de tempo inválido: {tempo}',
                'dados': {'cpf': cpf, 'tempo': tempo}
            }
            return None, erro
        
        # Buscar atleta
        atleta = obter_atleta_por_cpf(cpf)
        if not atleta:
            erro = {
                'tipo': 'atleta_nao_encontrado',
                'mensagem': f'Atleta com CPF {cpf} não encontrado',
                'dados': {'cpf': cpf, 'tempo': tempo}
            }
            return None, erro
        
        # Criar resultado
        try:
            resultado = criar_resultado_para_atleta(atleta, tempo, data_evento)
            return resultado, None
        except Exception as e:
            erro = {
                'tipo': 'erro_criacao',
                'mensagem': f'Erro ao criar resultado: {e}',
                'dados': {'cpf': cpf, 'tempo': tempo}
            }
            return None, erro
    
    def _validar_cpf(self, cpf: str) -> bool:
        """
        Valida formato básico do CPF.
        
        Args:
            cpf: CPF para validar
            
        Returns:
            True se formato é válido, False caso contrário
        """
        # Limpar CPF (remover pontos, traços, espaços)
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Verificar se tem 11 dígitos
        return len(cpf_limpo) == 11
    
    def _validar_formato_tempo(self, tempo: str) -> bool:
        """
        Valida formato do tempo HH:MM:SS.
        
        Args:
            tempo: Tempo para validar
            
        Returns:
            True se formato é válido, False caso contrário
        """
        try:
            partes = tempo.split(':')
            if len(partes) != 3:
                return False
            
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])
            
            # Validações básicas
            if horas < 0 or minutos < 0 or segundos < 0:
                return False
            if minutos >= 60 or segundos >= 60:
                return False
            
            return True
        except (ValueError, IndexError):
            return False
    
    def calcular_rankings(self, resultados: List[Resultado]) -> List[Resultado]:
        """
        Calcula as classificações dos resultados baseado nas regras de negócio.
        
        Implementa:
        - RN06: Classificação Geral = Top 5 de cada gênero
        - RN07: Demais atletas classificados por categoria (Júnior, Adulto, Master)
        - PCD compete separadamente
        
        Args:
            resultados: Lista de resultados sem classificações
            
        Returns:
            Lista de resultados com classificações calculadas
        """
        # Limpar classificações existentes
        for resultado in resultados:
            resultado.limpar_classificacoes()
        
        # Separar por gênero
        masculino, feminino = separar_resultados_por_genero(resultados)
        
        # Ordenar por tempo
        masculino_ordenado = ordenar_resultados_por_tempo(masculino)
        feminino_ordenado = ordenar_resultados_por_tempo(feminino)
        
        # RN06: Classificação Geral (Top 5 de cada gênero)
        for i, resultado in enumerate(masculino_ordenado[:5], 1):
            resultado.definir_classificacao_geral(i)
        
        for i, resultado in enumerate(feminino_ordenado[:5], 1):
            resultado.definir_classificacao_geral(i)
        
        # RN07: Classificação por categoria para os demais
        self._calcular_classificacao_categoria(masculino_ordenado[5:])
        self._calcular_classificacao_categoria(feminino_ordenado[5:])
        
        return resultados
    
    def _calcular_classificacao_categoria(self, resultados: List[Resultado]):
        """
        Calcula classificação por categoria para uma lista de resultados.
        
        Args:
            resultados: Lista de resultados (já ordenados por tempo)
        """
        # Separar por categoria
        categorias = {}
        for resultado in resultados:
            categoria = resultado.categoria
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(resultado)
        
        # Calcular posição em cada categoria
        for categoria, resultados_categoria in categorias.items():
            # Já estão ordenados por tempo
            for i, resultado in enumerate(resultados_categoria, 1):
                resultado.definir_classificacao_categoria(i)
    
    def obter_resumo_importacao(self, total_importados: int, erros: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cria um resumo da importação para exibição.
        
        Args:
            total_importados: Número de resultados importados
            erros: Lista de erros encontrados
            
        Returns:
            Dicionário com resumo da importação
        """
        # Contar erros por tipo
        erros_por_tipo = {}
        for erro in erros:
            tipo = erro['tipo']
            erros_por_tipo[tipo] = erros_por_tipo.get(tipo, 0) + 1
        
        return {
            'total_importados': total_importados,
            'total_erros': len(erros),
            'erros_por_tipo': erros_por_tipo,
            'sucesso': len(erros) == 0,
            'taxa_sucesso': (total_importados / (total_importados + len(erros))) * 100 if (total_importados + len(erros)) > 0 else 0
        }
    
    def validar_arquivo_csv(self, caminho_arquivo: str) -> Tuple[bool, str]:
        """
        Valida se um arquivo é um CSV válido para importação.
        
        Args:
            caminho_arquivo: Caminho do arquivo
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if not os.path.exists(caminho_arquivo):
            return False, "Arquivo não encontrado"
        
        if not caminho_arquivo.lower().endswith('.csv'):
            return False, "Arquivo deve ter extensão .csv"
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo)
                
                # Verificar se tem pelo menos uma linha
                primeira_linha = next(leitor, None)
                if not primeira_linha:
                    return False, "Arquivo está vazio"
                
                # Verificar se tem pelo menos 2 colunas
                if len(primeira_linha) < 2:
                    return False, "Arquivo deve ter pelo menos 2 colunas (CPF, Tempo)"
                
                # Contar linhas
                total_linhas = 1  # Já lemos a primeira
                for linha in leitor:
                    total_linhas += 1
                
                if total_linhas < 2:
                    return False, "Arquivo deve ter pelo menos 2 linhas (cabeçalho + dados)"
                
                return True, f"Arquivo válido com {total_linhas} linhas"
                
        except Exception as e:
            return False, f"Erro ao ler arquivo: {e}"


if __name__ == "__main__":
    # Teste do controlador
    print("=== Teste do ControladorImportacao ===")
    
    controlador = ControladorImportacao()
    
    # Teste de validação de CPF
    print("Teste de validação de CPF:")
    cpfs_teste = ["11111111111", "123.456.789-01", "12345678901", "123", "abc"]
    for cpf in cpfs_teste:
        valido = controlador._validar_cpf(cpf)
        print(f"  {cpf}: {'✓' if valido else '✗'}")
    
    # Teste de validação de tempo
    print("\nTeste de validação de tempo:")
    tempos_teste = ["01:30:45", "2:15:30", "00:45:00", "1:70:00", "abc", "1:30"]
    for tempo in tempos_teste:
        valido = controlador._validar_formato_tempo(tempo)
        print(f"  {tempo}: {'✓' if valido else '✗'}")
    
    # Teste de cálculo de rankings
    print("\nTeste de cálculo de rankings:")
    from entidade.resultado import Resultado
    
    resultados_teste = [
        Resultado("11111111111", "Atleta A", "Masculino", "01:30:00", "Adulto"),
        Resultado("11111111112", "Atleta B", "Masculino", "01:25:00", "Adulto"),
        Resultado("22222222221", "Atleta C", "Feminino", "01:35:00", "Adulto"),
        Resultado("22222222222", "Atleta D", "Feminino", "01:40:00", "Adulto"),
    ]
    
    resultados_com_rankings = controlador.calcular_rankings(resultados_teste)
    
    print("Resultados com rankings:")
    for resultado in resultados_com_rankings:
        geral = f"Geral: {resultado.classificacao_geral}º" if resultado.classificacao_geral else ""
        categoria = f"Categoria: {resultado.classificacao_categoria}º" if resultado.classificacao_categoria else ""
        print(f"  {resultado.nome_atleta} ({resultado.genero_atleta}) - {resultado.tempo_final} - {geral} {categoria}")
    
    print("\nTeste do controlador concluído!")
