from flask import Flask, request, jsonify
import pyodbc
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  # Altere para uma chave secreta segura

# Configure a conexão com o SQL Server
def get_db_connection():
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

# Função para processar o arquivo e inserir dados nas tabelas
def process_file(file_content, conn):
    lines = file_content.splitlines()

    header_line = lines[0].strip()
    footer_line = lines[-1].strip()

    # Processar o cabeçalho
    header = {
        'name': header_line[0:29].strip(),
        'date': header_line[29:37].strip(),
        'lot': header_line[37:45].strip(),
        'record_count': int(header_line[45:51].strip())
    }

    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Header (Name, Date, Lote, RecordCount)
    VALUES (?, ?, ?, ?)
    ''', (header['name'], header['date'], header['lot'], header['record_count']))

    conn.commit()

    cursor.execute('SELECT MAX(ID) FROM Header')
    header_id = cursor.fetchone()[0]

    # Processar as linhas
    for line in lines[1:-1]:
        line = line.strip()
        identificador = line[0:1].strip()

        if identificador == 'C':
            line_data = {
                'line_identifier': line[0:1].strip(),
                'line_number': line[1:7].strip(),
                'card_number': line[7:26].strip()
            }

            cursor.execute('''
            INSERT INTO Lines (LineIdentifier, LineNumber, CardNumber, HeaderID)
            VALUES (?, ?, ?, ?)
            ''', (line_data['line_identifier'], line_data['line_number'], line_data['card_number'], header_id))

    # Processar o rodapé
    footer = {
        'lot': footer_line[0:8].strip(),
        'record_count': int(footer_line[8:14].strip())
    }

    cursor.execute('''
    INSERT INTO Footer (Lote, RecordCount, HeaderID)
    VALUES (?, ?, ?)
    ''', (footer['lot'], footer['record_count'], header_id))

    conn.commit()

# Decorator para verificar o token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':  # Use uma verificação adequada para autenticação
        token = jwt.encode({'user': auth.username, 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Could not verify!'}), 401

@app.route('/upload', methods=['POST'])
@token_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_content = file.read().decode('utf-8')

        # Processar o arquivo e inserir os dados
        conn = get_db_connection()
        try:
            process_file(file_content, conn)
        finally:
            conn.close()

        return jsonify({'message': 'File processed successfully'})

@app.route('/card/<card_number>', methods=['GET'])
@token_required
def get_card_info(card_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT Lines.ID, Lines.CardNumber, Header.Lote
    FROM Lines
    JOIN Header ON Lines.HeaderID = Header.ID
    WHERE Lines.CardNumber = ?
    ''', (card_number,))
    
    card_info = cursor.fetchone()
    conn.close()
    
    if card_info:
        return jsonify({'ID': card_info[0], 'CardNumber': card_info[1], 'Lot': card_info[2]})
    else:
        return jsonify({'message': 'Card not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
