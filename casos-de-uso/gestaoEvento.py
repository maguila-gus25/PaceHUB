import PySimpleGUI as sg

def criar_janela_gestao_evento(dados_evento=None):
    """
    Cria uma janela para gestão completa de eventos de corrida (CRUD + casos de uso estendidos).
    Se dados_evento for fornecido, preenche os campos para edição.
    """
    sg.theme('DarkBlue14')
    
    # Se dados_evento for fornecido, é modo edição
    modo_edicao = dados_evento is not None
    
    # Dados padrão para modo criação
    dados_padrao = {
        'nome': '',
        'data': '',
        'distancia': '',
        'local': '',
        'horas_corte': '',
        'minutos_corte': '',
        'data_cancelamento': ''
    }
    
    # Se for modo edição, usa os dados fornecidos
    if modo_edicao:
        dados_padrao.update(dados_evento)
    
    layout = [
        [sg.Text('Gestão de Evento de Corrida', font=('Helvetica', 20))],
        [sg.HorizontalSeparator()],
        
        # --- INFORMAÇÕES BÁSICAS DO EVENTO ---
        [sg.Text('Informações do Evento', font=('Helvetica', 15))],
        [sg.Text('Nome do Evento*', size=(25,1)), sg.Input(dados_padrao['nome'], key='-NOME_EVENTO-', size=(40,1))],
        [sg.Text('Data do Evento*', size=(25,1)), sg.Input(dados_padrao['data'], key='-DATA_EVENTO-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_EVENTO-', format='%d/%m/%Y')],
        [sg.Text('Distância (km)*', size=(25,1)), sg.Combo(['5k', '10k', '21k', '42k'], default_value=dados_padrao['distancia'], key='-DISTANCIA-', readonly=True)],
        [sg.Text('Local de Largada*', size=(25,1)), sg.Input(dados_padrao['local'], key='-LOCAL-', size=(40,1))],
        [sg.Text('Tempo de Corte*', size=(25,1)),
         sg.Input(dados_padrao['horas_corte'], key='-HORAS-', size=(4,1)), sg.Text('horas e'),
         sg.Input(dados_padrao['minutos_corte'], key='-MINUTOS-', size=(4,1)), sg.Text('minutos')],
        [sg.Text('Data Limite para Cancelamento*', size=(25,1)), sg.Input(dados_padrao['data_cancelamento'], key='-DATA_CANCEL-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_CANCEL-', format='%d/%m/%Y')],
        
        [sg.HorizontalSeparator()],
        
        # --- BOTÕES CRUD ---
        [sg.Text('Ações do Evento', font=('Helvetica', 15))],
        [sg.Button('Criar Novo Evento', key='-CRIAR-', size=(15,1), visible=not modo_edicao),
         sg.Button('Atualizar Evento', key='-ATUALIZAR-', size=(15,1), visible=modo_edicao),
         sg.Button('Excluir Evento', key='-EXCLUIR-', size=(15,1), visible=modo_edicao),
         sg.Button('Limpar Campos', key='-LIMPAR-', size=(15,1))],
        
        [sg.HorizontalSeparator()],
        
        # --- CASOS DE USO ESTENDIDOS (UC08 extends) ---
        [sg.Text('Gestão Avançada do Evento', font=('Helvetica', 15))],
        [sg.Text('Use os botões abaixo para gerenciar aspectos específicos do evento:')],
        
        # Botões organizados em duas colunas
        [sg.Column([
            [sg.Button('Cadastrar Kits de Corrida', key='-CADASTRAR_KITS-', size=(25,2))],
            [sg.Button('Gerenciar Entrega de Kits', key='-GERENCIAR_KITS-', size=(25,2))]
        ]), sg.VSeperator(), sg.Column([
            [sg.Button('Importar Tempos de Participantes', key='-IMPORTAR_TEMPOS-', size=(25,2))],
            [sg.Button('Publicar Resultados da Corrida', key='-PUBLICAR_RESULTADOS-', size=(25,2))]
        ])],
        
        [sg.HorizontalSeparator()],
        
        # --- BOTÕES DE NAVEGAÇÃO ---
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10,1))]
    ]

    return sg.Window('PaceHub - Gestão de Evento de Corrida', layout, finalize=True, resizable=True)


# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    # Simula dados de um evento para teste (modo edição)
    dados_teste = {
        'nome': 'Meia Maratona de Inverno',
        'data': '10/08/2025',
        'distancia': '21k',
        'local': 'Parque Ibirapuera',
        'horas_corte': '3',
        'minutos_corte': '30',
        'data_cancelamento': '05/08/2025'
    }
    
    # Para testar modo criação, comente a linha abaixo e descomente a próxima
    janela_gestao = criar_janela_gestao_evento(dados_teste)  # Modo edição
    # janela_gestao = criar_janela_gestao_evento()  # Modo criação

    while True:
        event, values = janela_gestao.read()
        
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
            
        # --- AÇÕES CRUD ---
        if event == '-CRIAR-':
            # Validação dos campos obrigatórios
            campos_obrigatorios = ['-NOME_EVENTO-', '-DATA_EVENTO-', '-DISTANCIA-', '-LOCAL-', '-HORAS-', '-MINUTOS-', '-DATA_CANCEL-']
            campos_vazios = [campo for campo in campos_obrigatorios if not values[campo]]
            
            if campos_vazios:
                sg.popup_error('Por favor, preencha todos os campos obrigatórios.')
                continue
                
            sg.popup('Evento criado com sucesso!')
            break
            
        elif event == '-ATUALIZAR-':
            sg.popup('Evento atualizado com sucesso!')
            break
            
        elif event == '-EXCLUIR-':
            if sg.popup_yes_no('Tem certeza que deseja excluir este evento?') == 'Yes':
                sg.popup('Evento excluído com sucesso!')
                break
                
        elif event == '-LIMPAR-':
            # Limpa todos os campos
            campos_para_limpar = ['-NOME_EVENTO-', '-DATA_EVENTO-', '-DISTANCIA-', '-LOCAL-', '-HORAS-', '-MINUTOS-', '-DATA_CANCEL-']
            for campo in campos_para_limpar:
                janela_gestao[campo].update('')
            sg.popup('Campos limpos!')
        
        # --- CASOS DE USO ESTENDIDOS ---
        elif event == '-CADASTRAR_KITS-':
            sg.popup('Abrindo tela de cadastro de kits...')
            # Aqui você chamaria: import cadastroKits; cadastroKits.criar_janela_cadastro_kit()
            
        elif event == '-GERENCIAR_KITS-':
            sg.popup('Abrindo tela de gerenciamento de entrega de kits...')
            # Aqui você chamaria: import gerenciaKits; gerenciaKits.criar_janela_gerenciar_kits()
            
        elif event == '-IMPORTAR_TEMPOS-':
            sg.popup('Abrindo tela de importação de tempos...')
            # Aqui você chamaria: import importaResulta; importaResulta.criar_janela_importar_resultados()
            
        elif event == '-PUBLICAR_RESULTADOS-':
            sg.popup('Resultados da corrida publicados com sucesso!')

    janela_gestao.close()
