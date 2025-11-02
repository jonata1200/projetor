import threading
import time
import pyaudio

from .ia.audio_streamer import AudioStreamer
from .ia.speech_transcriber import SpeechTranscriber
from .ia.slide_synchronizer import SlideSynchronizer

class IASyncEngine:
    """
    Orquestra o processo de sincronização por IA, unindo captura de áudio,
    transcrição e a lógica de sincronização de slides.
    """
    SAMPLE_RATE = 16000
    CHUNK_SIZE = int(SAMPLE_RATE / 10)
    AUDIO_FORMAT = pyaudio.paInt16
    WORDS_PER_SYNC_ATTEMPT = 4
    POST_JUMP_PAUSE_DURATION = 4.0

    def __init__(self, callback_goto_slide, callback_status_update, input_device_index=None, **kwargs):
        self.callback_goto_slide = callback_goto_slide
        self.callback_status_update = callback_status_update
        
        self.audio_streamer = AudioStreamer(
            self.SAMPLE_RATE, self.CHUNK_SIZE, 1, self.AUDIO_FORMAT, input_device_index
        )
        try:
            self.transcriber = SpeechTranscriber(self.SAMPLE_RATE)
            self.is_ready = True
        except (ImportError, RuntimeError) as e:
            self.callback_status_update("IA: Erro inicialização.")
            print(f"ERRO IASyncEngine: {e}")
            self.is_ready = False

        self.synchronizer = SlideSynchronizer()

        self.is_listening = False
        self.stop_event = threading.Event()
        self.main_thread = None
        self.current_slides = []
        self.current_slide_index = -1

    def start_listening(self, lyrics_slides, start_index):
        if self.is_listening or not self.is_ready:
            if not self.is_ready: self.callback_status_update("IA: Não está pronto.")
            return

        try:
            self.audio_streamer.start()
        except Exception as e:
            self.callback_status_update("IA: Erro no Mic.")
            return

        self.current_slides = lyrics_slides
        self.current_slide_index = start_index
        self.is_listening = True
        self.stop_event.clear()
        
        self.main_thread = threading.Thread(target=self._run_sync_loop, daemon=True)
        self.main_thread.start()
        self.callback_status_update("IA: Ouvindo...")

    def stop_listening(self):
        if not self.is_listening:
            return
            
        self.is_listening = False
        self.stop_event.set()
        self.audio_streamer.stop()
        
        if self.main_thread and self.main_thread.is_alive():
            self.main_thread.join(timeout=1.0)
        
        self.main_thread = None
        self.callback_status_update("IA: Parado.")

    def update_current_slide(self, new_slide_index, new_slides_list=None):
        self.current_slide_index = new_slide_index
        if new_slides_list is not None:
            self.current_slides = new_slides_list
        if self.is_listening:
             self.callback_status_update(f"IA: Slide {new_slide_index + 1}...")

    def _run_sync_loop(self):
        word_buffer = []
        
        audio_generator = self.audio_streamer.audio_generator()
        transcription_generator = self.transcriber.transcribe_stream(audio_generator)

        for response in transcription_generator:
            if self.stop_event.is_set(): break
            if not response.results: continue
            
            result = response.results[0]
            if not result.alternatives: continue
            
            transcript = result.alternatives[0].transcript.strip()
            
            if not result.is_final:
                self.callback_status_update(f"IA: ...{transcript[-30:]}")
                continue

            if transcript:
                word_buffer.extend(self.synchronizer.normalize_text(transcript).split())
                
                if len(word_buffer) >= self.WORDS_PER_SYNC_ATTEMPT:
                    text_to_analyze = " ".join(word_buffer)
                    new_slide_index = self.synchronizer.find_best_match(
                        text_to_analyze, self.current_slides, self.current_slide_index
                    )
                    
                    if new_slide_index is not None:
                        self.callback_goto_slide(new_slide_index)
                        word_buffer.clear()
                        
                        self.callback_status_update(f"IA: Pausa ({self.POST_JUMP_PAUSE_DURATION}s)...")
                        time.sleep(self.POST_JUMP_PAUSE_DURATION)
                        if self.stop_event.is_set(): break
                        self.callback_status_update("IA: Ouvindo...")

                    else:
                        word_buffer = word_buffer[self.WORDS_PER_SYNC_ATTEMPT:]