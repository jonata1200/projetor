import pyaudio
import threading

class AudioStreamer:
    """
    Gerencia a captura de áudio do microfone usando PyAudio.
    Fornece um gerador que produz 'chunks' de áudio para serem consumidos
    por um serviço de transcrição.
    """
    def __init__(self, sample_rate, chunk_size, channels, audio_format, input_device_index=None):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.audio_format = audio_format
        self.input_device_index = input_device_index

        self.pyaudio_instance = None
        self.pyaudio_stream = None
        self.is_streaming = threading.Event()

    def start(self):
        """Abre o stream de áudio. Lança uma exceção em caso de erro."""
        if self.pyaudio_stream and self.pyaudio_stream.is_active():
            return
            
        try:
            self.pyaudio_instance = pyaudio.PyAudio()
            self.pyaudio_stream = self.pyaudio_instance.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=self.input_device_index
            )
            self.is_streaming.set()

        except Exception as e:
            print(f"ERRO AudioStreamer: Falha ao iniciar o stream - {e}")
            self.stop()
            raise

    def stop(self):
        """Para e fecha o stream de áudio, liberando os recursos."""
        self.is_streaming.clear()
        if self.pyaudio_stream:
            try:
                if self.pyaudio_stream.is_active():
                    self.pyaudio_stream.stop_stream()
                self.pyaudio_stream.close()
            except Exception as e:
                print(f"AVISO AudioStreamer: Erro ao fechar o stream: {e}")
            self.pyaudio_stream = None
        
        if self.pyaudio_instance:
            try:
                self.pyaudio_instance.terminate()
            except Exception as e:
                print(f"AVISO AudioStreamer: Erro ao terminar PyAudio: {e}")
            self.pyaudio_instance = None
        print("AudioStreamer: Stream de áudio parado e recursos liberados.")

    def audio_generator(self):
        """Gerador que produz 'chunks' de áudio enquanto o stream estiver ativo."""
        while self.is_streaming.is_set():
            try:
                chunk = self.pyaudio_stream.read(self.chunk_size, exception_on_overflow=False)
                if chunk:
                    yield chunk
            except IOError as e:
                print(f"ERRO AudioStreamer: Erro de I/O no stream: {e}")
                self.is_streaming.clear()
                break