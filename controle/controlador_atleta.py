import bcrypt
from entidade.atleta import Atleta
from limite.tela_cadastro import TelaCadastro


class ControladorAtleta:
    def __init__(self, controlador_sistema, tela_principal, usuario_dao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_cadastro = TelaCadastro(tela_principal.root)
        self.__usuario_dao = usuario_dao


    def abre_tela_cadastro(self):
        evento, valores = self.__tela_cadastro.exibir_janela_cadastro('Atleta')

        if evento == '-CADASTRAR-':
            if not all(valores[key] for key in ['-NOME-', '-CPF-', '-EMAIL-', '-SENHA-']):
                self.__controlador_sistema.exibir_popup_erro('Todos os campos com * devem ser preenchidos')
                return

            cpf_existente = self.__usuario_dao.get(valores['-CPF-'])

            if cpf_existente:
                self.__controlador_sistema.exibir_popup_erro('O CPF informado já está cadastrado')
                return

            try:
                senha_pura = valores['-SENHA-'].encode('utf-8')
                senha_hash = bcrypt.hashpw(senha_pura, bcrypt.gensalt()).decode('utf-8')

                novo_atleta = Atleta(
                    nome = valores['-NOME-'],
                    cpf = valores['-CPF-'],
                    email = valores['-EMAIL-'],
                    senha_hash = senha_hash,
                    data_nascimento=valores['-DATA_NASC-'],
                    genero=valores['-GENERO-'],
                    pcd=valores['-PCD_SIM-'],
                )
                self.__usuario_dao.add(novo_atleta)
                self.__controlador_sistema.exibir_popup_sucesso('Cadastro Efetuado com sucesso')

                print('Atelta adicionad à lista', novo_atleta.nome)
            except Exception as e:
                self.__controlador_sistema.exibir_popup_erro(f'Erro ao criar atleta: {e}')

    def listar_atletas(self):
        print("\n--- LISTANDO ATLETAS CADASTRADOS ---")
        todos_usuarios = self.__usuario_dao.get_all()
        if not todos_usuarios:
            print("Nenhum atleta cadastrado no momento.")
            self.__controlador_sistema.exibir_popup_sucesso("Nenhum atleta cadastrado.")
            return

        for usuario in todos_usuarios:
            if isinstance(usuario, Atleta):
                print(f"Nome: {usuario.nome}, CPF: {usuario.cpf}, Email: {usuario.email}")

        print("------------------------------------")
        self.__controlador_sistema.exibir_popup_sucesso("Lista de atletas impressa no console/terminal!")
