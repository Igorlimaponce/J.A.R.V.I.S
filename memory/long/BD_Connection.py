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

def salvar_historico(usuario_id, mensagem, resposta,Topicos,data=datetime.today()):
    cursor.execute("INSERT INTO historico (usuario_id, mensagem, resposta,data,principais_topicos) VALUES (%s, %s, %s,%s,%s)", (usuario_id, mensagem, resposta,data,Topicos))
    conn.commit()

def obter_historico(usuario_id, TopicosResumidos, limite=5):
    """Busca histórico relevante com base nos principais tópicos"""
    # Verifica se há dados para o usuário antes de fazer a consulta
    cursor.execute("SELECT EXISTS (SELECT 1 FROM historico WHERE usuario_id = %s)", (usuario_id,))
    existe = cursor.fetchone()[0]  # Retorna True se há dados, False se não houver

    # Se não há histórico, retorna vazio
    if not existe:
        return ""

    # Se os tópicos estiverem vazios, evita erro
    if not TopicosResumidos.strip():
        return ""

    # Monta a string de busca no formato correto para `to_tsquery`
    topicos_busca = " & ".join(TopicosResumidos.lower().replace(",", " ").split())

    # Faz a consulta ao histórico
    cursor.execute("""
        SELECT mensagem, resposta 
        FROM historico 
        WHERE to_tsvector('portuguese', principais_topicos) @@ to_tsquery('portuguese', %s) 
        AND COALESCE(principais_topicos, '') <> ''
        ORDER BY data DESC 
        LIMIT %s

    """, (topicos_busca, limite))

    return cursor.fetchall()

    
