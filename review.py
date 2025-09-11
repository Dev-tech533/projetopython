import sqlite3
import os

# --- NOME DO ARQUIVO DO BANCO DE DADOS ---
DB_FILE = "book_reviews.db"

def create_database():
    if os.path.exists(DB_FILE):
        print(f"O banco de dados '{DB_FILE}' já existe. Nenhuma ação foi tomada.")
        return

    conn = None 
    try:
       
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print(f"Banco de dados '{DB_FILE}' criado com sucesso.")

    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        print("Tabela 'users' criada com sucesso.")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL,
                author TEXT NOT NULL,
                rating INTEGER NOT NULL,
                review_text TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        print("Tabela 'reviews' criada com sucesso.")

        users_to_insert = [
            ('admin', 'admin123'),
            ('leitor', 'senha456'),
            ('ana', 'livros789')
        ]
        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users_to_insert)
        print("Dados de exemplo inseridos na tabela 'users'.")

      
        reviews_to_insert = [
            ('O Senhor dos Anéis', 'J.R.R. Tolkien', 5, 'Uma obra-prima da fantasia.', 2),
            ('Duna', 'Frank Herbert', 5, 'Ficção científica no seu melhor.', 1),
            ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 4, 'Emocionante e reflexivo.', 3),
            ('1984', 'George Orwell', 5, 'Um livro assustadoramente atual.', 2)
        ]
        cursor.executemany("""
            INSERT INTO reviews (book_title, author, rating, review_text, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, reviews_to_insert)
        print("Dados de exemplo inseridos na tabela 'reviews'.")

        # 6. Salva (commit) as alterações no banco de dados
        conn.commit()
        print("\n[SUCESSO] O banco de dados foi criado e populado com sucesso!")

    except sqlite3.Error as e:
        # Tratamento de exceção, como visto no PDF "TEMA_3"
        print(f"[ERRO] Ocorreu um erro com o banco de dados: {e}")
        # Se der erro, desfaz quaisquer alterações
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    create_database()
