import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        sg.theme('DarkBlue14')

    def criar_janela_login(self):
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Sistema de Gestão de Organizadores', font=('Helvetica', 16, 'bold'), justification='center', expand_x=True)],
            [sg.Text('Faça login para acessar sua conta', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Text('Login', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Text('CPF*', font=('Helvetica', 12)), sg.Input(key='-CPF_LOGIN-', size=(30, 1), font=('Helvetica', 11))],
            [sg.Text('Senha*', font=('Helvetica', 12)), sg.Input(key='-SENHA_LOGIN-', password_char='*', size=(30, 1), font=('Helvetica', 11))],
            [sg.Text('* Campos obrigatórios', text_color='red', font=('Helvetica', 10))],
            [sg.Text('')],
            [sg.Button('Entrar', key='-ENTRAR-', size=(12, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('_' * 50)],
            [sg.Text('Ainda não tem uma conta?', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.Button('Cadastrar como Organizador', key='-CADASTRAR-', size=(25, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969'))],
            [sg.VPush()],
        ]
        return sg.Window('PaceHub - Login', layout, size=(600, 500), finalize=True, resizable=False)

    def criar_janela_cadastro_organizador(self):
        layout_usuario = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Cadastro de Organizador', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Frame('Dados Pessoais', [
                [sg.Text('Nome Completo*', size=(15, 1), font=('Helvetica', 12)), sg.Input(key='-NOME-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('CPF*', size=(15, 1), font=('Helvetica', 12)), sg.Input(key='-CPF-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Email*', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-EMAIL-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Senha*', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-SENHA-', password_char='*', size=(40, 1), font=('Helvetica', 11))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('* Todos os campos são obrigatórios.', text_color='red', font=('Helvetica', 10))],
            [sg.Text('_' * 50)],
            [sg.Button('Cadastrar', key='-CADASTRAR-', size=(12, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969'))],
            [sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Cadastro de Organizador', [layout_usuario], finalize=True, resizable=False, size=(600, 500))

    def exibir_popup_erro(self, mensagem: str):
        sg.popup_error(mensagem)

    def exibir_popup_sucesso(self, mensagem: str, dados: str = ""):
        sg.popup(mensagem, dados)

    # ========== TELAS CRUD DE ORGANIZADORES ==========

    def criar_janela_listagem_organizadores(self):
        """Cria a janela de listagem de organizadores"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Listagem de Organizadores', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Text('Ações:', font=('Helvetica', 14, 'bold'))],
            [sg.Button('Buscar', key='-BUSCAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Atualizar', key='-ATUALIZAR-', size=(12, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('_' * 50)],
            [sg.Text('Lista de Organizadores:', font=('Helvetica', 14, 'bold'))],
            [sg.Table(
                values=[],
                headings=['Nome', 'CPF', 'Email', 'Eventos'],
                key='-TABELA-',
                col_widths=[25, 15, 30, 8],
                auto_size_columns=False,
                justification='left',
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                enable_events=True,
                expand_x=True,
                expand_y=True,
                font=('Helvetica', 10),
                header_font=('Helvetica', 12, 'bold')
            )],
            [sg.Text('Total: 0 organizadores', key='-TOTAL-', font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Text('Ações na linha selecionada:', font=('Helvetica', 14, 'bold'))],
            [sg.Button('Ver Detalhes', key='-DETALHES-', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Editar', key='-EDITAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Deletar', key='-DELETAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#DC143C'))],
            [sg.Text('_' * 50)],
            [sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Listagem de Organizadores', layout, size=(1000, 750), finalize=True, resizable=False)

    def criar_janela_busca_organizador(self):
        """Cria a janela de busca de organizadores"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Buscar Organizadores', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Text('Critérios de Busca:', font=('Helvetica', 14, 'bold'))],
            [sg.Text('Tipo de busca:', font=('Helvetica', 12)), 
             sg.Combo(['Nome', 'CPF'], default_value='Nome', key='-TIPO_BUSCA-', size=(15, 1), font=('Helvetica', 11))],
            [sg.Text('Termo de busca:', font=('Helvetica', 12)), sg.Input(key='-TERMO_BUSCA-', size=(40, 1), font=('Helvetica', 11))],
            [sg.Button('Buscar', key='-BUSCAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Limpar', key='-LIMPAR-', size=(8, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('_' * 50)],
            [sg.Text('Resultados:', font=('Helvetica', 14, 'bold'))],
            [sg.Table(
                values=[],
                headings=['Nome', 'CPF', 'Email', 'Eventos'],
                key='-TABELA_RESULTADOS-',
                col_widths=[25, 15, 30, 8],
                auto_size_columns=False,
                justification='left',
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                enable_events=True,
                expand_x=True,
                expand_y=True,
                font=('Helvetica', 10),
                header_font=('Helvetica', 12, 'bold')
            )],
            [sg.Text('Encontrados: 0 organizadores', key='-TOTAL_RESULTADOS-', font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Buscar Organizadores', layout, size=(900, 650), finalize=True, resizable=False)

    def criar_janela_edicao_organizador(self, organizador):
        """Cria a janela de edição de organizador"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Editar Organizador', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Frame('Dados Pessoais', [
                [sg.Text('Nome Completo*', size=(15, 1), font=('Helvetica', 12)), sg.Input(organizador.nome, key='-NOME-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('CPF*', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.get_cpf_formatado(), text_color='gray', font=('Helvetica', 11))],
                [sg.Text('Email*', size=(15,1), font=('Helvetica', 12)), sg.Input(organizador.email, key='-EMAIL-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Nova Senha', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-SENHA-', password_char='*', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('(Deixe em branco para manter a senha atual)', text_color='gray', font=('Helvetica', 9))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('* Campos obrigatórios.', text_color='red', font=('Helvetica', 10))],
            [sg.Text('_' * 50)],
            [sg.Button('Salvar', key='-SALVAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Editar Organizador', [layout], finalize=True, resizable=False, size=(600, 500))

    def criar_janela_detalhes_organizador(self, organizador):
        """Cria a janela de detalhes do organizador"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Detalhes do Organizador', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Frame('Informações Pessoais', [
                [sg.Text('Nome:', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.nome, font=('Helvetica', 12, 'bold'))],
                [sg.Text('CPF:', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.get_cpf_formatado(), font=('Helvetica', 12, 'bold'))],
                [sg.Text('Email:', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.email, font=('Helvetica', 12, 'bold'))],
                [sg.Text('Perfil:', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.perfil, font=('Helvetica', 12, 'bold'))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 30)],
            [sg.Frame('Estatísticas', [
                [sg.Text('Total de Eventos:', size=(20, 1), font=('Helvetica', 12)), sg.Text(str(len(organizador.eventos) if organizador.eventos else 0), font=('Helvetica', 12, 'bold'))],
                [sg.Text('Cadastrado em:', size=(20, 1), font=('Helvetica', 12)), sg.Text('Sistema', font=('Helvetica', 12, 'bold'))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Button('Editar', key='-EDITAR-', size=(10, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Detalhes do Organizador', [layout], finalize=True, resizable=False, size=(600, 500))

    def criar_janela_menu_principal(self):
        """Cria o menu principal com opções CRUD"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Sistema de Gestão de Organizadores', font=('Helvetica', 16, 'bold'), justification='center', expand_x=True)],
            [sg.Text('Gerenciamento completo de organizadores de eventos esportivos', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.VPush()],
            [sg.Text('Menu Principal', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.VPush()],
            [sg.Button('Cadastrar Organizador', key='-CADASTRAR-', size=(22, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('')],
            [sg.Button('Listar Organizadores', key='-LISTAR-', size=(22, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('')],
            [sg.Button('Buscar Organizador', key='-BUSCAR-', size=(22, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.VPush()],
            [sg.Text('_' * 50)],
            [sg.Button('Sair', key='-SAIR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#DC143C'))]
        ]
        return sg.Window('PaceHub - Menu Principal', layout, size=(600, 550), finalize=True, resizable=False)

    # ========== TELAS DE AUTENTICAÇÃO E PERFIL ==========

    def criar_janela_painel_organizador(self, organizador):
        """Cria a janela do painel do organizador"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Painel do Organizador', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Text(f'Bem-vindo, {organizador.nome}!', font=('Helvetica', 16, 'bold'), justification='center', expand_x=True)],
            [sg.Text(f'CPF: {organizador.get_cpf_formatado()}', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.VPush()],
            [sg.Text('Menu Principal', font=('Helvetica', 16, 'bold'), justification='center', expand_x=True)],
            [sg.Text('_' * 40)],
            [sg.Button('Ver Meu Perfil', key='-PERFIL-', size=(18, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('')],
            [sg.Button('Gerenciar Eventos', key='-EVENTOS-', size=(18, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.Text('')],
            [sg.Button('Relatórios', key='-RELATORIOS-', size=(18, 2), font=('Helvetica', 14, 'bold'), button_color=('white', '#696969'))],
            [sg.VPush()],
            [sg.Text('_' * 50)],
            [sg.Button('Sair do Perfil', key='-SAIR_PERFIL-', size=(15, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#DC143C')),
             sg.Button('Sair', key='-SAIR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#DC143C'))]
        ]
        return sg.Window('PaceHub - Painel do Organizador', layout, size=(600, 550), finalize=True, resizable=False)

    def criar_janela_perfil_organizador(self, organizador):
        """Cria a janela de perfil do organizador"""
        layout = [
            [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text('Meu Perfil', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Text('_' * 50)],
            [sg.Frame('Informações Pessoais', [
                [sg.Text('Nome Completo*', size=(15, 1), font=('Helvetica', 12)), sg.Input(organizador.nome, key='-NOME-', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('CPF*', size=(15, 1), font=('Helvetica', 12)), sg.Text(organizador.get_cpf_formatado(), text_color='gray', font=('Helvetica', 11))],
                [sg.Text('Email*', size=(15,1), font=('Helvetica', 12)), sg.Input(organizador.email, key='-EMAIL-', size=(40, 1), font=('Helvetica', 11))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 30)],
            [sg.Frame('Alterar Senha', [
                [sg.Text('Senha Atual', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-SENHA_ATUAL-', password_char='*', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Nova Senha', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-NOVA_SENHA-', password_char='*', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Confirmar Nova Senha', size=(15,1), font=('Helvetica', 12)), sg.Input(key='-CONFIRMAR_SENHA-', password_char='*', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('(Deixe em branco para manter a senha atual)', text_color='gray', font=('Helvetica', 9))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('_' * 30)],
            [sg.Frame('Estatísticas', [
                [sg.Text('Total de Eventos:', size=(20, 1), font=('Helvetica', 12)), sg.Text(str(len(organizador.eventos) if organizador.eventos else 0), font=('Helvetica', 12, 'bold'))],
                [sg.Text('Perfil:', size=(20, 1), font=('Helvetica', 12)), sg.Text(organizador.perfil, font=('Helvetica', 12, 'bold'))],
            ], font=('Helvetica', 12, 'bold'))],
            [sg.Text('* Campos obrigatórios.', text_color='red', font=('Helvetica', 10))],
            [sg.Text('_' * 50)],
            [sg.Button('Salvar Alterações', key='-SALVAR-', size=(18, 1), font=('Helvetica', 12, 'bold'), button_color=('white', '#696969')),
             sg.Button('Voltar', key='-VOLTAR-', size=(8, 1), font=('Helvetica', 10), button_color=('white', '#696969'))]
        ]
        return sg.Window('PaceHub - Meu Perfil', [layout], finalize=True, resizable=False, size=(700, 600))