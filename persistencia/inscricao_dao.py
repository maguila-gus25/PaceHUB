# persistencia/inscricao_dao.py
import sqlite3
from typing import LiteralString

from entidade.inscricao import Inscricao
from entidade.kit_de_corrida import KitDeCorrida


class InscricaoDAO:
    def __init__(self, db_path='banco.db'):
        self.__db_path = db_path

    def __conectar(self):
        return sqlite3.connect(self.__db_path)

    def add(self, inscricao: Inscricao):
        conexao = self.__conectar()
        cursor = conexao.cursor()

        if isinstance(inscricao, Inscricao):
            dados = (
                inscricao.data_inscricao_str,
                inscricao.kit_entregue,
                inscricao.status,
                inscricao.atleta_cpf_str,
                inscricao.evento_id,
                inscricao.kit_id
            )

            sql = """
            INSERT INTO inscricoes
            (data_inscricao, kit_entregue, status, atleta_cpf, evento_id, kit_id)
            values (?, ?, ?, ?, ?, ?);
            """

            cursor.execute(sql, dados)
            inscricao.id = cursor.lastrowid

            conexao.commit()
            print(f"Inscrição ID {inscricao.id} salva para o atleta {inscricao.atleta_cpf}")
            conexao.close()

    def get_by_atleta_and_evento(self, atleta_cpf, evento_id):
        conexao = self.__conectar()
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        sql = ("""
               select inscricoes.*, 
               kitsdecorrida.nome as kit_nome,
               kitsdecorrida.descricao as kit_descricao,
               kitsdecorrida.valor as kit_valor
               from inscricoes
               join kitsdecorrida
                on inscricoes.kit_id = kitsdecorrida.id
                where atleta_cpf = ? and inscricoes.evento_id = ?;
               """)
        cursor.execute(sql, (atleta_cpf, evento_id))

        dados = cursor.fetchone()

        if dados:
            inscricao = Inscricao(
                atleta_cpf = dados['atleta_cpf'],
                evento_id = dados['evento_id'],
                kit_id = dados['kit_id'],
                status = dados['status'],
                data_inscricao = dados['data_inscricao'],
                kit_entregue = dados['kit_entregue']
            )
            inscricao.id = dados['id']

            kit = KitDeCorrida(
                nome = dados['kit_nome'],
                descricao = dados['kit_descricao'],
                valor = dados['kit_valor']
            )
            return inscricao, kit
        conexao.close()
        return None, None

    def update_kit_entregue(self, inscricao_id: int, kit_entregue: bool):
        conexao = None
        try:
            conexao = self.__conectar()
            cursor = conexao.cursor()

            sql = "UPDATE inscricoes SET kit_entregue = ? WHERE ID = ?;"
            cursor.execute(sql, (int(kit_entregue), inscricao_id))

            conexao.commit()
            print(f"Status do kit para Inscrição ID {inscricao_id} atualizado.")

        except sqlite3.Error as e:
            if conexao:
                conexao.rollback()
            print(f"Erro ao atualizar kit: {e}")
        finally:
            if conexao:
                conexao.close()

    def count_by_evento(self, evento_id: int):
        conexao = None
        try:
            conexao = self.__conectar()
            cursor = conexao.cursor()

            sql = "SELECT COUNT(*) FROM Inscricoes WHERE evento_id = ?;"
            cursor.execute(sql, (evento_id,))

            count = cursor.fetchone()[0]
            return count

        except sqlite3.Error as e:
            print(f"Erro ao contar inscrições: {e}")
        finally:
            if conexao:
                conexao.close()