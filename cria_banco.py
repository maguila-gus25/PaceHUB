import sqlite3

conexao = sqlite3.connect('banco.db')

cursor = conexao.cursor()

sql_comando = """
    CREATE TABLE IF NOT EXISTS usuarios (
        cpf TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        perfil TEXT NOT NULL,
        data_nascimento TEXT,
        genero TEXT,
        pcd INTEGER
    );
    """

try:
    cursor.execute(sql_comando)
    print('Tabela ""usuarios" criada com sucesso (ou já existia).!')
except Exception as e:
    print(e)

conexao.close()