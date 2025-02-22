import os
import shutil
import webbrowser
import smtplib
from email.mime.text import MIMEText
import requests
import spacy

# ============================ #
#  1️⃣ Carregar o Modelo de NLP #
# ============================ #
nlp = spacy.load("pt_core_news_sm")  # Baixa com: python -m spacy download pt_core_news_sm

# ============================ #
#  2️⃣ Funções de Comandos       #
# ============================ #

def abrir_pasta(caminho):
    os.startfile(caminho)
    return f"Pasta '{caminho}' aberta."

def criar_arquivo(nome, conteudo=""):
    with open(nome, "w") as f:
        f.write(conteudo)
    return f"Arquivo '{nome}' criado com conteúdo: {conteudo}"

#def deletar_arquivo(nome):
    if os.path.exists(nome):
        os.remove(nome)
        return f"Arquivo '{nome}' deletado."
    return "Arquivo não encontrado."

def mover_arquivo(origem, destino):
    if os.path.exists(origem):
        shutil.move(origem, destino)
        return f"Arquivo movido para '{destino}'."
    return "Arquivo de origem não encontrado."

def abrir_site(url):
    webbrowser.open(url)
    return f"Abrindo '{url}' no navegador."

def enviar_email(destinatario, assunto, mensagem):
    remetente = "seuemail@gmail.com"  # Substitua pelo seu e-mail
    senha = "suasenha"  # Substitua pela senha do e-mail

    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())

    return f"E-mail enviado para {destinatario} com assunto '{assunto}'."

# Dicionário de comandos disponíveis
comandos = {
    "abrir pasta": abrir_pasta,
    "criar arquivo": criar_arquivo,
    #"deletar arquivo": deletar_arquivo,
    "mover arquivo": mover_arquivo,
    "abrir site": abrir_site,
    "enviar email": enviar_email
}

# ============================ #
#  3️⃣ Detectar Comandos usando NLP #
# ============================ #

def detectar_comando(mensagem):
    """
    Usa NLP para identificar comandos na mensagem.
    Retorna o comando detectado e os parâmetros extraídos.
    """

    doc = nlp(mensagem.lower())

    # Verifica comandos de forma mais flexível
    if "abrir" in mensagem and "pasta" in mensagem:
        for token in doc:
            if token.dep_ in ["obl", "obj"]:  # Tenta pegar objetos
                return "abrir pasta", (token.text,)
    
    if "criar" in mensagem and "arquivo" in mensagem:
        palavras = mensagem.split()
        if "chamado" in palavras:
            index = palavras.index("chamado") + 1
            nome_arquivo = palavras[index]
            conteudo = " ".join(palavras[index + 2:]) if "com" in palavras else ""
            return "criar arquivo", (nome_arquivo, conteudo)

    #if "deletar" in mensagem and "arquivo" in mensagem:
        #palavras = mensagem.split()
        #nome_arquivo = palavras[-1]
        #return "deletar arquivo", (nome_arquivo,)

    if "mover" in mensagem and "arquivo" in mensagem:
        palavras = mensagem.split()
        if "para" in palavras:
            index = palavras.index("para")
            origem = palavras[index - 1]
            destino = palavras[index + 1]
            return "mover arquivo", (origem, destino)

    if "abrir" in mensagem and "site" in mensagem:
        palavras = mensagem.split()
        url = next((word for word in palavras if "http" in word), None)
        return "abrir site", (url,)

    if "enviar" in mensagem and "email" in mensagem:
        destinatario = None
        assunto = "Mensagem Automática"
        mensagem_email = ""

        for token in doc:
            if token.like_email:
                destinatario = token.text
            if token.dep_ == "obl":
                mensagem_email += token.text + " "

        if destinatario:
            return "enviar email", (destinatario, assunto, mensagem_email.strip())

    return None, None  # Nenhum comando encontrado

def verificar_task(mensagem):
    """
    Função principal que recebe a entrada do usuário, processa a resposta da IA,
    detecta comandos e executa ações conforme necessário.
    """

    # Tenta extrair comando da resposta
    comando, parametros = detectar_comando(mensagem)
    
    if comando and comando in comandos:
        resultado = comandos[comando](*parametros)
        return f"\n[EXECUTADO] {resultado}"
    else:
        return ""
    