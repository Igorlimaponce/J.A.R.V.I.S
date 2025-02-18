import re

def limpar_transcricao(texto):
    """
    Remove a marcação de tempo do texto transcrito.
    Exemplo:
    Entrada: "[00:00:00.000 --> 00:00:02.000]   Teste de algo."
    Saída: "Teste de algo."
    """
    return re.sub(r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*", "", texto)
