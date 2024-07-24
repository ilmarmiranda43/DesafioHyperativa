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

### /login (POST)
Gera um token JWT para autenticação.

Todos os Endpoints abaixo, foram executados no Postman

![image](https://github.com/user-attachments/assets/71c12f05-29c6-4c95-88dd-a8a3d62c9c93)

### /upload (POST)
Permite o upload de um arquivo para processamento. O arquivo deve ser enviado no corpo da solicitação com o campo file.

Para fazer o upload do arquivo, primeiro insira o token no local indicado:

![image](https://github.com/user-attachments/assets/3c0d8030-f5e3-4bd1-84eb-0d7cd19a4a89)

Depois, faça a seleção do arquivo na sua máquina:

![image](https://github.com/user-attachments/assets/344aad5a-e963-424b-8235-96657323e85e)

### /card/<card_number> (GET)
Obtém informações sobre um cartão com base no número do cartão fornecido.

Para consultar um cartão na base de dados, faça como mostrado na tela abaixo:

![image](https://github.com/user-attachments/assets/2331f668-27d5-4ec0-90a3-2a1b447f274c)





