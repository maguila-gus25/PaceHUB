import PySimpleGUI as sg

def criar_janela_rankings():
    """
    Cria a janela de rankings de um evento, com abas para cada categoria,
    seguindo as regras de negócio do PaceHub.
    """
    sg.theme('DarkBlue14')

    # --- DADOS DE EXEMPLO (Simulando um resultado de prova) ---

    # Classificação Geral: Top 5 de cada gênero 
    headings_geral = ['Pos.', 'Nome do Atleta', 'Tempo']
    dados_geral_masc = [
        [1, "José Pereira", "02:30:15"],
        [2, "Carlos Souza", "02:32:40"],
        [3, "Marcos Andrade", "02:35:11"],
        [4, "Ricardo Lima", "02:38:22"],
        [5, "Paulo Costa", "02:40:05"],
    ]
    dados_geral_fem = [
        [1, "Maria Santos", "02:55:01"],
        [2, "Juliana Almeida", "02:57:33"],
        [3, "Fernanda Rocha", "02:59:10"],
        [4, "Beatriz Melo", "03:01:45"],
        [5, "Luiza Gonçalves", "03:03:18"],
    ]

    # Classificação por Categoria: Júnior, Adulto e Master 
    headings_categoria = ['Pos. Cat.', 'Nome do Atleta', 'Tempo']
    
    # Categoria Júnior (até 17 anos)
    dados_junior_masc = [[1, "Lucas Ferraz", "00:44:50"]]
    dados_junior_fem = [[1, "Clara Martins", "00:46:20"]]
    
    # Categoria Adulto (18 a 49 anos)
    dados_adulto_masc = [
        [1, "Fernando Gomes", "00:40:15"],
        [2, "Thiago Nunes", "00:41:05"],
    ]
    dados_adulto_fem = [
        [1, "Ana Beatriz", "00:45:10"],
        [2, "Carla Dias", "00:48:30"],
    ]

    # Categoria Master (50 anos ou mais)
    dados_master_masc = [[1, "Roberto Assis", "00:49:55"]]
    dados_master_fem = [[1, "Sônia Braga", "00:55:40"]]

    # --- LAYOUT DAS ABAS ---

    # Aba para a classificação Geral
    layout_geral = [
        [sg.Text('Geral Masculino', font=('Helvetica', 12, 'bold'))],
        [sg.Table(values=dados_geral_masc, headings=headings_geral, justification='left', expand_x=True, num_rows=5)],
        [sg.Text('')],
        [sg.Text('Geral Feminino', font=('Helvetica', 12, 'bold'))],
        [sg.Table(values=dados_geral_fem, headings=headings_geral, justification='left', expand_x=True, num_rows=5)],
    ]

    # Função para criar o layout de uma aba de categoria (Júnior, Adulto, Master)
    def criar_layout_categoria(titulo, dados_masc, dados_fem):
        return [
            [sg.Text(f'{titulo} - Masculino', font=('Helvetica', 12, 'bold'))],
            [sg.Table(values=dados_masc, headings=headings_categoria, justification='left', expand_x=True, auto_size_columns=True)],
            [sg.Text('')],
            [sg.Text(f'{titulo} - Feminino', font=('Helvetica', 12, 'bold'))],
            [sg.Table(values=dados_fem, headings=headings_categoria, justification='left', expand_x=True, auto_size_columns=True)],
        ]

    # --- LAYOUT PRINCIPAL ---

    layout_final = [
        [sg.Text('Rankings - Maratona de Floripa', font=('Helvetica', 20))], # Exemplo de nome de evento
        [sg.TabGroup([[
            sg.Tab('Geral', layout_geral),
            sg.Tab('Júnior', criar_layout_categoria('Júnior', dados_junior_masc, dados_junior_fem)),
            sg.Tab('Adulto', criar_layout_categoria('Adulto', dados_adulto_masc, dados_adulto_fem)),
            sg.Tab('Master', criar_layout_categoria('Master', dados_master_masc, dados_master_fem))
        ]], expand_x=True, expand_y=True)],
        [sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Rankings', layout_final, size=(700, 600), finalize=True, resizable=True)


if __name__ == '__main__':
    janela_rankings = criar_janela_rankings()

    while True:
        event, values = janela_rankings.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
            
    janela_rankings.close()