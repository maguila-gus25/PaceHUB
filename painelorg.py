import PySimpleGUI as sg

def criar_painel_organizador():
    sg.theme('DarkBlue14')

    # Dados de exemplo
    meus_eventos = [
        ["Meia Maratona de Inverno", "10/08/2025", 1530, "Concluído"],
        ["Corrida Solidária", "30/09/2025", 875, "Inscrições Abertas"],
        ["Maratona de Floripa", "25/10/2025", 450, "Inscrições Abertas"],
    ]
    headings = ['Nome do Evento', 'Data', 'Inscritos', 'Status']

    layout = [
        [sg.Text('Painel do Organizador', font=('Helvetica', 20))],
        [sg.Text('Bem-vindo, [Nome do Organizador]!')],
        [sg.Button('Criar Novo Evento', key='-CRIAR_EVENTO-', size=(20, 2))],
        [sg.HorizontalSeparator()],
        [sg.Text('Meus Eventos', font=('Helvetica', 15))],
        [sg.Table(values=meus_eventos, headings=headings,
                  auto_size_columns=False,
                  justification='left',
                  num_rows=10,
                  key='-TABELA_MEUS_EVENTOS-',
                  row_height=25,
                  expand_x=True)],
        [sg.Button('Ver Inscritos', key='-VER_INSCRITOS-'),
         sg.Button('Importar Resultados', key='-IMPORTAR-'),
         sg.Button('Ver Estatísticas', key='-ESTATISTICAS-')]
    ]

    return sg.Window('PaceHub - Painel do Organizador', layout, size=(700, 450), finalize=True)

# Bloco principal para executar a janela
if __name__ == '__main__':
    janela_organizador = criar_painel_organizador()
    
    while True:
        event, values = janela_organizador.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-CRIAR_EVENTO-':
            sg.popup('Abrindo tela de criação de evento...')
        
        # Valida se um evento foi selecionado para as outras ações
        if event in ['-VER_INSCRITOS-', '-IMPORTAR-', '-ESTATISTICAS-']:
            if not values['-TABELA_MEUS_EVENTOS-']:
                sg.popup_error('Por favor, selecione um evento na tabela.')
            else:
                sg.popup(f'Ação "{event}" para o evento selecionado.')

    janela_organizador.close()