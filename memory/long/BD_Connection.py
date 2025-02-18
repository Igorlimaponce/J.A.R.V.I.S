import psycopg2

# Conectar ao banco de dados
conn = psycopg2.connect(database="J.A.R.V.I.S", user="postgres", password="123456", host="localhost")
cursor = conn.cursor()

# Criar tabela para armazenar histórico
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id SERIAL PRIMARY KEY,
        usuario_id TEXT,
        mensagem TEXT,
        resposta TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def salvar_historico(usuario_id, mensagem, resposta):
    cursor.execute("INSERT INTO historico (usuario_id, mensagem, resposta) VALUES (%s, %s, %s)", (usuario_id, mensagem, resposta))
    conn.commit()

def obter_historico(usuario_id, limite=20):
    cursor.execute("SELECT mensagem, resposta FROM historico WHERE usuario_id=%s ORDER BY data DESC LIMIT %s", (usuario_id, limite))
    return cursor.fetchall()
