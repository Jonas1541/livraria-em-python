import sqlite3
import os
import csv
from pathlib import Path
from datetime import datetime

conexao = sqlite3.connect('silence_in_the_library.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        preco FLOAT NOT NULL
    )
''')
conexao.commit()

BACKUP_DIR = Path("backups")
CSV_DIR = Path("csv")

def ensure_directories():
    BACKUP_DIR.mkdir(exist_ok=True)
    CSV_DIR.mkdir(exist_ok=True)

def create_backup():
    ensure_directories()
    backup_file = BACKUP_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    conexao.backup(sqlite3.connect(backup_file))
    print(f"Backup criado: {backup_file}")

def clean_old_backups(max_files=5):
    backups = sorted(BACKUP_DIR.glob("*.db"), key=os.path.getmtime, reverse=True)
    for backup in backups[max_files:]:
        backup.unlink()
        print(f"Backup removido: {backup}")

def create_book(titulo, autor, ano_publicacao, preco):
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))
    conexao.commit()
    create_backup()
    clean_old_backups()
    print("Livro adicionado com sucesso!")

def read_all():
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    if livros:
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Preço: R$ {livro[4]:.2f}")
    else:
        print("Nenhum livro encontrado.")

def update_price(titulo, novo_preco):
    cursor.execute('''
        UPDATE livros SET preco = ? WHERE titulo = ?
    ''', (novo_preco, titulo))
    conexao.commit()
    create_backup()
    clean_old_backups()
    print("Preço atualizado com sucesso!")

def delete_book(titulo):
    cursor.execute('DELETE FROM livros WHERE titulo = ?', (titulo,))
    conexao.commit()
    create_backup()
    clean_old_backups()
    print("Livro removido com sucesso!")

def search_by_author(autor):
    cursor.execute('SELECT * FROM livros WHERE autor = ?', (autor,))
    livros = cursor.fetchall()
    if livros:
        for livro in livros:
            print(f"Título: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Preço: R$ {livro[4]:.2f}")
    else:
        print("Nenhum livro encontrado para esse autor.")

def export_to_csv():
    ensure_directories()
    csv_file = CSV_DIR / f"livros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Título", "Autor", "Ano de Publicação", "Preço"])
        writer.writerows(livros)
    
    print(f"Dados exportados para {csv_file}")

def import_from_csv(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho
        for row in reader:
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (row[1], row[2], int(row[3]), float(row[4])))
        conexao.commit()
        create_backup()
        clean_old_backups()
    print(f"Dados importados de {file_path}")

def menu():
    while True:
        print("\n1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")

        escolha = input("Escolha sua opção: ")

        if escolha == '1':
            titulo = input("Digite o título: ")
            autor = input("Digite o autor: ")
            ano_publicacao = int(input("Digite o ano de publicação: "))
            preco = float(input("Digite o preço: "))
            create_book(titulo, autor, ano_publicacao, preco)
        elif escolha == '2':
            read_all()
        elif escolha == '3':
            titulo = input("Digite o título do livro: ")
            preco = float(input("Digite o novo preço: "))
            update_price(titulo, preco)
        elif escolha == '4':
            titulo = input("Digite o título do livro a remover: ")
            delete_book(titulo)
        elif escolha == '5':
            autor = input("Digite o nome do autor: ")
            search_by_author(autor)
        elif escolha == '6':
            export_to_csv()
        elif escolha == '7':
            file_path = input("Digite o caminho do arquivo CSV: ")
            import_from_csv(file_path)
        elif escolha == '8':
            create_backup()
        elif escolha == '9':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")

menu()

conexao.close()