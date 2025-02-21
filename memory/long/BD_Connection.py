import psycopg2
from datetime import datetime

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

def salvar_historico(usuario_id, mensagem, resposta,data=datetime.today()):
    cursor.execute("INSERT INTO historico (usuario_id, mensagem, resposta,data) VALUES (%s, %s, %s,%s)", (usuario_id, mensagem, resposta,data))
    conn.commit()

def obter_historico(usuario_id, limite=20):
    cursor.execute("SELECT EXISTS (SELECT 1 FROM historico WHERE usuario_id = %s)", (usuario_id,))
    existe = cursor.fetchone()[0]  # Retorna True se há dados, False se não houver

    if existe == True:
        cursor.execute("SELECT mensagem, resposta FROM historico WHERE usuario_id=%s ORDER BY data DESC LIMIT %s", (usuario_id, limite))
        return cursor.fetchall()
    else:
        return ""
    
def salvar_principais_topicos(topicos_conversa):
    cursor.execute("UPDATE historico SET principais_topicos = %s WHERE id = (SELECT id FROM historico ORDER BY data DESC LIMIT 1);", (topicos_conversa))
    conn.commit()
