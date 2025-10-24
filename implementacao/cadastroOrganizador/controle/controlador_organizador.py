import re
import PySimpleGUI as sg
import bcrypt
from entidade.organizador import Organizador
from persistencia.organizador_dao import OrganizadorDAO
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from limite.tela_sistema import TelaSistema
from validadores import validar_nome_completo, validar_email, validar_cpf

class ControladorOrganizador:
    def __init__(self, tela_sistema: TelaSistema):
        self.organizador_dao = OrganizadorDAO()
        self.tela_sistema = tela_sistema
        self.janela_cadastro = None
        self.janela_listagem = None
        self.janela_edicao = None
        self.janela_busca = None
        self.janela_detalhes = None

    def _hash_senha(self, senha: str) -> str:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        return hash_bytes.decode('utf-8')

    def abrir_tela_cadastro(self):
        self.janela_cadastro = self.tela_sistema.criar_janela_cadastro_organizador()
        
        if self.janela_cadastro is None:
            print("Error: Failed to create window")
            return False
        
        while True:
            event, values = self.janela_cadastro.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            if event == '-CADASTRAR-':
                if self.cadastrar_organizador(values):
                    return True
        
        self.fechar_tela_cadastro()
        return False

    def fechar_tela_cadastro(self):
        if self.janela_cadastro:
            self.janela_cadastro.close()
            self.janela_cadastro = None

    def cadastrar_organizador(self, values):
        nome = values['-NOME-']
        cpf_input = values['-CPF-']
        email = values['-EMAIL-']
        senha = values['-SENHA-']

        if not all([nome, cpf_input, email, senha]):
            self.tela_sistema.exibir_popup_erro('Todos os campos com * são obrigatórios!')
            return
        if not validar_nome_completo(nome):
            self.tela_sistema.exibir_popup_erro('Por favor, insira seu nome completo (nome e sobrenome).')
            return
        if not validar_cpf(cpf_input):
            self.tela_sistema.exibir_popup_erro('O CPF inserido é inválido!')
            return
        if not validar_email(email):
            self.tela_sistema.exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return
        
        if self.organizador_dao.cpf_ja_existe(cpf_input):
            self.tela_sistema.exibir_popup_erro(f'O CPF {cpf_input} já está cadastrado no sistema.')
            return

        cpf_limpo = ''.join(re.findall(r'\d', cpf_input))

        senha_hash = self._hash_senha(senha)
        organizador = Organizador(nome=nome, cpf=cpf_limpo, email=email)
        organizador.senha_hash = senha_hash
        
        self.organizador_dao.salvar(organizador)
        
        self.tela_sistema.exibir_popup_sucesso('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
        # Fechar janela de cadastro após sucesso
        self.fechar_tela_cadastro()
        return True

    # ========== MÉTODOS DE LISTAGEM ==========
    
    def abrir_tela_listagem(self):
        """Abre a tela de listagem de organizadores"""
        self.janela_listagem = self.tela_sistema.criar_janela_listagem_organizadores()
        
        if self.janela_listagem is None:
            print("Error: Failed to create list window")
            return
        
        self._atualizar_lista_organizadores()
        
        while True:
            event, values = self.janela_listagem.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            elif event == '-ATUALIZAR-':
                self._atualizar_lista_organizadores()
            elif event == '-EDITAR-':
                if values['-TABELA-']:
                    self._editar_organizador_selecionado(values['-TABELA-'][0])
            elif event == '-DETALHES-':
                if values['-TABELA-']:
                    self._ver_detalhes_organizador(values['-TABELA-'][0])
            elif event == '-DELETAR-':
                if values['-TABELA-']:
                    self._deletar_organizador_selecionado(values['-TABELA-'][0])
            elif event == '-BUSCAR-':
                self.abrir_tela_busca()
        
        self.fechar_tela_listagem()

    def fechar_tela_listagem(self):
        """Fecha a tela de listagem"""
        if self.janela_listagem:
            self.janela_listagem.close()
            self.janela_listagem = None

    def _atualizar_lista_organizadores(self):
        """Atualiza a lista de organizadores na tela"""
        if not self.janela_listagem:
            return
            
        organizadores = self.organizador_dao.listar_todos()
        dados_tabela = []
        
        for org in organizadores:
            dados_tabela.append([
                org.nome,
                org.get_cpf_formatado(),
                org.email,
                len(org.eventos) if org.eventos else 0
            ])
        
        self.janela_listagem['-TABELA-'].update(values=dados_tabela)
        self.janela_listagem['-TOTAL-'].update(f"Total: {len(organizadores)} organizadores")

    # ========== MÉTODOS DE BUSCA ==========
    
    def abrir_tela_busca(self):
        """Abre a tela de busca de organizadores"""
        self.janela_busca = self.tela_sistema.criar_janela_busca_organizador()
        
        if self.janela_busca is None:
            print("Error: Failed to create search window")
            return
        
        while True:
            event, values = self.janela_busca.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            elif event == '-BUSCAR-':
                self._buscar_organizadores(values)
            elif event == '-LIMPAR-':
                self._limpar_busca()
        
        self.fechar_tela_busca()

    def fechar_tela_busca(self):
        """Fecha a tela de busca"""
        if self.janela_busca:
            self.janela_busca.close()
            self.janela_busca = None

    def _buscar_organizadores(self, values):
        """Executa a busca de organizadores"""
        if not self.janela_busca:
            return
            
        termo_busca = values['-TERMO_BUSCA-'].strip()
        tipo_busca = values['-TIPO_BUSCA-']
        
        if not termo_busca:
            self.tela_sistema.exibir_popup_erro('Digite um termo para buscar!')
            return
        
        organizadores = []
        if tipo_busca == 'Nome':
            organizadores = self.organizador_dao.buscar_por_nome(termo_busca)
        elif tipo_busca == 'CPF':
            org = self.organizador_dao.buscar_por_cpf(termo_busca)
            if org:
                organizadores = [org]
        
        # Atualizar tabela de resultados
        dados_tabela = []
        for org in organizadores:
            dados_tabela.append([
                org.nome,
                org.get_cpf_formatado(),
                org.email,
                len(org.eventos) if org.eventos else 0
            ])
        
        self.janela_busca['-TABELA_RESULTADOS-'].update(values=dados_tabela)
        self.janela_busca['-TOTAL_RESULTADOS-'].update(f"Encontrados: {len(organizadores)} organizadores")

    def _limpar_busca(self):
        """Limpa os campos de busca"""
        if self.janela_busca:
            self.janela_busca['-TERMO_BUSCA-'].update('')
            self.janela_busca['-TABELA_RESULTADOS-'].update(values=[])
            self.janela_busca['-TOTAL_RESULTADOS-'].update('Encontrados: 0 organizadores')

    # ========== MÉTODOS DE EDIÇÃO ==========
    
    def abrir_tela_edicao(self, organizador: Organizador):
        """Abre a tela de edição de organizador"""
        self.janela_edicao = self.tela_sistema.criar_janela_edicao_organizador(organizador)
        
        if self.janela_edicao is None:
            print("Error: Failed to create edit window")
            return
        
        while True:
            event, values = self.janela_edicao.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            elif event == '-SALVAR-':
                self._salvar_edicao_organizador(organizador, values)
                break
        
        self.fechar_tela_edicao()

    def fechar_tela_edicao(self):
        """Fecha a tela de edição"""
        if self.janela_edicao:
            self.janela_edicao.close()
            self.janela_edicao = None

    def _editar_organizador_selecionado(self, indice_selecionado):
        """Edita o organizador selecionado na lista"""
        organizadores = self.organizador_dao.listar_todos()
        if 0 <= indice_selecionado < len(organizadores):
            organizador = organizadores[indice_selecionado]
            self.abrir_tela_edicao(organizador)
            # Atualizar lista após edição
            if self.janela_listagem:
                self._atualizar_lista_organizadores()

    def _salvar_edicao_organizador(self, organizador: Organizador, values):
        """Salva as alterações do organizador"""
        nome = values['-NOME-']
        email = values['-EMAIL-']
        senha = values['-SENHA-']
        
        # Validações
        if not all([nome, email]):
            self.tela_sistema.exibir_popup_erro('Nome e email são obrigatórios!')
            return
        
        if not validar_nome_completo(nome):
            self.tela_sistema.exibir_popup_erro('Por favor, insira um nome completo (nome e sobrenome).')
            return
        
        if not validar_email(email):
            self.tela_sistema.exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return
        
        # Atualizar dados
        organizador.atualizar_dados(nome=nome, email=email)
        
        # Se senha foi fornecida, atualizar hash
        if senha:
            if len(senha) < 6:
                self.tela_sistema.exibir_popup_erro('A senha deve ter pelo menos 6 caracteres!')
                return
            senha_hash = self._hash_senha(senha)
            organizador.atualizar_dados(senha_hash=senha_hash)
        
        # Salvar no banco
        if self.organizador_dao.atualizar(organizador):
            self.tela_sistema.exibir_popup_sucesso('Organizador atualizado com sucesso!')
        else:
            self.tela_sistema.exibir_popup_erro('Erro ao atualizar organizador!')

    # ========== MÉTODOS DE DETALHES ==========
    
    def abrir_tela_detalhes(self, organizador: Organizador):
        """Abre a tela de detalhes do organizador"""
        self.janela_detalhes = self.tela_sistema.criar_janela_detalhes_organizador(organizador)
        
        if self.janela_detalhes is None:
            print("Error: Failed to create details window")
            return
        
        while True:
            event, values = self.janela_detalhes.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            elif event == '-EDITAR-':
                self.fechar_tela_detalhes()
                self.abrir_tela_edicao(organizador)
                break
        
        self.fechar_tela_detalhes()

    def fechar_tela_detalhes(self):
        """Fecha a tela de detalhes"""
        if self.janela_detalhes:
            self.janela_detalhes.close()
            self.janela_detalhes = None

    def _ver_detalhes_organizador(self, indice_selecionado):
        """Mostra detalhes do organizador selecionado"""
        organizadores = self.organizador_dao.listar_todos()
        if 0 <= indice_selecionado < len(organizadores):
            organizador = organizadores[indice_selecionado]
            self.abrir_tela_detalhes(organizador)

    # ========== MÉTODOS DE DELEÇÃO ==========
    
    def _deletar_organizador_selecionado(self, indice_selecionado):
        """Deleta o organizador selecionado"""
        organizadores = self.organizador_dao.listar_todos()
        if 0 <= indice_selecionado < len(organizadores):
            organizador = organizadores[indice_selecionado]
            
            # Confirmação dupla
            resposta = sg.popup_yes_no(
                f'Deseja realmente deletar o organizador?\n\n{organizador.nome}\n{organizador.get_cpf_formatado()}',
                title='Confirmar Exclusão'
            )
            
            if resposta == 'Yes':
                if self.organizador_dao.deletar(organizador.cpf):
                    self.tela_sistema.exibir_popup_sucesso('Organizador deletado com sucesso!')
                    self._atualizar_lista_organizadores()
                else:
                    self.tela_sistema.exibir_popup_erro('Erro ao deletar organizador!')

    # ========== MÉTODOS AUXILIARES ==========
    
    def listar_organizadores(self) -> list:
        """Retorna lista de todos os organizadores"""
        return self.organizador_dao.listar_todos()

    def buscar_organizador_por_cpf(self, cpf: str) -> Organizador:
        """Busca organizador por CPF"""
        return self.organizador_dao.buscar_por_cpf(cpf)

    def contar_organizadores(self) -> int:
        """Conta total de organizadores"""
        return self.organizador_dao.contar_organizadores()