import sqlite3
from datetime import datetime


STATUS_PENDENTE = 1
STATUS_PAGA = 3


def limpar_tabelas(cursor):
    """Limpa as tabelas na ordem correta (respeitando chaves estrangeiras)."""
    print("Limpando tabelas existentes...")
    try:
        # --- CORREÇÃO AQUI ---
        cursor.execute("DELETE FROM inscricoes;")  # Trocado "Inscricao" por "inscricoes"

        cursor.execute("DELETE FROM KitsDeCorrida;")
        cursor.execute("DELETE FROM Eventos;")
        cursor.execute("DELETE FROM usuarios;")
        print("Tabelas limpas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao limpar tabelas: {e}")
        raise


def popular_usuarios(cursor):
    """Popula a tabela 'usuarios' com seus dados."""
    dados_usuarios = [
        ('12671115938', 'Lucas Dutra de Ávila', 'lucas@gmail.com',
         '$2b$12$UG3pOfSFPWBlC8..bQJj/.KNJpf5Gz4x/5UL1Z3iPfXWN159oewbe', '0', None, None, None),
        ('90869210009', 'pedro', 'pedro@gmail.com', '$2b$12$Uam7cGVgCZwE7IsdxDTRBOxK8hmPvnlBJNTSnwKjwhKgrWS6AtqAa', '1',
         '1990-06-21', 'Masculino', 0),
        ('93061326030', 'Ruan', 'ruan@gmail.com', '$2b$12$8HzUdli/sypVopzMXe7Qjupq81iXJyzebn3eRAtksNslKfzE0DBOO', '1',
         '1980-08-05', 'Masculino', 0),
        ('64590032031', 'Gustavo', 'gustavo@gmail.com', '$2b$12$YiZcTjzXzQfLOa/DUCxk0uZGhSV8RJwrxmO4lQwM.0OJRtgY68UvK',
         '1', '2010-12-30', 'Masculino', 0)
    ]

    sql = """
    INSERT INTO usuarios 
    (cpf, nome, email, senha_hash, perfil, data_nascimento, genero, pcd)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """

    cursor.executemany(sql, dados_usuarios)
    print(f"{cursor.rowcount} usuários inseridos.")


def popular_eventos(cursor):
    """Popula a tabela 'Eventos' com seus dados."""
    dados_eventos = [
        (1, 'corrida oficial de teste', '16/12/2025', 5, 'Av. Beira Mar Norte', '6:0', '12/11/2025', '12671115938'),
        (2, 'corrida numero 2', '30/01/2026', 10, 'Rua', '6:0', '21/11/2025', '12671115938'),
        (3, 'evento para teste 3', '12/08/2026', 42, 'Rua 3', '6:0', '24/12/2025', '12671115938')
    ]

    sql = """
    INSERT INTO Eventos
    (id, nome, data, distancia, local_largada, tempo_corte, data_limite_cred, organizador_cpf)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """

    cursor.executemany(sql, dados_eventos)
    print(f"{cursor.rowcount} eventos inseridos.")


def popular_kits(cursor):
    """Popula a tabela 'KitsDeCorrida' com seus dados."""
    dados_kits = [
        (1, 'kit de teste', 'este kit contem:\n1 camiseta\n1 garrafa', 15.0, 1),
        (2, 'kit de teste casal', 'Este kit contem:\n2 camisetas', 25.0, 1),
        (3, 'sdasfr', 'asfdd', 45.0, 2),
        (4, 'sqrgherthb', '12341', 90.0, 2),
        (5, 'e235rfdc', '12323', 67.0, 2),
        (6, 's3er', '2ewrefd', 23.0, 3),
        (7, '12312', '41324dsfd', 12.0, 3)
    ]

    sql = """
    INSERT INTO KitsDeCorrida
    (id, nome, descricao, valor, evento_id)
    VALUES (?, ?, ?, ?, ?);
    """

    cursor.executemany(sql, dados_kits)
    print(f"{cursor.rowcount} kits inseridos.")


def popular_inscricoes(cursor):
    """Popula a tabela 'inscricoes' com dados de teste."""

    data_agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dados_inscricoes = [
        (data_agora, 0, STATUS_PAGA, '90869210009', 1, 1),
        (data_agora, 1, STATUS_PAGA, '93061326030', 1, 2),
        (data_agora, 0, STATUS_PENDENTE, '64590032031', 2, 3),
        (data_agora, 0, STATUS_PAGA, '90869210009', 3, 6)
    ]

    # --- CORREÇÃO AQUI ---
    sql = """
    INSERT INTO inscricoes 
    (data_inscricao, kit_entregue, status, atleta_cpf, evento_id, kit_id)
    VALUES (?, ?, ?, ?, ?, ?);
    """

    cursor.executemany(sql, dados_inscricoes)
    print(f"{cursor.rowcount} inscrições inseridas.")


def popular_banco():
    conexao = None
    try:
        conexao = sqlite3.connect('banco.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        limpar_tabelas(cursor)
        popular_usuarios(cursor)
        popular_eventos(cursor)
        popular_kits(cursor)
        popular_inscricoes(cursor)

        conexao.commit()
        print("\n--- BANCO POPULADO COM SUCESSO! ---")

    except sqlite3.Error as e:
        print(f"\n--- OCORREU UM ERRO ---")
        print(f"Erro: {e}")
        if conexao:
            print("Revertendo transações (rollback)...")
            conexao.rollback()
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    popular_banco()