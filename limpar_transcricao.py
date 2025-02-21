import re

def limpar_transcricao(texto):
    """
    Remove a marcação de tempo do texto transcrito.
    Exemplo:
    Entrada: "[00:00:00.000 --> 00:00:02.000]   Teste de algo."
    Saída: "Teste de algo."
    """
    #Remove o Think
    texto_sem_think =  re.sub(r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*", "", texto)

    # Extraindo o conteúdo dentro das tags <topicos> </topicos>
    texto_topicos = re.search(r"<topicos>(.*?)</topicos>", texto_sem_think, re.DOTALL)

    #Remove o <topicos>
    texto_sem_think = re.sub(r"<topicos>.*?</topicos>", "", texto_sem_think, flags=re.DOTALL)

    if texto_topicos:
        conteudo_extraido = texto_topicos.group(1)
    else:
        conteudo_extraido = ''
        print("Nenhum conteúdo encontrado entre <topicos>.")

    return texto_sem_think.strip(), conteudo_extraido.strip()


