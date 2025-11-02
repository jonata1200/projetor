import customtkinter as ctk

class AllSlidesViewWindow(ctk.CTkToplevel):
    def __init__(self, master, slides_list, current_slide_index, callback_goto_slide):
        super().__init__(master)
        self.transient(master)
        self.title("Visualização de Todos os Slides")
        self.geometry("800x600")
        self.resizable(True, True)

        self.slides_list = slides_list
        self.current_slide_index = current_slide_index 
        self.callback_goto_slide = callback_goto_slide

        self.miniature_frames = []
        self.highlight_color = "cyan"
        self.default_border_color = ctk.ThemeManager.theme["CTkFrame"]["border_color"]
        if self.default_border_color is None:
            try:
                temp_frame = ctk.CTkFrame(self)
                self.default_border_color = temp_frame.cget("border_color")
                temp_frame.destroy()
            except:
                self.default_border_color = "gray50"

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text=None)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_slides()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(100, self._center_window_on_master)

    def display_slides(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.miniature_frames.clear()

        if not self.slides_list:
            ctk.CTkLabel(self.scrollable_frame, text="Nenhum slide para exibir.").pack(pady=20)
            return

        num_columns = 3 
        for i in range(num_columns):
            self.scrollable_frame.grid_columnconfigure(i, weight=1, uniform="slide_col")

        row_num = 0
        col_num = 0

        for index, slide_text in enumerate(self.slides_list):
            border_c = self.highlight_color if index == self.current_slide_index else self.default_border_color
            
            miniature_frame = ctk.CTkFrame(
                self.scrollable_frame,
                border_width=2,
                border_color=border_c
            )
            miniature_frame.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="nsew")
            miniature_frame.grid_rowconfigure(1, weight=1)
            miniature_frame.grid_columnconfigure(0, weight=1)
            
            self.miniature_frames.append(miniature_frame) 

            slide_number_label = ctk.CTkLabel(miniature_frame, text=f"Slide {index + 1}", font=ctk.CTkFont(size=10))
            slide_number_label.grid(row=0, column=0, padx=5, pady=(5,0), sticky="nw")

            preview_text = " ".join(slide_text.split()[:20])
            if len(slide_text.split()) > 20: preview_text += "..."
            
            text_label = ctk.CTkLabel(
                miniature_frame, 
                text=preview_text, 
                font=ctk.CTkFont(size=11), 
                wraplength=180, 
                justify="left",
                anchor="nw"
            )
            text_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            widgets_to_bind = [miniature_frame, slide_number_label, text_label]
            for widget in widgets_to_bind:
                widget.bind("<Button-1>", lambda event, idx=index: self.on_miniature_click(idx))
                widget.configure(cursor="hand2")

            col_num += 1
            if col_num >= num_columns:
                col_num = 0
                row_num += 1
        
        ctk.CTkFrame(self.scrollable_frame, height=10, fg_color="transparent").grid(row=row_num + 1, column=0)

    def on_miniature_click(self, new_slide_index):

        if new_slide_index != self.current_slide_index:
            if 0 <= self.current_slide_index < len(self.miniature_frames):
                old_frame = self.miniature_frames[self.current_slide_index]
                old_frame.configure(border_color=self.default_border_color)

            if 0 <= new_slide_index < len(self.miniature_frames):
                new_frame = self.miniature_frames[new_slide_index]
                new_frame.configure(border_color=self.highlight_color)
            
            self.current_slide_index = new_slide_index

        if self.callback_goto_slide:
            self.callback_goto_slide(new_slide_index)
        
    def update_current_selection_highlight(self, new_current_index):
        """
        Chamado pela MainWindow se o slide for alterado por outros meios 
        (ex: botões Próximo/Anterior na MainWindow ou IA), 
        para que esta janela de visualização reflita a seleção.
        """

        if new_current_index != self.current_slide_index:
            if 0 <= self.current_slide_index < len(self.miniature_frames):
                self.miniature_frames[self.current_slide_index].configure(border_color=self.default_border_color)
            
            if 0 <= new_current_index < len(self.miniature_frames):
                self.miniature_frames[new_current_index].configure(border_color=self.highlight_color)
            
            self.current_slide_index = new_current_index

    def on_close(self):
        self.destroy()

    def _center_window_on_master(self):
        self.after(20, self._do_center) 

    def _do_center(self):
        try:
            self.update_idletasks() 
            if not self.master or not self.master.winfo_exists(): return

            master_x = self.master.winfo_x()
            master_y = self.master.winfo_y()
            master_width = self.master.winfo_width()
            master_height = self.master.winfo_height()

            dialog_width = self.winfo_width()
            dialog_height = self.winfo_height()

            if dialog_width <= 1 or dialog_height <= 1:
                self.after(50, self._do_center)
                return

            x = master_x + (master_width - dialog_width) // 2
            y = master_y + (master_height - dialog_height) // 2
            
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = max(0, min(x, screen_width - dialog_width))
            y = max(0, min(y, screen_height - dialog_height))
            
            self.geometry(f"+{x}+{y}")
        except Exception:
            pass