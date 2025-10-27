import sqlite3
import os
from typing import List, Optional, Dict, Any
from entidade.resultado import Resultado
from entidade.evento import Evento


class ResultadoDAO:
    """
    Data Access Object para operações com resultados no banco SQLite.
    Implementa operações CRUD completas para a tabela de resultados.
    """
    
    def __init__(self, db_file: str = None):
        """
        Inicializa o DAO com o caminho do banco de dados.
        
        Args:
            db_file: Caminho do arquivo de banco. Se None, usa banco.db na pasta pai.
        """
        if db_file is None:
            # Caminho relativo ao diretório do módulo
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, '..', 'banco.db')
        else:
            self.db_path = db_file
    
    def _get_conexao(self) -> sqlite3.Connection:
        """
        Retorna uma conexão SQLite com configurações otimizadas.
        
        Returns:
            Conexão SQLite configurada
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        conn.execute("PRAGMA foreign_keys = ON")  # Habilita foreign keys
        return conn
    
    def criar_tabelas(self) -> bool:
        """
        Cria as tabelas do schema se não existirem.
        
        Returns:
            True se criou com sucesso, False caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            # Criar tabela eventos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data TEXT NOT NULL,
                    status TEXT NOT NULL,
                    distancia TEXT NOT NULL
                )
            """)
            
            # Criar tabela resultados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    evento_id INTEGER NOT NULL,
                    cpf_atleta TEXT NOT NULL,
                    nome_atleta TEXT NOT NULL,
                    genero_atleta TEXT NOT NULL,
                    tempo_final TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    classificacao_geral INTEGER,
                    classificacao_categoria INTEGER,
                    pcd INTEGER DEFAULT 0,
                    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
                )
            """)
            
            # Criar índices para performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_resultados_evento 
                ON resultados(evento_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_resultados_cpf 
                ON resultados(cpf_atleta)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_resultados_tempo 
                ON resultados(tempo_final)
            """)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def salvar_evento(self, evento: Evento) -> bool:
        """
        Salva um evento no banco de dados.
        
        Args:
            evento: Objeto Evento para salvar
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            print(f"[DAO] Salvando evento: {evento.nome}")
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO eventos (nome, data, status, distancia)
                VALUES (?, ?, ?, ?)
            """, (evento.nome, evento.data, evento.status, evento.distancia))
            
            evento.id = cursor.lastrowid
            print(f"[DAO] Evento salvo com ID: {evento.id}")
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[DAO] ERRO ao salvar evento: {e}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def salvar_resultado(self, resultado: Resultado) -> bool:
        """
        Salva um resultado no banco de dados.
        
        Args:
            resultado: Objeto Resultado para salvar
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO resultados 
                (evento_id, cpf_atleta, nome_atleta, genero_atleta, 
                 tempo_final, categoria, classificacao_geral, classificacao_categoria, pcd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                resultado.evento_id,
                resultado.cpf_atleta,
                resultado.nome_atleta,
                resultado.genero_atleta,
                resultado.tempo_final,
                resultado.categoria,
                resultado.classificacao_geral,
                resultado.classificacao_categoria,
                1 if resultado.pcd else 0
            ))
            
            resultado.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def salvar_lote_resultados(self, resultados: List[Resultado]) -> int:
        """
        Salva múltiplos resultados em uma única transação.
        
        Args:
            resultados: Lista de objetos Resultado
            
        Returns:
            Número de resultados salvos com sucesso
        """
        if not resultados:
            print("[DAO] Lista de resultados vazia, nada para salvar")
            return 0
        
        try:
            print(f"[DAO] Iniciando salvamento de {len(resultados)} resultados")
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            # Preparar dados para inserção em lote
            dados_lote = []
            for resultado in resultados:
                print(f"[DAO] Preparando: {resultado.nome_atleta} - evento_id={resultado.evento_id}")
                dados_lote.append((
                    resultado.evento_id,
                    resultado.cpf_atleta,
                    resultado.nome_atleta,
                    resultado.genero_atleta,
                    resultado.tempo_final,
                    resultado.categoria,
                    resultado.classificacao_geral,
                    resultado.classificacao_categoria,
                    1 if resultado.pcd else 0
                ))
            
            # Inserir em lote
            print(f"[DAO] Executando INSERT de {len(dados_lote)} registros...")
            cursor.executemany("""
                INSERT INTO resultados 
                (evento_id, cpf_atleta, nome_atleta, genero_atleta, 
                 tempo_final, categoria, classificacao_geral, classificacao_categoria, pcd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados_lote)
            
            print(f"[DAO] Linhas afetadas: {cursor.rowcount}")
            
            # Atualizar IDs dos objetos
            # Para executemany, precisamos buscar os IDs inseridos
            cursor.execute("SELECT last_insert_rowid()")
            ultimo_id = cursor.fetchone()[0]
            primeiro_id = ultimo_id - len(resultados) + 1
            
            for i, resultado in enumerate(resultados):
                resultado.id = primeiro_id + i
            
            conn.commit()
            print(f"[DAO] Commit realizado com sucesso! {len(resultados)} resultados salvos")
            conn.close()
            return len(resultados)
            
        except Exception as e:
            print(f"[DAO] ERRO ao salvar lote de resultados: {e}")
            import traceback
            traceback.print_exc()
            if 'conn' in locals():
                conn.close()
            return 0
    
    def buscar_resultados_por_evento(self, evento_id: int) -> List[Resultado]:
        """
        Busca todos os resultados de um evento, ordenados por tempo.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Lista de objetos Resultado ordenados por tempo
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM resultados 
                WHERE evento_id = ? 
                ORDER BY tempo_final ASC
            """, (evento_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            resultados = []
            for row in rows:
                resultado = Resultado(
                    cpf_atleta=row['cpf_atleta'],
                    nome_atleta=row['nome_atleta'],
                    genero_atleta=row['genero_atleta'],
                    tempo_final=row['tempo_final'],
                    categoria=row['categoria'],
                    pcd=bool(row['pcd'])
                )
                resultado.id = row['id']
                resultado.evento_id = row['evento_id']
                resultado.classificacao_geral = row['classificacao_geral']
                resultado.classificacao_categoria = row['classificacao_categoria']
                
                resultados.append(resultado)
            
            return resultados
            
        except Exception as e:
            print(f"Erro ao buscar resultados por evento: {e}")
            if 'conn' in locals():
                conn.close()
            return []
    
    def buscar_resultado_por_cpf(self, cpf: str, evento_id: int) -> Optional[Resultado]:
        """
        Busca um resultado específico por CPF e evento.
        
        Args:
            cpf: CPF do atleta
            evento_id: ID do evento
            
        Returns:
            Objeto Resultado se encontrado, None caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM resultados 
                WHERE cpf_atleta = ? AND evento_id = ?
            """, (cpf, evento_id))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                resultado = Resultado(
                    cpf_atleta=row['cpf_atleta'],
                    nome_atleta=row['nome_atleta'],
                    genero_atleta=row['genero_atleta'],
                    tempo_final=row['tempo_final'],
                    categoria=row['categoria'],
                    pcd=bool(row['pcd'])
                )
                resultado.id = row['id']
                resultado.evento_id = row['evento_id']
                resultado.classificacao_geral = row['classificacao_geral']
                resultado.classificacao_categoria = row['classificacao_categoria']
                
                return resultado
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar resultado por CPF: {e}")
            if 'conn' in locals():
                conn.close()
            return None
    
    def atualizar_resultado(self, resultado: Resultado) -> bool:
        """
        Atualiza um resultado existente no banco.
        
        Args:
            resultado: Objeto Resultado com dados atualizados
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE resultados SET
                    nome_atleta = ?, genero_atleta = ?, tempo_final = ?,
                    categoria = ?, classificacao_geral = ?, classificacao_categoria = ?, pcd = ?
                WHERE id = ?
            """, (
                resultado.nome_atleta,
                resultado.genero_atleta,
                resultado.tempo_final,
                resultado.categoria,
                resultado.classificacao_geral,
                resultado.classificacao_categoria,
                1 if resultado.pcd else 0,
                resultado.id
            ))
            
            sucesso = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return sucesso
            
        except Exception as e:
            print(f"Erro ao atualizar resultado: {e}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def deletar_resultado(self, resultado_id: int) -> bool:
        """
        Deleta um resultado do banco.
        
        Args:
            resultado_id: ID do resultado
            
        Returns:
            True se deletou com sucesso, False caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM resultados WHERE id = ?", (resultado_id,))
            
            sucesso = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return sucesso
            
        except Exception as e:
            print(f"Erro ao deletar resultado: {e}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def limpar_resultados_evento(self, evento_id: int) -> int:
        """
        Remove todos os resultados de um evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Número de resultados removidos
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM resultados WHERE evento_id = ?", (evento_id,))
            
            removidos = cursor.rowcount
            conn.commit()
            conn.close()
            return removidos
            
        except Exception as e:
            print(f"Erro ao limpar resultados do evento: {e}")
            if 'conn' in locals():
                conn.close()
            return 0
    
    def contar_resultados_evento(self, evento_id: int) -> int:
        """
        Conta quantos resultados existem para um evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Número de resultados
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM resultados WHERE evento_id = ?", (evento_id,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception as e:
            print(f"Erro ao contar resultados: {e}")
            if 'conn' in locals():
                conn.close()
            return 0
    
    def buscar_evento_por_id(self, evento_id: int) -> Optional[Evento]:
        """
        Busca um evento por ID.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Objeto Evento se encontrado, None caso contrário
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                evento = Evento(
                    id=row['id'],
                    nome=row['nome'],
                    data=row['data'],
                    status=row['status'],
                    distancia=row['distancia']
                )
                return evento
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar evento: {e}")
            if 'conn' in locals():
                conn.close()
            return None
    
    def listar_eventos(self) -> List[Evento]:
        """
        Lista todos os eventos do banco.
        
        Returns:
            Lista de objetos Evento
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM eventos ORDER BY data DESC")
            
            rows = cursor.fetchall()
            conn.close()
            
            eventos = []
            for row in rows:
                evento = Evento(
                    id=row['id'],
                    nome=row['nome'],
                    data=row['data'],
                    status=row['status'],
                    distancia=row['distancia']
                )
                eventos.append(evento)
            
            return eventos
            
        except Exception as e:
            print(f"Erro ao listar eventos: {e}")
            if 'conn' in locals():
                conn.close()
            return []
    
    def obter_estatisticas_evento(self, evento_id: int) -> Dict[str, Any]:
        """
        Obtém estatísticas de um evento.
        
        Args:
            evento_id: ID do evento
            
        Returns:
            Dicionário com estatísticas
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            
            # Total de resultados
            cursor.execute("SELECT COUNT(*) FROM resultados WHERE evento_id = ?", (evento_id,))
            total_resultados = cursor.fetchone()[0]
            
            # Por gênero
            cursor.execute("""
                SELECT genero_atleta, COUNT(*) 
                FROM resultados 
                WHERE evento_id = ? 
                GROUP BY genero_atleta
            """, (evento_id,))
            por_genero = dict(cursor.fetchall())
            
            # Por categoria
            cursor.execute("""
                SELECT categoria, COUNT(*) 
                FROM resultados 
                WHERE evento_id = ? 
                GROUP BY categoria
            """, (evento_id,))
            por_categoria = dict(cursor.fetchall())
            
            # Melhor tempo
            cursor.execute("""
                SELECT MIN(tempo_final) 
                FROM resultados 
                WHERE evento_id = ?
            """, (evento_id,))
            melhor_tempo = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_resultados': total_resultados,
                'por_genero': por_genero,
                'por_categoria': por_categoria,
                'melhor_tempo': melhor_tempo
            }
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            if 'conn' in locals():
                conn.close()
            return {}


if __name__ == "__main__":
    # Teste do DAO
    print("=== Teste do ResultadoDAO ===")
    
    dao = ResultadoDAO()
    
    # Criar tabelas
    print("Criando tabelas...")
    sucesso = dao.criar_tabelas()
    print(f"Tabelas criadas: {sucesso}")
    
    # Teste de estatísticas (evento inexistente)
    stats = dao.obter_estatisticas_evento(999)
    print(f"Estatísticas evento 999: {stats}")
    
    # Listar eventos
    eventos = dao.listar_eventos()
    print(f"Eventos no banco: {len(eventos)}")
    
    print("Teste do DAO concluído!")
