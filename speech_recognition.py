import sounddevice as sd
import numpy as np
import soundfile as sf
import subprocess
from TTS.api import TTS
from deep_seek_conection import ask_deepseek

from memory.long.BD_Connection import salvar_historico, obter_historico
from memory.short.redis import salvar_contexto, obter_contexto
from memory.Me import carregar_perfil

from deep_seek_modelo_base import montaTexto, monta_topicos

from limpar_transcricao import limpar_transcricao

from aux_comand.tasks import verificar_task

# Configuração do áudio
RATE = 16000  # Taxa de amostragem (16 kHz, compatível com Whisper)
DURATION = 10  # Tempo de gravação (segundos)
OUTPUT_FILE = "audio_temp.wav"  # Nome do arquivo de saída
tts = TTS("tts_models/pt/cv/vits", progress_bar=False)

def gravar_audio():
    """Grava áudio do microfone e salva como um arquivo WAV"""
    print("🎙️ Gravando... Fale agora!")
    audio = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1, dtype="int16")
    sd.wait()  # Aguarda a gravação terminar
    print("🛑 Gravação finalizada!")

    # Salva o áudio como um arquivo WAV
    sf.write(OUTPUT_FILE, audio, RATE)

def transcrever_audio():
    """Executa o Whisper-cpp para transcrever o áudio gravado"""
    whisper_cli_path = "/Users/igor/whisper.cpp/build/bin/whisper-cli" 
    Whisper_model_path = "/Users/igor/whisper/models/small.bin"
    comando = [
        whisper_cli_path,  # Caminho para o executável do Whisper
        "-m", Whisper_model_path,  # Modelo de transcrição
        "-f", OUTPUT_FILE,  # Arquivo de áudio gravado
        "--language", "pt"  # Define o idioma como português
    ]
    
    try:
        # Executa o comando e captura a saída
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return resultado.stdout  # Retorna a transcrição
    except subprocess.CalledProcessError as e:
        # Caso ocorra um erro na execução do comando
        print("Erro ao executar o comando:", e.stderr)
        return None
    
def texto_para_fala(texto, arquivo_saida="fala.wav"):
    """Executa o Whisper-cpp para Ciar o áudio a partir do texto"""
    
    print("🔊 Gerando fala...")
    tts.tts_to_file(text=texto, file_path=arquivo_saida)

    # Toca o áudio gerado
    data, samplerate = sf.read(arquivo_saida)
    sd.play(data, samplerate)
    sd.wait()

    print("✅ Fala gerada e reproduzida!")

def processar_mensagem(usuario_id, mensagem):
    contexto = obter_contexto(usuario_id)  # Puxa curto prazo (Redis)
    perfil = carregar_perfil(usuario_id)   # Carrega personalização (JSON)
    MontaHistoricoDeTopicos = monta_topicos(mensagem)
    respostaHistorico = ask_deepseek(MontaHistoricoDeTopicos)
    
    historico = obter_historico(1,respostaHistorico, 5)  # Consulta últimas interações (PostgreSQL)

    # Busca conhecimento relevante via embeddings
    #memoria_relevante = buscar_memoria(mensagem)
    perguntaOtimizada = montaTexto(mensagem,contexto,perfil,historico,memoria_relevante='')
    # Gera resposta com IA baseada em tudo isso
    resposta = ask_deepseek(perguntaOtimizada)

    MensagemLimpa, Topicos = limpar_transcricao(mensagem)
    salvar_contexto(usuario_id, MensagemLimpa)  # Atualiza memória de curto prazo
    salvar_historico(usuario_id, MensagemLimpa, resposta,Topicos)  # Atualiza memória de longo prazo
    
    #adicionar_memoria(mensagem)  # Atualiza embeddings

    return resposta

    
# Executa o processo completo
gravar_audio()
transcricao = transcrever_audio()
print("📝 Transcrição:", transcricao)
verificaTask = verificar_task(transcricao)
print("📝 Task:", verificaTask)
if verificaTask == "":
    deep_seek_response = processar_mensagem(1, transcricao)
else:
    texto_para_fala(verificaTask)
if deep_seek_response != '':
    if transcricao:
        print("Resposta Deep-Seek - ",deep_seek_response)
    else:
        print("❌ Erro na transcrição")

    texto_para_fala(deep_seek_response)
else:
    if verificaTask == "":
        print("J.A.R.V.I.S nao retornou nada!")


