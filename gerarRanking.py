import PySimpleGUI as sg

def criar_janela_rankings():
    sg.theme('DarkBlue14')

    dados_geral = [
        [1, "José Pereira", "02:30:15"],
        [2, "Carlos Souza", "02:32:40"],
    ]
    headings_geral = ['Posição', 'Nome do Atleta', 'Tempo']
    
    dados_categoria = [
        [1, "Ana Beatriz", "00:45:10", "Adulto"],
        [2, "Clara Martins", "00:46:20", "Júnior"],
    ]
    headings_categoria = ['Posição', 'Nome do Atleta', 'Tempo', 'Categoria']

    layout_geral = [[sg.Table(values=dados_geral, headings=headings_geral, justification='left', expand_x=True)]]
    layout_categoria = [[sg.Table(values=dados_categoria, headings=headings_categoria, justification='left', expand_x=True)]]

    layout = [
        [sg.Text('Rankings - [Nome do Evento]', font=('Helvetica', 20))],
        [sg.TabGroup([[
            sg.Tab('Geral', layout_geral),
            sg.Tab('Por Categoria', layout_categoria)
        ]])],
        [sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Rankings', layout, finalize=True)

if __name__ == '__main__':
    janela_rankings = criar_janela_rankings()

    while True:
        event, values = janela_rankings.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
            
    janela_rankings.close()