"""
Module pour l'automatisation du navigateur
"""
import webbrowser
import time
import yaml

def load_config():
    """Charge la configuration depuis config.yaml"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def open_google():
    """
    Ouvre le navigateur par défaut sur l'URL configurée
    """
    try:
        config = load_config()
        # Ouvre l'URL dans le navigateur par défaut
        webbrowser.open(config["browser"]["url"])
        
        # Attendre que la page se charge
        time.sleep(config["browser"]["wait_time"])
        
        print(f"Navigateur ouvert sur {config['browser']['url']}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'ouverture du navigateur : {str(e)}")
        return False 