import redis

r = redis.Redis(host="localhost",port=6379,db=0,decode_responses=0)

def salvar_contexto(usuario_id,mensagem):
    chave = f"contexto:{usuario_id}"
    r.rpush(chave, mensagem)  
    r.expire(chave, 3600)  # Define tempo de expiração (1 hora)
    if r.llen(chave) > 10:  # Mantém apenas as últimas 10 interações
        r.lpop(chave)

def obter_contexto(usuario_id):
    chave = f"contexto:{usuario_id}"
    return r.lrange(chave, 0, -1)