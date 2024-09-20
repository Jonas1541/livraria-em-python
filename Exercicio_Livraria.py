import sqlite3

# Conectar ao banco de dados (ou criar um novo arquivo .db)
conexao = sqlite3.connect('silence_in_the_library.db')

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

print("Conexão estabelecida com sucesso!")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        preco FLOAT NOT NULL
    )
''')

# Salvar (commit) as mudanças
conexao.commit()

def create_book(titulo, autor, ano_publicacao, preco):
    cursor.execute('''
    INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)
''', (titulo, autor, ano_publicacao, preco))
    conexao.commit()
    print("Dados inseridos com sucesso!")
    
def read_all():
    cursor.execute('''
    SELECT * FROM livros
    ''')
    
    livros = cursor.fetchall()

    if livros:
        print("Lista de livros:")
        for livro in livros:
            id_livro, titulo, autor, ano_publicacao, preco = livro
            print(f"Título: {titulo}")
            print(f"Autor: {autor}")
            print(f"Ano de Publicação: {ano_publicacao}")
            print(f"Preço: R$ {preco:.2f}")
            print("-" * 30)
    else:
        print("Nenhum livro encontrado.")
    
def update_price(titulo, novo_preco):
    cursor.execute('''
    UPDATE livros SET preco = ? WHERE titulo = ?
    ''', (novo_preco, titulo)
    )
    conexao.commit()
    
def delete_book(titulo):
    cursor.execute('''
    DELETE FROM livros WHERE titulo = ?
    ''', (titulo,)
    )
    conexao.commit()
    
def menu():
    while True:
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Sair")

        n = int(input("Escolha sua opção: "))
        
        if n == 1:
            titulo = input("Digite o título: ")
            autor = input("Digite o autor: ")
            ano_publicacao = input("Digite o ano de publicação: ")
            preco = input("Digite o preço: ")
            create_book(titulo, autor, ano_publicacao, preco)
        elif n == 2:
            read_all()
        elif n == 3:
            titulo = input("Digite o título do livro que você quer mudar o preço: ")
            preco = input("Digite o novo preço: ")
            update_price(titulo, preco)
        elif n == 4:
            titulo = input("Digite o título do livro que você quer apagar: ")
            delete_book(titulo)
        elif n == 5:
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")
        
menu()