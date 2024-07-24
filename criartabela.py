import pyodbc

def create_connection():
    server = r'LAPTOP-R3DK1NKD\SQLEXPRESS'
    database = 'SistemaGerenciamento'
    username = 'Teste_API'
    password = '123456'

    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return conn


def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE Header (
        ID INT PRIMARY KEY IDENTITY(1,1),
        Name NVARCHAR(29),
        Date NVARCHAR(8),
        Lote NVARCHAR(8),
        RecordCount INT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Lines (
        ID INT PRIMARY KEY IDENTITY(1,1),
        LineIdentifier NVARCHAR(1),
        LineNumber NVARCHAR(6),
        CardNumber NVARCHAR(19),
        HeaderID INT FOREIGN KEY REFERENCES Header(ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Footer (
        ID INT PRIMARY KEY IDENTITY(1,1),
        Lote NVARCHAR(8),
        RecordCount INT,
        HeaderID INT FOREIGN KEY REFERENCES Header(ID)
    )
    ''')
    
    conn.commit()


# Conexão com o SQL Server
conn = create_connection()

# Criar as tabelas
create_tables(conn)

    