"""
Utilitários para diálogos.

Este módulo fornece funções centralizadas para operações comuns com diálogos,
eliminando duplicação de código.
"""

import logging

logger = logging.getLogger(__name__)


def center_dialog(dialog, master):
    """
    Centraliza uma janela de diálogo em relação à janela mestre.
    
    Calcula a posição centralizada da janela de diálogo baseada na posição
    e tamanho da janela mestre. Lida com casos edge como janela minimizada.
    
    Args:
        dialog: Janela de diálogo a ser centralizada (deve ter métodos winfo_*)
        master: Janela mestre em relação à qual centralizar (deve ter métodos winfo_*)
    
    Examples:
        >>> from gui.utils.dialog_utils import center_dialog
        >>> dialog = AddEditSongDialog(master)
        >>> center_dialog(dialog, master)
        # Centraliza o diálogo na janela mestre
    """
    try:
        dialog.update_idletasks()
        
        # Obter posição e tamanho da janela mestre
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_w = master.winfo_width()
        master_h = master.winfo_height()
        
        # Obter tamanho da janela de diálogo
        dialog_w = dialog.winfo_width()
        dialog_h = dialog.winfo_height()
        
        # Verificar se as dimensões são válidas (evitar erro se janela minimizada)
        if dialog_w <= 1 or dialog_h <= 1:
            logger.debug("Dimensões do diálogo inválidas, tentando novamente...")
            # Tentar novamente após um pequeno delay (pode ser chamado via after())
            if hasattr(dialog, 'after'):
                dialog.after(50, lambda: center_dialog(dialog, master))
            return
        
        # Calcular posição centralizada
        x = master_x + (master_w - dialog_w) // 2
        y = master_y + (master_h - dialog_h) // 2
        
        # Aplicar posição
        dialog.geometry(f"+{x}+{y}")
    except Exception as e:
        # Se algo der errado (ex: janela principal minimizada), apenas loga e ignora
        logger.debug(f"Erro ao centralizar diálogo: {e}")

