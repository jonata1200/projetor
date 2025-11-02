try:
    from google.cloud import speech
    GOOGLE_CLOUD_SPEECH_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_SPEECH_AVAILABLE = False
    speech = None

class SpeechTranscriber:
    """
    Responsável por interagir com a API de Speech-to-Text do Google Cloud.
    Recebe um fluxo de áudio e retorna os resultados da transcrição.
    """
    def __init__(self, sample_rate, language_code="pt-BR"):
        if not GOOGLE_CLOUD_SPEECH_AVAILABLE:
            raise ImportError("Biblioteca google-cloud-speech não está instalada.")
        
        try:
            self.speech_client = speech.SpeechClient()
        except Exception as e:
            raise RuntimeError(f"Falha ao inicializar o cliente Google Speech: {e}")

        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=True
        )

    def transcribe_stream(self, audio_generator):
        """
        Recebe um gerador de áudio e produz os resultados da API do Google.
        Este método é um gerador ele mesmo.
        """
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        try:
            responses = self.speech_client.streaming_recognize(
                config=self.streaming_config,
                requests=requests
            )
            yield from responses
        except Exception as e:
            print(f"ERRO SpeechTranscriber: Falha na API de streaming: {e}")
            return