import PySimpleGUI as sg

def criar_janela_visualizar_inscritos():
    sg.theme('DarkBlue14')

    dados_inscritos = [
        ["João da Silva", "123.456.789-00", "Masculino", "Pendente"],
        ["Maria Oliveira", "987.654.321-00", "Feminino", "Entregue"],
    ]
    headings = ['Nome do Atleta', 'CPF', 'Gênero', 'Status do Kit']

    layout = [
        [sg.Text('Lista de Inscritos - [Nome do Evento]', font=('Helvetica', 20))],
        [sg.Table(values=dados_inscritos, headings=headings,
                  auto_size_columns=False,
                  justification='left',
                  num_rows=15,
                  key='-TABELA_INSCRITOS-',
                  row_height=25,
                  expand_x=True)],
        [sg.Button('Exportar Lista (.csv)', key='-EXPORTAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Visualizar Inscritos', layout, size=(700, 500), finalize=True)

if __name__ == '__main__':
    janela_visualizar_inscritos = criar_janela_visualizar_inscritos()

    while True:
        event, values = janela_visualizar_inscritos.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-EXPORTAR-':
            sg.popup('Lista exportada com sucesso!')

    janela_visualizar_inscritos.close()