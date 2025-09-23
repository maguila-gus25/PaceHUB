import sqlite3
import os
from entidade.organizador import Organizador


class OrganizadorDAO:
	def __init__(self, db_path: str = None):
		base_dir = os.path.dirname(os.path.abspath(__file__))
		cadastro_dir = os.path.dirname(base_dir)
		self.db_path = db_path or os.path.join(cadastro_dir, 'banco.db')
		self._criar_tabela_se_nao_existir()

	def _obter_conexao(self):
		return sqlite3.connect(self.db_path)

	def _criar_tabela_se_nao_existir(self):
		with self._obter_conexao() as conn:
			cur = conn.cursor()
			cur.execute(
				"""
				CREATE TABLE IF NOT EXISTS organizadores (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					nome TEXT NOT NULL,
					cpf TEXT NOT NULL UNIQUE,
					email TEXT NOT NULL,
					senha_hash TEXT NOT NULL
				);
				"""
			)
			conn.commit()

	def salvar_organizador(self, organizador: Organizador):
		with self._obter_conexao() as conn:
			cur = conn.cursor()
			cur.execute(
				"INSERT INTO organizadores (nome, cpf, email, senha_hash) VALUES (?, ?, ?, ?)",
				(organizador.nome, organizador.cpf, organizador.email, organizador.senha_hash),
			)
			conn.commit()

	def cpf_ja_existe(self, cpf: str) -> bool:
		cpf_limpo = ''.join([c for c in cpf if c.isdigit()])
		with self._obter_conexao() as conn:
			cur = conn.cursor()
			cur.execute("SELECT 1 FROM organizadores WHERE cpf = ? LIMIT 1", (cpf_limpo,))
			return cur.fetchone() is not None

	def listar_organizadores(self):
		with self._obter_conexao() as conn:
			cur = conn.cursor()
			cur.execute("SELECT nome, cpf, email, senha_hash FROM organizadores")
			rows = cur.fetchall()
			result = []
			for nome, cpf, email, senha_hash in rows:
				org = Organizador(nome=nome, cpf=cpf, email=email)
				org.senha_hash = senha_hash
				result.append(org)
			return result

	def buscar_organizador_por_cpf(self, cpf: str):
		cpf_limpo = ''.join([c for c in cpf if c.isdigit()])
		with self._obter_conexao() as conn:
			cur = conn.cursor()
			cur.execute("SELECT nome, cpf, email, senha_hash FROM organizadores WHERE cpf = ?", (cpf_limpo,))
			row = cur.fetchone()
			if not row:
				return None
			nome, cpf_db, email, senha_hash = row
			org = Organizador(nome=nome, cpf=cpf_db, email=email)
			org.senha_hash = senha_hash
			return org
