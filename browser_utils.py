"""
Module pour l'automatisation du navigateur
"""
import webbrowser
import time
from utils.config_loader import ConfigLoader

def open_google():
    """
    Ouvre le navigateur par défaut sur l'URL configurée
    """
    try:
        config = ConfigLoader()
        browser_config = config.browser
        
        # Ouvre l'URL dans le navigateur par défaut
        webbrowser.open(browser_config["url"])
        
        # Attendre que la page se charge
        time.sleep(browser_config["wait_time"])
        
        print(f"Navigateur ouvert sur {browser_config['url']}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'ouverture du navigateur : {str(e)}")
        return False 