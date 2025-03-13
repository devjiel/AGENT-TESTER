"""
Module pour l'automatisation du navigateur
"""
import webbrowser
import time
from utils.config_loader import ConfigLoader

# Initialisation de la configuration
config = ConfigLoader()

def open_url():
    """
    Ouvre le navigateur par défaut sur l'URL spécifiée dans la configuration
            
    Returns:
        bool: True si le navigateur a été ouvert avec succès, False sinon
    """
    try:
        # Ouvre l'URL dans le navigateur par défaut
        url = config.browser.get("url", "https://www.google.com")
        webbrowser.open(url)
        
        # Attendre que la page se charge
        time.sleep(config.browser.get("wait_time", 2))
        
        print(f"Navigateur ouvert sur {url}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'ouverture du navigateur : {str(e)}")
        return False 