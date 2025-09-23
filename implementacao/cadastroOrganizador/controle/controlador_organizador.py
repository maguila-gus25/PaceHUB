import re
import bcrypt
from entidade.organizador import Organizador
from persistencia.organizador_dao import OrganizadorDAO
from limite.tela_organizador import criar_janela_cadastro, exibir_popup_erro, exibir_popup_sucesso


class ControladorOrganizador:
	def __init__(self):
		self.dao = OrganizadorDAO()
		self.janela_cadastro = None

	# Validações embutidas conforme requisito
	def validar_nome_completo(self, nome: str) -> bool:
		return len(nome.strip().split()) >= 2

	def validar_email(self, email: str) -> bool:
		padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
		return re.match(padrao, email) is not None

	def validar_cpf(self, cpf: str) -> bool:
		cpf = ''.join(re.findall(r'\d', cpf))
		if len(cpf) != 11 or len(set(cpf)) == 1:
			return False
		soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
		resto = (soma * 10) % 11
		if resto == 10:
			resto = 0
		if resto != int(cpf[9]):
			return False
		soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
		resto = (soma * 10) % 11
		if resto == 10:
			resto = 0
		if resto != int(cpf[10]):
			return False
		return True

	def _hash_senha(self, senha: str) -> str:
		senha_bytes = senha.encode('utf-8')
		salt = bcrypt.gensalt()
		hash_bytes = bcrypt.hashpw(senha_bytes, salt)
		return hash_bytes.decode('utf-8')

	def abrir_janela_cadastro(self):
		self.janela_cadastro = criar_janela_cadastro('Organizador')
		return self.janela_cadastro

	def cadastrar_organizador(self, values):
		nome = values['-NOME-']
		cpf_input = values['-CPF-']
		email = values['-EMAIL-']
		senha = values['-SENHA-']

		if not all([nome, cpf_input, email, senha]):
			exibir_popup_erro('Todos os campos com * são obrigatórios!')
			return False
		if not self.validar_nome_completo(nome):
			exibir_popup_erro('Por favor, insira seu nome completo (nome e sobrenome).')
			return False
		if not self.validar_cpf(cpf_input):
			exibir_popup_erro('O CPF inserido é inválido!')
			return False
		if not self.validar_email(email):
			exibir_popup_erro('O formato do e-mail inserido é inválido.')
			return False

		cpf_limpo = ''.join(re.findall(r'\d', cpf_input))
		if self.dao.cpf_ja_existe(cpf_limpo):
			exibir_popup_erro(f'O CPF {cpf_limpo} já está cadastrado no sistema.')
			return False

		senha_hash = self._hash_senha(senha)
		organizador = Organizador(nome=nome, cpf=cpf_limpo, email=email)
		organizador.senha_hash = senha_hash
		self.dao.salvar_organizador(organizador)

		exibir_popup_sucesso('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
		return True
