import PySimpleGUI as sg

def criar_janela_cadastro(perfil): # perfil pode ser "Atleta" ou "Organizador"
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text(f'Cadastro de {perfil}', font=('Helvetica', 20))],
        [sg.Text('Nome Completo', size=(15,1)), sg.Input(key='-NOME-')],
        [sg.Text('CPF', size=(15,1)), sg.Input(key='-CPF-')],
        [sg.Text('Data de Nascimento', size=(15,1)), sg.Input(key='-DATA_NASC-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_NASC-', format='%d/%m/%Y')],
        [sg.Text('Gênero', size=(15,1)), sg.Combo(['Masculino', 'Feminino', 'Outro'], key='-GENERO-')],
        [sg.Text('Email', size=(15,1)), sg.Input(key='-EMAIL-')],
        [sg.Text('Senha', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Text('* Todos os campos são obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar', key='-CADASTRAR-', size=(10,1))],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10,1))]
    ]
    
    # Validação do requisito RNF02 sobre o asterisco
    for row in layout:
        if isinstance(row[0], sg.Text) and row[0].get().endswith('*') == False and row[0].get() not in [f'Cadastro de {perfil}', 'Senha']:
             if len(row[0].get()) < 20 and len(row[0].get()) > 1: # Evitar adicionar em textos grandes
                row[0].update(row[0].get() + ' *')

    return sg.Window(f'PaceHub - Cadastro de {perfil}', layout, finalize=True)

# Bloco principal para executar a janela
if __name__ == '__main__':
    # Simulação de escolha de perfil
    perfil_escolhido = sg.popup_get_text('Qual perfil deseja cadastrar? (Atleta/Organizador)', 'Escolha de Perfil')
    
    if perfil_escolhido in ["Atleta", "Organizador"]:
        janela_cadastro = criar_janela_cadastro(perfil_escolhido)
        
        while True:
            event, values = janela_cadastro.read()
            if event in (sg.WIN_CLOSED, '-VOLTAR-'):
                break
            if event == '-CADASTRAR-':
                sg.popup('Cadastro realizado com sucesso! (Simulação)')
                break
        
        janela_cadastro.close()