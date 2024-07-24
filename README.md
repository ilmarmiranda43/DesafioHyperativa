# DesafioHyperativa
API para inserir dados de cartão via upload de arquivo TXT.

# API de Processamento de Arquivos e Consulta de Cartões

Esta API em Flask é projetada para processar arquivos e armazenar informações em um banco de dados SQL Server, além de permitir a consulta de informações de cartões.

## Requisitos

- Python 3.7 ou superior
- Flask
- pyodbc
- PyJWT

Você pode instalar as dependências usando o `pip`:

pip install Flask pyodbc PyJWT

## Configuração do Banco de Dados
A API se conecta a um banco de dados SQL Server. As credenciais de conexão são configuradas diretamente no código. Certifique-se de alterar os seguintes parâmetros na função get_db_connection para refletir as suas configurações:

server

database

username

password

## Endpoints

/login (POST)
Gera um token JWT para autenticação.

Exemplo de utilização no Postman

![image](https://github.com/user-attachments/assets/71c12f05-29c6-4c95-88dd-a8a3d62c9c93)


