import re
import ollama

def ask_deepseek(prompt, context=None):
    """Envia uma pergunta para o DeepSeek via Ollama e retorna apenas a resposta relevante."""
    try:
        messages = [{"role": "user", "content": prompt}]
        if context:
            messages.insert(0, {"role": "system", "content": context})
        
        response = ollama.chat(model="deepseek-r1:7b", messages=messages)

        # Certifica-se de que 'message' e 'content' existem na resposta
        if not hasattr(response, "message") or not hasattr(response.message, "content"):
            return "Erro: Resposta inválida recebida do modelo."

        # Obtém o conteúdo da resposta
        content = response.message.content.strip()

        # Remove qualquer coisa dentro de <think>...</think>
        clean_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        return clean_content if clean_content else "Erro: Resposta vazia do modelo."
    
    except Exception as e:
        print(f"Erro ao comunicar com DeepSeek: {e}")
        return f"Erro ao processar a solicitação: {e}"
