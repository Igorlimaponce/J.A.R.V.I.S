import json

def carregar_perfil(usuario_id):
    with open(f"memory/{usuario_id}.json", "r") as arquivo:
        return json.load(arquivo)

# Exemplo de arquivo JSON
"""
{
    "nome": "Igor",
    "personalidade": "Sou um estudante de engenharia de software, gosto muito de tecnologia e sou bastante interessado por Inteligencia artificial",
    "interesses": ["investimentos", "engenharia de software", "IA", "robótica"],
    "preferencias_resposta": {
        "formalidade": "informal",
        "detalhamento": "médio",
        "Idioma": "Portugues - BR"
    }
}
"""
