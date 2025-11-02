from services.bible_api_client import BibleAPIClient

class BibleManager:
    def __init__(self):
        self.api_client = BibleAPIClient()
        self.versions = []
        self.books = []
        self.current_version = None

    def load_versions(self):
        self.versions = self.api_client.get_versions()
        return self.versions

    def load_books(self, version_abbrev=None):
        if not self.books:
            self.books = self.api_client.get_books()
        return self.books
    
    def get_book_by_abbrev(self, abbrev):
        if not self.books: self.load_books()
        for book in self.books:
            current_book_abbrev = book.get('abbrev')
            if isinstance(current_book_abbrev, dict):
                if current_book_abbrev.get('pt') == abbrev or current_book_abbrev.get('en') == abbrev:
                    return book
            elif isinstance(current_book_abbrev, str):
                if current_book_abbrev == abbrev:
                    return book
        return None

    def get_verses_as_slides(self, version_abbrev, book_abbrev, chapter_number):
        """
        Retorna os versículos de um capítulo como uma lista de strings (slides).
        Cada slide pode ser um único versículo ou um pequeno grupo. Por simplicidade, um por slide.
        """
        verses_data = self.api_client.get_chapter_verses(version_abbrev, book_abbrev, chapter_number)
        slides = []
        if verses_data:
            book_name = book_abbrev.upper()
            
            if not self.books:
                self.load_books()
            
            found_book = self.get_book_by_abbrev(book_abbrev)
            if found_book:
                book_name = found_book.get("name", book_name)

            for verse in verses_data:
                slide_text = f"{book_name} {chapter_number}:{verse['number']}\n{verse['text']}"
                slides.append(slide_text)
        return slides

if __name__ == '__main__':
    manager = BibleManager()
    
    versions = manager.load_versions()
    if versions:
        for v in versions:
            print(f"{v['name']} ({v['version']})")
        selected_version = versions[0]['version']
    else:
        print("Nenhuma versão carregada.")
        selected_version = "nvi"

    books = manager.load_books()
    if books:
        for i, book in enumerate(books[:3]):
             current_book_abbrev = book.get('abbrev')
             abbrev_display = current_book_abbrev.get('pt') if isinstance(current_book_abbrev, dict) else current_book_abbrev
             print(f"{book['name']} ({abbrev_display})")
        
        if books:
            selected_book_data = books[0]
            selected_book_abbrev_obj = selected_book_data['abbrev']
            selected_book_abbrev = selected_book_abbrev_obj.get('pt') if isinstance(selected_book_abbrev_obj, dict) else selected_book_abbrev_obj
            chapter_to_load = 1

            print(f"\n--- Slides de {selected_book_data['name']} Cap. {chapter_to_load} ({selected_version}) ---")
            slides = manager.get_verses_as_slides(selected_version, selected_book_abbrev, chapter_to_load)
            if slides:
                for i, slide in enumerate(slides[:2]):
                    print(f"Slide {i+1}:\n{slide}\n")
            else:
                print("Nenhum slide de versículo encontrado.")
    else:
        print("Nenhum livro carregado.")