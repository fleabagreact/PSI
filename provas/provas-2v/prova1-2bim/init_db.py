import sqlite3

# Nome do arquivo do banco de dados
DATABASE = 'escola.db'

# Localização do arquivo SQL
SCHEMA = 'database/schema.sql'

def init_db():
    # Abre a conexão com o banco de dados
    conn = sqlite3.connect(DATABASE)
    
    # Executa as declarações SQL do arquivo de esquema
    with open(SCHEMA, 'r') as f:
        conn.executescript(f.read())
    
    # Confirma as alterações e fecha a conexão
    conn.commit()
    conn.close()

# Executa a função init_db quando o script for rodado
if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso.")