import FreeSimpleGUI as sg


class TelaCadastro:

    def __init__(self):
        pass

    def exibir_janela_cadastro(self, perfil: str):
        sg.theme('DarkBlue14')

        frame_dados_layout = [
            [sg.Text("Nome Completo*", size=(15, 1)), sg.Input(key='-NOME-')],
            [sg.Text("CPF*", size=(15, 1)), sg.Input(key='-CPF-')],
        ]

        if perfil == 'Atleta':
            frame_dados_layout.extend([
                [sg.Text("Data de Nascimento*", size=(15, 1)), sg.Input(key='-DATA_NASC-'), sg.Text("(dd/mm/aaaa)")],
                [sg.Text("Gênero*", size=(15, 1)),
                 sg.Combo(['Masculino', 'Feminino', 'Outro'], key='-GENERO-', readonly=True)],
                [sg.Text("PCD*", size=(15, 1)),
                 sg.Radio("Sim", "PCD", key='-PCD_SIM-'),
                 sg.Radio("Não", "PCD", key='-PCD_NAO-', default=True)]
            ])

        frame_dados_layout.extend([
            [sg.Text("Email*", size=(15, 1)), sg.Input(key='-EMAIL-')],
            [sg.Text("Senha*", size=(15, 1)), sg.Input(key='-SENHA-', password_char='*')],
        ])

        layout = [
            [sg.Text(f"Cadastro de {perfil}", font=("Helvetica", 20))],
            [sg.Frame("Dados Pessoais", frame_dados_layout)],
            [sg.Button("Voltar", key='-VOLTAR-'), sg.Push(), sg.Button("Cadastrar", key='-CADASTRAR-')]
        ]

        janela = sg.Window(f"PaceHub - Cadastro de {perfil}", layout, modal=True)

        evento, valores = janela.read()
        janela.close()

        if evento == sg.WIN_CLOSED:
            return None, None

        return evento, valores

    def exibir_janela_edicao(self, nome, email):
        sg.theme('DarkBlue14')

        frame_dados_layout = [
            [sg.Text("Nome Completo*", size=(15, 1)), sg.Input(key='-NOME-', default_text=nome)]
        ]
        frame_dados_layout.extend([
            [sg.Text("Email*", size=(15, 1)), sg.Input(key='-EMAIL-', default_text=email)],
            [sg.Text("Nova Senha", size=(15, 1)), sg.Input(key='-SENHA-', password_char='*')],
            [sg.Text("(Deixe a senha em branco para não alterar)", font=("Helvetica", 8), text_color='yellow')]
        ])

        layout = [
            [sg.Text(f"Edição de Perfil", font=("Helvetica", 20))],
            [sg.Frame("Dados Pessoais", frame_dados_layout)],
            [sg.Button("Voltar", key='-VOLTAR-'), sg.Push(), sg.Button("Atualizar", key='-ATUALIZAR-')]
        ]

        janela = sg.Window(f"PaceHub - Edicao de Perfil", layout, modal=True)

        evento, valores = janela.read()
        janela.close()

        if evento == sg.WIN_CLOSED:
            return None, None

        return evento, valores

    def exibir_janela_edicao_organizador(self, nome: str, email: str):
        sg.theme('DarkBlue14')

        frame_dados_layout = [
            [sg.Text("Nome Completo*", size=(15, 1)), sg.Input(key='-NOME-', default_text=nome)],
            [sg.Text("Email*", size=(15, 1)), sg.Input(key='-EMAIL-', default_text=email)],
            [sg.Text("Nova Senha", size=(15, 1)), sg.Input(key='-SENHA-', password_char='*')],
            [sg.Text("(Deixe a senha em branco para não alterar)", font=("Helvetica", 8), text_color='yellow')]
        ]

        layout = [
            [sg.Text("Edição de Perfil - Organizador", font=("Helvetica", 20))],
            [sg.Frame("Dados Pessoais", frame_dados_layout)],
            [sg.Button("Voltar", key='-VOLTAR-'), sg.Push(), sg.Button("Atualizar", key='-ATUALIZAR-')]
        ]

        janela = sg.Window("PaceHub - Edição de Perfil do Organizador", layout, modal=True)

        evento, valores = janela.read()
        janela.close()

        if evento == sg.WIN_CLOSED:
            return None, None

        return evento, valores