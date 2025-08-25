import sqlite3
from sqlite3 import Error
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

class Database:

    #cria o banco de dados
    def __init__(self, name: str) -> None:
        """
        Criação do banco de dados, possui um único atributo nome.
        A estrutura do banco está em databaseControler
        try -> instancia o banco 
        except -> em caso de erro informa o erro
        
        :param name: string
        
        :return None
        """
        self.name = name
        try:
            conn = sqlite3.connect(self.name)
            conn.execute('''
            PRAGMA foreign_keys = ON;
            ''')
            
        except OSError as e:
            print(e)
            print('Erro')
            
    
    #conectando/criando o banco, caso ele não exista
    @staticmethod
    def conect_database(database_name: str) -> object:
        """
        Responsável por criar uma conexão com o banco de dados
        try -> estabelece uma conexão com o banco de dados
        except -> informa o erro em caso de erro na operação anterior
        
        :param database_name: string
        :return conn: object || código erro = D1

        """
        try:
            conn = sqlite3.connect(database_name)
            return conn
        except OSError as e:
            print(e)
            print('Erro na conexão')
            return 'D1'

    #criando a tabela dos produtos, caso não exista
    # model/database.py  (somente trechos das 3 funções)

    @staticmethod
    def create_table_itens(cursor: object) -> bool:
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Itens (
                    IdItens INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nome VARCHAR(30) UNIQUE,
                    Preco REAL,
                    Tipo VARCHAR(30),
                    Descricao VARCHAR(255)
                );
            ''')
            return True
        except OSError as e:
            print(e)
            return 'D2'

    @staticmethod
    def create_table_pedidos(cursor: object) -> bool:
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pedidos (
                    IdPedido   INTEGER PRIMARY KEY AUTOINCREMENT,
                    Status     VARCHAR(30) NOT NULL,
                    Delivery   INTEGER NOT NULL DEFAULT 0,  -- 0/1 no SQLite
                    Endereco   VARCHAR(100),
                    Data       TEXT,                         -- string do input datetime-local
                    ValorTotal REAL NOT NULL DEFAULT 0
                );
            ''')
            return True
        except OSError as e:
            print(e)
            return 'D3'

    @staticmethod
    def create_table_itens_pedidos(cursor: object) -> bool:
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ItensPedidos (
                    Id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    IdPedido INTEGER NOT NULL,
                    IdItem   INTEGER NOT NULL,
                    FOREIGN KEY(IdPedido) REFERENCES Pedidos(IdPedido) ON DELETE CASCADE,
                    FOREIGN KEY(IdItem)   REFERENCES Itens(IdItens)   ON DELETE CASCADE
                );
            ''')
            return True
        except OSError as e:
            print(e)
            return 'D4'



'''
Códigos de Erro

conect_database - D1
create_table_itens - D2
create_table_pedidos - D3
create_table_itens_pedido - D4

'''