def montaTexto(mensagem, contexto, perfil, historico, memoria_relevante):
    # Garante que as variáveis existem
    perfil = perfil or {}  # Evita erro se perfil for None
    historico = historico or []
    memoria_relevante = memoria_relevante or "Nenhuma memória relevante encontrada."
    contexto = contexto or "Nenhum contexto disponível."
    mensagem = mensagem or "Nenhuma mensagem fornecida."

    # Verifica se as chaves existem antes de acessar
    nome_usuario = perfil.get('nome', 'Usuário')
    interesses = ', '.join(perfil.get('interesses', ['sem interesses definidos']))
    formalidade = perfil.get('preferencias_resposta', {}).get('formalidade', 'neutra')
    detalhamento = perfil.get('preferencias_resposta', {}).get('detalhamento', 'médio')
    idioma = perfil.get('idioma', 'Português')

    # Histórico formatado de forma segura
    historico_formatado = '\n'.join([f'Usuário: {m[0]} | Assistente: {m[1]}' for m in historico]) if historico else "Nenhum histórico disponível."

    # String final
    pergunta_modelo = f"""
    Você é um assistente pessoal inteligente e offline. Seu usuário é {nome_usuario}.
    Ele gosta de {interesses}.
    Ele prefere respostas {formalidade} e com nível de detalhe {detalhamento}.
    Ele quer que você utilize como linguagem de resposta {idioma}.

    Contexto geral:
    {contexto}

    Histórico recente da conversa:
    {historico_formatado}

    Memória relevante do usuário:
    {memoria_relevante}

    Responda normalmente à minha pergunta.
    Depois da resposta, liste em no máximo 15 palavras os principais tópicos abordados.
    Coloque APENAS os tópicos dentro <topicos> e </topicos>.
    Antes de enviar a resposta, verifique que <topicos> foi aberto e fechado corretamente.

    Agora, responda da melhor maneira possível:
    Usuário: {mensagem}
    Assistente:
    """

    print(pergunta_modelo)  # Para depuração

        
    return pergunta_modelo