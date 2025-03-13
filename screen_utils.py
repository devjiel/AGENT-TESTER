"""
Module pour la capture d'ecran
"""
from PIL import ImageGrab
from datetime import datetime
import os
from paths import SCREENSHOTS_DIR

def take_screenshot(directory=SCREENSHOTS_DIR):
    """
    Prend une capture d'ecran et la sauvegarde dans le dossier specifie
    
    Args:
        directory (str): Le dossier ou sauvegarder les captures d'ecran
    
    Returns:
        str: Le chemin du fichier de la capture d'ecran
    """
    try:
        # Creer le dossier s'il n'existe pas
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Generer un nom de fichier unique avec la date et l'heure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(directory, filename)
        
        # Prendre la capture d'ecran avec PIL
        screenshot = ImageGrab.grab()
        
        # Sauvegarder l'image
        screenshot.save(filepath)
        
        print(f"Capture d'ecran sauvegardee : {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Erreur lors de la capture d'ecran : {str(e)}")
        return None 