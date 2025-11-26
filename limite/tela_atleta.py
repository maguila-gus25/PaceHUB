import FreeSimpleGUI as sg

class TelaAtleta:
    def __init__(self):
        pass

    def exibir_painel(self, nome_atleta: str, dados_eventos):
        sg.theme('DarkBlue14')

        cabecalhos = ['Nome do Evento', 'Data', 'Distância', 'Status']

        layout_eventos = [
            [sg.Text('Eventos Disponíveis', font=('Helvetica', 18))],
            [sg.Table(
                values=dados_eventos,
                headings=cabecalhos,
                key='-TABELA_EVENTOS-',
                auto_size_columns=False,
                col_widths=[25, 10, 8, 15],
                justification='left',
                num_rows=10,
                enable_events=True,
                display_row_numbers=False,
                expand_x=True
            )],
            [sg.Button('Inscrever-se no Evento', key='-INSCREVER_EVENTO-')]
        ]

        layout = [
            [sg.Text('Painel do Atleta', font=('Helvetica', 25, 'bold'))],
            [sg.Text(f'Bem-vindo, {nome_atleta}!', font=('Helvetica', 14), key='-TEXTO_BEM_VINDO-')],
            [sg.Button('Editar Informações', key='-EDITAR_INFOS-', size=(20, 2), pad=((0,0), (10, 20)))],
            [sg.HSeparator()],
            [sg.Frame('', layout_eventos, background_color=sg.theme_background_color(), border_width=0)],
            [sg.Button('Apagar Conta', key='-APAGAR_CONTA-', size=(20, 2), pad=((0, 0), (10, 20)))],
            [sg.Push(), sg.Button('Sair (Logout)', key='-SAIR-')]
        ]

        return sg.Window('PaceHub - Painel do Atelta', layout, finalize=True, size=(800, 600))