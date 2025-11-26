import bcrypt
import FreeSimpleGUI as sg
import re
from entidade.organizador import Organizador
from limite.tela_cadastro import TelaCadastro


class ControladorOrganizador:
    def __init__(self, controlador_sistema, usuario_dao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_cadastro = TelaCadastro()
        self.__usuario_dao = usuario_dao

    def abre_tela_cadastro(self):
        evento, valores = self.__tela_cadastro.exibir_janela_cadastro('Organizador')
        if evento is None or evento == sg.WIN_CLOSED or evento == '-VOLTAR-':
            return

        campos_obrigatorios = ['-NOME-', '-CPF-', '-EMAIL-', '-SENHA-']
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

                novo_organizador = Organizador(
                    nome=valores['-NOME-'],
                    cpf=valores['-CPF-'],
                    email=valores['-EMAIL-'],
                    senha_hash=senha_hash
                )
                self.__usuario_dao.add(novo_organizador)
                self.__controlador_sistema.exibir_popup_sucesso('Cadastro Efetuado com sucesso')

                print('Organizador adicionad à lista', novo_organizador.nome)
            except Exception as e:
                self.__controlador_sistema.exibir_popup_erro(f'Erro ao criar atleta: {e}')

    def listar_organizadores(self):
        print("\n--- LISTANDO ORGANIZADORES CADASTRADOS ---")
        todos_usuarios = self.__usuario_dao.get_all()

        organizadores_encontrados = False
        for usuario in todos_usuarios:
            if isinstance(usuario, Organizador):
                print(
                    f"Nome: {usuario.nome}, CPF: {usuario.cpf}, Email: {usuario.email}")
                organizadores_encontrados = True

        if not organizadores_encontrados:
            print("Nenhum Organizador cadastrado no momento.")
            self.__controlador_sistema.exibir_popup_sucesso("Nenhum organizador cadastrado.")
            return

        print("------------------------------------")
        self.__controlador_sistema.exibir_popup_sucesso("Lista de organizadores impressa no console/terminal!")

    def abre_tela_editar(self, organizador: Organizador):
        evento, valores = self.__tela_cadastro.exibir_janela_edicao_organizador(organizador.nome, organizador.email)
        if evento is None or evento == sg.WIN_CLOSED or evento == '-VOLTAR-':
            return

        if evento == '-ATUALIZAR-':
            novo_nome = valores['-NOME-']
            novo_email = valores['-EMAIL-']
            nova_senha = valores['-SENHA-']

            if not novo_nome or not novo_nome.strip():
                self.__controlador_sistema.exibir_popup_erro('O nome é obrigatório.')
                return

            if not novo_email or not novo_email.strip():
                self.__controlador_sistema.exibir_popup_erro('O email é obrigatório.')
                return

            try:
                # Atualiza senha se fornecida
                if nova_senha and nova_senha.strip():
                    senha_pura = nova_senha.encode('utf-8')
                    senha_hash = bcrypt.hashpw(senha_pura, bcrypt.gensalt()).decode('utf-8')
                    organizador.set_senha_hash(senha_hash)
                
                # Atualiza nome (sempre atualiza, mesmo se igual, para garantir sincronização)
                if novo_nome and novo_nome.strip():
                    organizador.nome = novo_nome
                
                # Atualiza email (sempre atualiza, mesmo se igual, para garantir sincronização)
                if novo_email and novo_email.strip():
                    organizador.email = novo_email
                
                # Persiste as mudanças no banco de dados
                resultado = self.__usuario_dao.update(organizador)
                if resultado:
                    self.__controlador_sistema.exibir_popup_sucesso('Dados atualizados com sucesso')
                else:
                    self.__controlador_sistema.exibir_popup_erro('Erro ao atualizar dados no banco de dados')
            except ValueError as e:
                self.__controlador_sistema.exibir_popup_erro(str(e))
            except Exception as e:
                self.__controlador_sistema.exibir_popup_erro(f'Erro ao atualizar organizador: {e}')

    def deletar_organizador_e_eventos(self, organizador: Organizador):
        from datetime import datetime
        from persistencia.evento_dao import EventoDAO
        from persistencia.inscricao_dao import InscricaoDAO

        evento_dao = EventoDAO()
        inscricao_dao = InscricaoDAO()

        # Busca todos os eventos do organizador
        eventos_do_organizador = evento_dao.get_all_by_organizador(organizador.cpf)

        # Filtra eventos não concluídos (data >= hoje)
        eventos_nao_concluidos = []
        for evento in eventos_do_organizador:
            try:
                data_evento_obj = datetime.strptime(evento.data, '%d/%m/%Y')
                if data_evento_obj >= datetime.now():
                    eventos_nao_concluidos.append(evento)
            except ValueError:
                # Se a data for inválida, considera como não concluído para segurança
                eventos_nao_concluidos.append(evento)

        # Deleta eventos não concluídos e suas inscrições
        for evento in eventos_nao_concluidos:
            try:
                # Deleta todas as inscrições do evento
                inscricao_dao.delete_by_evento(evento.id)
                # Deleta o evento (kits serão deletados via cascade)
                evento_dao.delete_evento(evento.id)
            except Exception as e:
                print(f"Erro ao deletar evento {evento.id}: {e}")

        # Deleta o organizador
        try:
            self.__usuario_dao.remove(organizador.cpf)
            self.__controlador_sistema.exibir_popup_sucesso('Conta e eventos não concluídos apagados com sucesso.')
        except Exception as e:
            self.__controlador_sistema.exibir_popup_erro(f'Erro ao deletar organizador: {e}')