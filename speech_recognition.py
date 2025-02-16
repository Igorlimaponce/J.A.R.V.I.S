import sounddevice as sd
import numpy as np
import soundfile as sf
import subprocess

# Configuração do áudio
RATE = 16000  # Taxa de amostragem (16 kHz, compatível com Whisper)
DURATION = 10  # Tempo de gravação (segundos)
OUTPUT_FILE = "audio_temp.wav"  # Nome do arquivo de saída

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

# Executa o processo completo
gravar_audio()
transcricao = transcrever_audio()
if transcricao:
    print("📝 Transcrição:", transcricao)
else:
    print("❌ Erro na transcrição")
