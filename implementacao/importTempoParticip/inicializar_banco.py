#!/usr/bin/env python3
"""
Script de inicialização do banco de dados para o sistema de importação de resultados.
Cria as tabelas necessárias e popula com dados de exemplo.
"""

import os
import sys

# Adicionar o diretório pai ao path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from persistencia.resultado_dao import ResultadoDAO
from entidade.evento import Evento, EVENTOS_MOCK


def inicializar_banco(forcar_repopular=False):
    """
    Inicializa o banco de dados criando tabelas e populando com dados de exemplo.
    
    Args:
        forcar_repopular: Se True, repopula eventos mesmo se já existirem
    """
    print("\n=== Inicialização do Banco de Dados ===")
    
    # Criar instância do DAO
    dao = ResultadoDAO()
    
    # Criar tabelas
    print("1. Criando tabelas...")
    sucesso = dao.criar_tabelas()
    if sucesso:
        print("   ✓ Tabelas criadas com sucesso!")
    else:
        print("   ✗ Erro ao criar tabelas!")
        return False
    
    # Verificar se já existem eventos
    eventos_existentes = dao.listar_eventos()
    print(f"2. Verificando eventos no banco...")
    print(f"   Eventos existentes: {len(eventos_existentes)}")
    
    if eventos_existentes and not forcar_repopular:
        print("   ✓ Banco já possui eventos!")
        for evento in eventos_existentes:
            print(f"      - {evento.nome} (ID: {evento.id})")
        return True
    
    # Popular com eventos de exemplo
    print("3. Populando com eventos de exemplo...")
    eventos_salvos = 0
    
    for evento in EVENTOS_MOCK:
        # Criar novo objeto Evento sem ID (para permitir auto-increment)
        evento_novo = Evento(
            id=None,
            nome=evento.nome,
            data=evento.data,
            status=evento.status,
            distancia=evento.distancia
        )
        
        if dao.salvar_evento(evento_novo):
            eventos_salvos += 1
            print(f"   ✓ Evento salvo: {evento_novo.nome} (ID: {evento_novo.id})")
        else:
            print(f"   ✗ Erro ao salvar evento: {evento_novo.nome}")
    
    print(f"\n4. Total: {eventos_salvos} eventos salvos com sucesso!")
    print("   ✓ Inicialização concluída!\n")
    
    return True


def verificar_banco():
    """
    Verifica o estado atual do banco de dados.
    """
    print("=== Verificação do Banco de Dados ===")
    
    dao = ResultadoDAO()
    
    # Listar eventos
    eventos = dao.listar_eventos()
    print(f"Eventos no banco: {len(eventos)}")
    
    for evento in eventos:
        resultados_count = dao.contar_resultados_evento(evento.id)
        print(f"  - {evento.nome}: {resultados_count} resultados")
    
    # Estatísticas gerais
    total_eventos = len(eventos)
    total_resultados = sum(dao.contar_resultados_evento(e.id) for e in eventos)
    
    print(f"\nResumo:")
    print(f"  Total de eventos: {total_eventos}")
    print(f"  Total de resultados: {total_resultados}")


def limpar_banco():
    """
    Limpa todos os dados do banco (mantém apenas as tabelas).
    """
    print("=== Limpeza do Banco de Dados ===")
    
    resposta = input("Tem certeza que deseja limpar TODOS os dados? (digite 'SIM' para confirmar): ")
    
    if resposta != 'SIM':
        print("Operação cancelada.")
        return False
    
    dao = ResultadoDAO()
    
    # Listar eventos para limpar resultados
    eventos = dao.listar_eventos()
    
    total_removidos = 0
    for evento in eventos:
        removidos = dao.limpar_resultados_evento(evento.id)
        total_removidos += removidos
        print(f"  Removidos {removidos} resultados do evento: {evento.nome}")
    
    print(f"\nTotal de resultados removidos: {total_removidos}")
    print("✓ Banco limpo com sucesso!")
    
    return True


def main():
    """
    Função principal do script.
    """
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == 'init':
            inicializar_banco()
        elif comando == 'check':
            verificar_banco()
        elif comando == 'clean':
            limpar_banco()
        else:
            print(f"Comando desconhecido: {comando}")
            print("Comandos disponíveis: init, check, clean")
    else:
        # Menu interativo
        print("=== Script de Inicialização do Banco ===")
        print("1. Inicializar banco (criar tabelas + dados exemplo)")
        print("2. Verificar estado do banco")
        print("3. Limpar banco (remover todos os dados)")
        print("4. Sair")
        
        while True:
            try:
                opcao = input("\nEscolha uma opção (1-4): ").strip()
                
                if opcao == '1':
                    inicializar_banco()
                    break
                elif opcao == '2':
                    verificar_banco()
                    break
                elif opcao == '3':
                    limpar_banco()
                    break
                elif opcao == '4':
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida! Escolha entre 1-4.")
                    
            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário.")
                break
            except Exception as e:
                print(f"Erro: {e}")


if __name__ == "__main__":
    main()
