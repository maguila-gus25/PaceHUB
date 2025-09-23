## Cadastro de Organizador — PaceHub

Este módulo implementa o caso de uso de cadastro de organizadores na plataforma PaceHub, utilizando arquitetura MVC em português (entidade, controle, limite) e persistência local com SQLite3.

### Estrutura
```
implementacao/cadastroOrganizador/
├── entidade/
│   ├── usuario.py              # Entidade base
│   ├── organizador.py          # Entidade Organizadora (herda de Usuario)
│   └── evento.py               # Entidade Evento (apoio)
├── persistencia/
│   └── organizador_dao.py      # DAO (SQLite3) para organizadores
├── controle/
│   ├── controlador_organizador.py  # Regras de cadastro + validações
│   └── controlador_sistema.py      # Orquestra fluxo e telas
├── limite/
│   ├── tela_principal.py       # Tela inicial (login simulado)
│   └── tela_organizador.py     # Tela de cadastro do organizador
├── banco.db                    # Banco SQLite (gerado automaticamente)
└── main.py                     # Ponto de entrada do módulo
```

### Requisitos
- Python 3.10+
- Bibliotecas:
  - PySimpleGUI
  - bcrypt

Instale as dependências na raiz do repositório:
```bash
pip install -r requirements.txt
```

### Como executar
A partir da raiz do repositório:
```bash
python implementacao/cadastroOrganizador/main.py
```
Ao iniciar, a tela principal será exibida. Use o botão “Cadastrar como Organizador” para abrir a tela de cadastro.

### Banco de dados (SQLite3)
- O arquivo `banco.db` é criado na primeira execução (se não existir) na pasta `cadastroOrganizador`.
- Tabela: `organizadores (id, nome, cpf, email, senha_hash)`
- O CPF é armazenado apenas com dígitos e possui restrição UNIQUE.

### Regras e validações
- Nome completo: pelo menos nome e sobrenome.
- Email: formato válido.
- CPF: validação dos dígitos verificadores e rejeição de sequências repetidas.
- Senha: armazenada como hash `bcrypt`.
- CPF duplicado: cadastro é bloqueado.

### Fluxo resumido
1. `main.py` inicia `ControladorSistema` e exibe `tela_principal`.
2. Usuário clica “Cadastrar como Organizador” → abre `tela_organizador`.
3. `ControladorOrganizador` valida dados, gera hash, consulta `OrganizadorDAO` e persiste no SQLite.
4. Exibe popup de sucesso/erro conforme resultado.

### Manutenção
- Camadas separadas por responsabilidade (MVC):
  - Entidades em `entidade/`
  - Acesso a dados em `persistencia/`
  - Regras e orquestração em `controle/`
  - Interface em `limite/`
- Evite importar de camadas superiores para inferiores (ex.: telas não devem acessar DAO diretamente).

### Referência
Estrutura inspirada no repositório do colega para cadastro de atletas: [PaceHub (ldavila43)](https://github.com/ldavila43/PaceHub)

### Troubleshooting
- Se a UI não abrir: confirme dependências instaladas e versão do Python.
- Erro de import: execute a partir da raiz do projeto, não de dentro da pasta do módulo.
- Erro de UNIQUE no CPF: o CPF (apenas dígitos) já existe no banco; utilize outro para teste.
