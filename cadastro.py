import PySimpleGUI as sg

def criar_janela_selecao():
    """Cria a janela inicial para o usuário escolher o perfil."""
    sg.theme('DarkBlue14')
    layout = [
        [sg.Text('Bem-vindo ao PaceHub!', font=('Helvetica', 18))],
        [sg.Text('Por favor, selecione o tipo de perfil que deseja cadastrar:')],
        [sg.Combo(['Atleta', 'Organizador'], key='-PERFIL-', readonly=True, default_value='Atleta')],
        [sg.Button('Avançar', key='-AVANCAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    return sg.Window('PaceHub - Seleção de Perfil', layout, finalize=True)

def criar_janela_cadastro(perfil):
    """Cria a janela de cadastro baseada no perfil escolhido ('Atleta' ou 'Organizador')."""
    sg.theme('DarkBlue14')

    # Campos base, comuns a todos os perfis
    layout_base = [
        [sg.Text(f'Cadastro de {perfil}', font=('Helvetica', 20))],
        [sg.Text('Nome Completo*', size=(15, 1)), sg.Input(key='-NOME-')],
        [sg.Text('CPF*', size=(15, 1)), sg.Input(key='-CPF-')],
    ]

    # Campos específicos para o perfil de Atleta
    if perfil == 'Atleta':
        layout_atleta = [
            [sg.Text('Data de Nascimento*', size=(15,1)), sg.Input(key='-DATA_NASC-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_NASC-', format='%d/%m/%Y')],
            [sg.Text('Gênero*', size=(15,1)), sg.Combo(['Masculino', 'Feminino', 'Outro'], key='-GENERO-')],
            [sg.Text('PCD*', size=(15,1)), 
             sg.Radio('Sim', 'GRUPO_PCD', key='-PCD_SIM-'), 
             sg.Radio('Não', 'GRUPO_PCD', key='-PCD_NAO-', default=True)],
        ]
        layout_base.extend(layout_atleta)

    # --- ALTERAÇÃO PRINCIPAL ---
    # Campos de login (Email/Senha) agora são adicionados para AMBOS os perfis
    layout_login = [
        [sg.Text('Email*', size=(15,1)), sg.Input(key='-EMAIL-')],
        [sg.Text('Senha*', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
    ]
    layout_base.extend(layout_login)

    # Botões e texto final, comuns a todos
    layout_final = [
        [sg.Text('* Todos os campos são obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar', key='-CADASTRAR-', size=(10, 1))],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10, 1))]
    ]
    layout_base.extend(layout_final)

    return sg.Window(f'PaceHub - Cadastro de {perfil}', layout_base, finalize=True)

# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_selecao = criar_janela_selecao()
    perfil_escolhido = None

    while True:
        event, values = janela_selecao.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break
        if event == '-AVANCAR-':
            perfil_escolhido = values['-PERFIL-']
            break
    janela_selecao.close()

    if perfil_escolhido:
        janela_cadastro = criar_janela_cadastro(perfil_escolhido)

        while True:
            event, values = janela_cadastro.read()
            if event in (sg.WIN_CLOSED, '-VOLTAR-'):
                break
            if event == '-CADASTRAR-':
                # Coleta os dados que são comuns a ambos
                dados = f"Cadastro de {perfil_escolhido} realizado com sucesso!\n"
                dados += f"Nome: {values['-NOME-']}\n"
                dados += f"CPF: {values['-CPF-']}\n"
                
                # --- LÓGICA DE COLETA MODIFICADA ---
                # Adiciona o email para ambos, pois agora é um campo comum
                dados += f"Email: {values['-EMAIL-']}\n"

                # Adiciona os dados que são exclusivos do atleta
                if perfil_escolhido == 'Atleta':
                    dados += f"Gênero: {values['-GENERO-']}\n"
                    eh_pcd = values['-PCD_SIM-']
                    dados += f"É PCD: {eh_pcd}\n"

                sg.popup(dados)
                break

        janela_cadastro.close()