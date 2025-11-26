import bcrypt
import FreeSimpleGUI as sg
import re
from entidade.atleta import Atleta
from limite.tela_cadastro import TelaCadastro
from limite.tela_atleta import TelaAtleta


class ControladorAtleta:
    def __init__(self, controlador_sistema, usuario_dao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_cadastro = TelaCadastro()
        self.__tela_atleta = TelaAtleta()
        self.__usuario_dao = usuario_dao

    def abre_tela_cadastro(self):
        evento, valores = self.__tela_cadastro.exibir_janela_cadastro('Atleta')
        if evento is None or evento == sg.WIN_CLOSED or evento == '-VOLTAR-':
            return

        campos_obrigatorios = ['-NOME-', '-CPF-', '-EMAIL-', '-DATA_NASC-', '-GENERO-', '-SENHA-']
        if evento == '-CADASTRAR-':

            if any(not valores[key].strip() for key in campos_obrigatorios):
                self.__controlador_sistema.exibir_popup_erro('Todos os campos com * devem ser preenchidos')
                return

            cpf_limpo_para_consulta = re.sub(r'[^0-9]', '', valores['-CPF-'])
            cpf_existente = self.__usuario_dao.get(cpf_limpo_para_consulta)

            if cpf_existente:
                self.__controlador_sistema.exibir_popup_erro('O CPF informado já está cadastrado')
                return

            try:
                senha_pura = valores['-SENHA-'].encode('utf-8')
                senha_hash = bcrypt.hashpw(senha_pura, bcrypt.gensalt()).decode('utf-8')

                novo_atleta = Atleta(
                    nome=valores['-NOME-'],
                    cpf=valores['-CPF-'],
                    email=valores['-EMAIL-'],
                    senha_hash=senha_hash,
                    data_nascimento=valores['-DATA_NASC-'],
                    genero=valores['-GENERO-'],
                    pcd=valores['-PCD_SIM-'],
                )
                self.__usuario_dao.add(novo_atleta)
                self.__controlador_sistema.exibir_popup_sucesso('Cadastro Efetuado com sucesso')

                print('Atelta adicionad à lista', novo_atleta.nome)
            except Exception as e:
                self.__controlador_sistema.exibir_popup_erro(f'Erro ao criar atleta: {e}')

    def abrir_painel_principal(self, atleta: Atleta):
        eventos_disponiveis = []
        janela_painel = self.__tela_atleta.exibir_painel(atleta.nome, eventos_disponiveis)
        while True:
            evento, valores = janela_painel.read()
            if evento in(sg.WIN_CLOSED, '-SAIR-'):
                break
            if evento == '-EDITAR_INFOS-':
                self.abre_tela_editar(atleta)
                janela_painel['-TEXTO_BEM_VINDO-'].update(f'Bem-vindo, {atleta.nome}!')
            if evento == '-APAGAR_CONTA-':
                if sg.popup_yes_no('Tem certeza que deseja apagar sua conta? Essa ação não pode ser desfeita.',
                                   title='Atenção') == 'Yes':
                    self.__usuario_dao.remove(atleta.cpf)
                    self.__controlador_sistema.exibir_popup_sucesso('Conta apagada com sucesso.')
                    break
        janela_painel.close()

    def abre_tela_editar(self, atleta:Atleta):
        evento, valores = self.__tela_cadastro.exibir_janela_edicao(atleta.nome, atleta.email)
        if evento is None or evento == sg.WIN_CLOSED or evento == '-VOLTAR-':
            return

        if evento == '-ATUALIZAR-':
            novo_nome = valores['-NOME-']
            novo_email = valores['-EMAIL-']
            nova_senha = valores['-SENHA-']
            try:
                if nova_senha and nova_senha.strip():
                    senha_pura = nova_senha.encode('utf-8')
                    senha_hash = bcrypt.hashpw(senha_pura, bcrypt.gensalt()).decode('utf-8')
                    atleta.set_senha_hash(senha_hash)
                if novo_nome and novo_nome.strip() and novo_nome != atleta.nome:
                    atleta.nome = novo_nome
                if novo_email and novo_nome.strip() and novo_email != atleta.email:
                    atleta.email = novo_email
                self.__usuario_dao.update(atleta)
                self.__controlador_sistema.exibir_popup_sucesso('Dados atualizados com sucesso')
            except ValueError as e:
                self.__controlador_sistema.exibir_popup_erro(str(e))