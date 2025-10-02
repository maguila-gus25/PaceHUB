#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema CRUD está funcionando
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def testar_imports():
    """Testa se todos os imports estão funcionando"""
    try:
        print("🔍 Testando imports...")
        
        # Teste DAO
        from persistencia.organizador_dao import OrganizadorDAO
        print("✅ OrganizadorDAO importado com sucesso")
        
        # Teste Entidade
        from entidade.organizador import Organizador
        print("✅ Organizador importado com sucesso")
        
        # Teste Controlador
        from controle.controlador_organizador import ControladorOrganizador
        print("✅ ControladorOrganizador importado com sucesso")
        
        # Teste Sistema
        from controle.controlador_sistema import ControladorSistema
        print("✅ ControladorSistema importado com sucesso")
        
        # Teste Tela
        from limite.tela_sistema import TelaSistema
        print("✅ TelaSistema importado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        return False

def testar_dao():
    """Testa funcionalidades do DAO"""
    try:
        print("\n🔍 Testando DAO...")
        
        from persistencia.organizador_dao import OrganizadorDAO
        dao = OrganizadorDAO()
        
        # Teste contagem
        total = dao.contar_organizadores()
        print(f"✅ Total de organizadores: {total}")
        
        # Teste listagem
        organizadores = dao.listar_todos()
        print(f"✅ Listagem retornou {len(organizadores)} organizadores")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no DAO: {e}")
        return False

def testar_entidade():
    """Testa funcionalidades da entidade"""
    try:
        print("\n🔍 Testando Entidade...")
        
        from entidade.organizador import Organizador
        
        # Criar organizador de teste
        org = Organizador("João Silva", "12345678901", "joao@teste.com")
        
        # Teste métodos
        cpf_formatado = org.get_cpf_formatado()
        print(f"✅ CPF formatado: {cpf_formatado}")
        
        dados_dict = org.to_dict()
        print(f"✅ Dados em dict: {dados_dict}")
        
        # Teste atualização
        org.atualizar_dados(nome="João Silva Santos", email="joao.santos@teste.com")
        print(f"✅ Dados atualizados: {org.nome}, {org.email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na Entidade: {e}")
        return False

def testar_controlador():
    """Testa funcionalidades do controlador"""
    try:
        print("\n🔍 Testando Controlador...")
        
        from controle.controlador_organizador import ControladorOrganizador
        from limite.tela_sistema import TelaSistema
        
        tela = TelaSistema()
        controlador = ControladorOrganizador(tela)
        
        # Teste métodos auxiliares
        total = controlador.contar_organizadores()
        print(f"✅ Total via controlador: {total}")
        
        organizadores = controlador.listar_organizadores()
        print(f"✅ Lista via controlador: {len(organizadores)} organizadores")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Controlador: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do sistema CRUD de Organizadores")
    print("=" * 60)
    
    testes = [
        ("Imports", testar_imports),
        ("DAO", testar_dao),
        ("Entidade", testar_entidade),
        ("Controlador", testar_controlador)
    ]
    
    sucessos = 0
    total = len(testes)
    
    for nome, teste in testes:
        if teste():
            sucessos += 1
        print()
    
    print("=" * 60)
    print(f"📊 Resultado: {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("🎉 Todos os testes passaram! Sistema funcionando corretamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
