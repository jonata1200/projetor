import string
from difflib import SequenceMatcher

class SlideSynchronizer:
    """
    Contém a lógica de negócio para sincronizar o texto transcrito com os slides.
    É uma classe sem estado de I/O, focada apenas na lógica de comparação.
    """
    PHRASE_MATCH_THRESHOLD = 0.40
    CURRENT_SLIDE_BIAS = 0.05
    NEXT_SLIDE_BONUS = 0.15
    LOW_CURRENT_MATCH_OVERRIDE = 0.25
    MIN_WORDS_FOR_PHRASE = 2
    
    def normalize_text(self, text):
        if not text: return ""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return " ".join(text.split())

    def _similarity(self, a, b):
        if not a or not b: return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def _find_best_substring_match(self, recognized_norm, slide_norm):
        """Usa uma janela deslizante para encontrar a melhor correspondência dentro do slide."""
        if not recognized_norm or not slide_norm:
            return 0.0

        recognized_words = recognized_norm.split()
        slide_words = slide_norm.split()
        
        if len(slide_words) < len(recognized_words):
            return self._similarity(recognized_norm, slide_norm)

        best_score = 0.0
        for i in range(len(slide_words) - len(recognized_words) + 1):
            substring_to_check = " ".join(slide_words[i : i + len(recognized_words)])
            score = self._similarity(recognized_norm, substring_to_check)
            if score > best_score:
                best_score = score
        return best_score

    def find_best_match(self, recognized_text, slides_content, current_slide_index):
        """
        Versão melhorada que usa uma busca por substring (janela deslizante) para
        analisar o texto reconhecido e decidir se deve pular para um novo slide.
        Retorna o índice do novo slide para pular, ou None se nenhum salto for necessário.
        """
        recognized_norm = self.normalize_text(recognized_text)
        
        if len(recognized_norm.split()) < self.MIN_WORDS_FOR_PHRASE:
            return None

        normalized_slides = [self.normalize_text(s) for s in slides_content]
        scores = [self._find_best_substring_match(recognized_norm, s) for s in normalized_slides]
        next_slide_index = current_slide_index + 1
        
        if next_slide_index < len(scores):
            original_next_score = scores[next_slide_index]
            scores[next_slide_index] += self.NEXT_SLIDE_BONUS
            print(f"IA BONUS: Bônus de {self.NEXT_SLIDE_BONUS} aplicado ao slide {next_slide_index + 1}. Score foi de {original_next_score:.2f} para {scores[next_slide_index]:.2f}.")

        best_match_index = scores.index(max(scores))
        highest_score = scores[best_match_index]

        print(f"IA DEBUG: Texto='{recognized_norm[:30]}...' | Melhor Slide: {best_match_index+1} (Score: {highest_score:.2f}) | Slide Atual: {current_slide_index+1} (Score: {scores[current_slide_index]:.2f})")
        
        if best_match_index != current_slide_index and highest_score > self.PHRASE_MATCH_THRESHOLD:
            
            current_slide_score_with_bias = scores[current_slide_index] + self.CURRENT_SLIDE_BIAS

            if highest_score > current_slide_score_with_bias:
                print(f"--- IA JUMP! Para slide {best_match_index + 1} ---")
                return best_match_index
        
        return None