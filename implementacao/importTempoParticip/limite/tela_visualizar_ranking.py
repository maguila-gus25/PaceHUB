import FreeSimpleGUI as sg
from typing import Optional, Dict, List
from entidade.evento import obter_evento_por_id
from controlador.controlador_ranking import ControladorRanking


def criar_janela_rankings(evento_id: int) -> sg.Window:
    """
    Cria a janela de visualização de rankings de um evento.
    Baseada no arquivo casos-de-uso/gerarRanking.py com dados reais do banco.
    
    Args:
        evento_id: ID do evento
        
    Returns:
        Janela PySimpleGUI configurada
    """
    sg.theme('DarkBlue14')
    
    # Buscar dados do evento
    evento = obter_evento_por_id(evento_id)
    if not evento:
        sg.popup_error(f"Evento com ID {evento_id} não encontrado!")
        return None
    
    # Verificar se tem resultados
    controlador = ControladorRanking()
    if not controlador.verificar_evento_tem_resultados(evento_id):
        sg.popup_error(f"Nenhum resultado importado para o evento '{evento.nome}'!")
        return None
    
    # Obter rankings
    rankings = controlador.obter_rankings_evento(evento_id)
    estatisticas = rankings['estatisticas']
    
    # Criar abas baseadas nas categorias disponíveis
    abas = []
    
    # Aba Geral (sempre presente se tem resultados)
    if estatisticas['total_resultados'] > 0:
        layout_geral = _criar_layout_geral(rankings)
        abas.append(sg.Tab('Geral', layout_geral))
    
    # Abas por categoria
    categorias_disponiveis = controlador.obter_categorias_disponiveis(evento_id)
    
    for categoria in ['Júnior', 'Adulto', 'Master']:
        if categoria in categorias_disponiveis:
            layout_categoria = _criar_layout_categoria(rankings, categoria)
            abas.append(sg.Tab(categoria, layout_categoria))
    
    # Aba PCD (só se tiver atletas PCD)
    if estatisticas['tem_categoria_pcd']:
        layout_pcd = _criar_layout_categoria(rankings, 'PCD')
        abas.append(sg.Tab('PCD', layout_pcd))
    
    # Layout principal
    layout_principal = [
        [sg.Text(f'Rankings - {evento.nome}', font=('Helvetica', 20))],
        [sg.Text(f'Data: {evento.data} | Distância: {evento.distancia} | Total: {estatisticas["total_resultados"]} atletas')],
        [sg.HorizontalSeparator()],
        [sg.TabGroup([abas], expand_x=True, expand_y=True)],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10, 1))]
    ]
    
    return sg.Window(
        f'PaceHub - Rankings - {evento.nome}', 
        layout_principal, 
        size=(1280, 720),  # Proporção 16:9 (1280x720)
        finalize=True, 
        resizable=True
    )


def _criar_layout_geral(rankings: Dict) -> List[List]:
    """
    Cria layout para a aba de classificação geral.
    
    Args:
        rankings: Dicionário com rankings organizados
        
    Returns:
        Layout da aba geral
    """
    layout = []
    
    # Classificação Geral Masculino
    geral_masc = rankings['geral_masculino']
    if geral_masc:
        layout.append([sg.Text('Geral Masculino', font=('Helvetica', 12, 'bold'))])
        
        dados_masc = []
        for resultado in geral_masc:
            dados_masc.append([
                resultado.classificacao_geral,
                resultado.nome_atleta,
                resultado.tempo_final
            ])
        
        layout.append([sg.Table(
            values=dados_masc,
            headings=['Pos.', 'Nome do Atleta', 'Tempo'],
            justification='left',
            expand_x=True,
            num_rows=min(len(dados_masc), 5),
            key='-TABELA_GERAL_MASC-'
        )])
        layout.append([sg.Text('')])
    
    # Classificação Geral Feminino
    geral_fem = rankings['geral_feminino']
    if geral_fem:
        layout.append([sg.Text('Geral Feminino', font=('Helvetica', 12, 'bold'))])
        
        dados_fem = []
        for resultado in geral_fem:
            dados_fem.append([
                resultado.classificacao_geral,
                resultado.nome_atleta,
                resultado.tempo_final
            ])
        
        layout.append([sg.Table(
            values=dados_fem,
            headings=['Pos.', 'Nome do Atleta', 'Tempo'],
            justification='left',
            expand_x=True,
            num_rows=min(len(dados_fem), 5),
            key='-TABELA_GERAL_FEM-'
        )])
    
    return layout


def _criar_layout_categoria(rankings: Dict, categoria: str) -> List[List]:
    """
    Cria layout para uma aba de categoria específica.
    
    Args:
        rankings: Dicionário com rankings organizados
        categoria: Nome da categoria
        
    Returns:
        Layout da aba da categoria
    """
    layout = []
    
    categoria_key = categoria.lower()
    
    # Masculino
    masc_key = f'{categoria_key}_masculino'
    resultados_masc = rankings.get(masc_key, [])
    
    if resultados_masc:
        layout.append([sg.Text(f'{categoria} - Masculino', font=('Helvetica', 12, 'bold'))])
        
        dados_masc = []
        for resultado in resultados_masc:
            dados_masc.append([
                resultado.classificacao_categoria,
                resultado.nome_atleta,
                resultado.tempo_final
            ])
        
        layout.append([sg.Table(
            values=dados_masc,
            headings=['Pos. Cat.', 'Nome do Atleta', 'Tempo'],
            justification='left',
            expand_x=True,
            auto_size_columns=True,
            key=f'-TABELA_{categoria.upper()}_MASC-'
        )])
        layout.append([sg.Text('')])
    
    # Feminino
    fem_key = f'{categoria_key}_feminino'
    resultados_fem = rankings.get(fem_key, [])
    
    if resultados_fem:
        layout.append([sg.Text(f'{categoria} - Feminino', font=('Helvetica', 12, 'bold'))])
        
        dados_fem = []
        for resultado in resultados_fem:
            dados_fem.append([
                resultado.classificacao_categoria,
                resultado.nome_atleta,
                resultado.tempo_final
            ])
        
        layout.append([sg.Table(
            values=dados_fem,
            headings=['Pos. Cat.', 'Nome do Atleta', 'Tempo'],
            justification='left',
            expand_x=True,
            auto_size_columns=True,
            key=f'-TABELA_{categoria.upper()}_FEM-'
        )])
    
    # Se não tem resultados para esta categoria
    if not resultados_masc and not resultados_fem:
        layout.append([sg.Text(f'Nenhum resultado encontrado para a categoria {categoria}.', 
                              font=('Helvetica', 10, 'italic'))])
    
    return layout


def executar_janela_rankings(evento_id: int) -> bool:
    """
    Executa a janela de rankings e retorna se foi exibida com sucesso.
    
    Args:
        evento_id: ID do evento
        
    Returns:
        True se janela foi exibida com sucesso, False caso contrário
    """
    janela = criar_janela_rankings(evento_id)
    
    if not janela:
        return False
    
    while True:
        event, values = janela.read()
        
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
    
    janela.close()
    return True


def mostrar_estatisticas_evento(evento_id: int):
    """
    Mostra estatísticas detalhadas de um evento.
    
    Args:
        evento_id: ID do evento
    """
    controlador = ControladorRanking()
    estatisticas = controlador.obter_estatisticas_evento(evento_id)
    
    if not estatisticas:
        sg.popup_error("Não foi possível obter estatísticas do evento.")
        return
    
    # Formatar estatísticas para exibição
    mensagem = f"Estatísticas do Evento:\n\n"
    mensagem += f"Total de Atletas: {estatisticas['total_resultados']}\n\n"
    
    # Por gênero
    mensagem += "Distribuição por Gênero:\n"
    for genero, count in estatisticas['por_genero'].items():
        mensagem += f"  {genero}: {count} atletas\n"
    
    mensagem += "\nDistribuição por Categoria:\n"
    for categoria, count in estatisticas['por_categoria'].items():
        mensagem += f"  {categoria}: {count} atletas\n"
    
    if estatisticas.get('melhor_tempo'):
        mensagem += f"\nMelhor Tempo: {estatisticas['melhor_tempo']}"
    
    sg.popup_scrolled(mensagem, title="Estatísticas do Evento", size=(400, 300))


def criar_janela_busca_atleta(evento_id: int) -> sg.Window:
    """
    Cria janela para busca de resultado de atleta específico.
    
    Args:
        evento_id: ID do evento
        
    Returns:
        Janela PySimpleGUI configurada
    """
    sg.theme('DarkBlue14')
    
    evento = obter_evento_por_id(evento_id)
    if not evento:
        return None
    
    layout = [
        [sg.Text(f'Buscar Resultado - {evento.nome}', font=('Helvetica', 16))],
        [sg.Text('Digite o CPF do atleta:')],
        [sg.Input(key='-CPF-', size=(20, 1)), sg.Button('Buscar', key='-BUSCAR-')],
        [sg.Text('', key='-RESULTADO-', size=(50, 6))]
    ]
    
    return sg.Window(
        f'Buscar Atleta - {evento.nome}',
        layout,
        size=(400, 200),
        finalize=True
    )


def executar_busca_atleta(evento_id: int) -> bool:
    """
    Executa janela de busca de atleta.
    
    Args:
        evento_id: ID do evento
        
    Returns:
        True se busca foi executada, False caso contrário
    """
    janela = criar_janela_busca_atleta(evento_id)
    
    if not janela:
        return False
    
    controlador = ControladorRanking()
    
    while True:
        event, values = janela.read()
        
        if event in (sg.WIN_CLOSED,):
            break
        
        if event == '-BUSCAR-':
            cpf = values['-CPF-'].strip()
            
            if not cpf:
                janela['-RESULTADO-'].update("Por favor, digite um CPF.")
                continue
            
            resultado_info = controlador.obter_resultado_atleta(evento_id, cpf)
            
            if resultado_info:
                resultado = resultado_info['resultado']
                mensagem = f"Nome: {resultado.nome_atleta}\n"
                mensagem += f"Tempo: {resultado.tempo_final}\n"
                mensagem += f"Categoria: {resultado.categoria}\n"
                
                if resultado_info['posicao_geral']:
                    mensagem += f"Classificação Geral: {resultado_info['posicao_geral']}º\n"
                
                if resultado_info['posicao_categoria']:
                    mensagem += f"Classificação na Categoria: {resultado_info['posicao_categoria']}º"
                
                janela['-RESULTADO-'].update(mensagem)
            else:
                janela['-RESULTADO-'].update("Atleta não encontrado neste evento.")
    
    janela.close()
    return True


if __name__ == "__main__":
    # Teste da janela de rankings
    print("=== Teste da Janela de Rankings ===")
    
    # Testar com evento ID 1 (Meia Maratona de Inverno)
    evento_id_teste = 1
    
    # Verificar se tem resultados
    controlador = ControladorRanking()
    tem_resultados = controlador.verificar_evento_tem_resultados(evento_id_teste)
    
    if tem_resultados:
        print(f"Evento {evento_id_teste} tem resultados. Abrindo janela...")
        sucesso = executar_janela_rankings(evento_id_teste)
        print(f"Janela executada: {'Sim' if sucesso else 'Não'}")
    else:
        print(f"Evento {evento_id_teste} não tem resultados importados.")
        print("Execute primeiro a importação de resultados.")
