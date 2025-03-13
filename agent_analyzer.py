"""
Module d'analyse des captures d'écran
"""
from anthropic import Anthropic
import os
from PIL import Image
import base64
from utils.config_loader import ConfigLoader

# Création du client Anthropic
client = Anthropic()
config = ConfigLoader()

def read_latest_screenshot(directory=None):
    """
    Lit la capture d'écran la plus récente du dossier
    """
    try:
        # Utiliser le répertoire configuré si non spécifié
        if directory is None:
            directory = config.get_screenshots_dir()
            
        # Obtenir tous les fichiers du dossier
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
        if not files:
            return None
            
        # Trier par date de modification et prendre le plus récent
        latest_screenshot = max(files, key=os.path.getmtime)
        return latest_screenshot
    except Exception as e:
        print(f"Erreur lors de la lecture de la capture d'écran : {str(e)}")
        return None

def save_analysis(analysis, directory=None):
    """
    Sauvegarde l'analyse dans le fichier interface_description.txt
    """
    try:
        # Utiliser le répertoire configuré si non spécifié
        if directory is None:
            directory = config.get_analyses_dir()
            
        # Créer le dossier s'il n'existe pas
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        filepath = config.get_ui_description_path()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(analysis)
            
        print(f"Analyse sauvegardée dans : {filepath}")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'analyse : {str(e)}")
        return False

def analyze_screenshot():
    """
    Analyse la dernière capture d'écran et sauvegarde la description
    """
    # Récupérer la dernière capture d'écran
    screenshot_path = read_latest_screenshot()
    if not screenshot_path:
        print("Aucune capture d'écran trouvée")
        return False
        
    try:
        # Charger l'image pour obtenir ses dimensions
        with Image.open(screenshot_path) as img:
            width, height = img.size
            
        # Lire et encoder l'image en base64
        with open(screenshot_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
            
        # Créer le prompt pour l'analyse
        prompt = f"""Analyse cette capture d'écran de navigateur web et décris tous les éléments de l'interface utilisateur visibles concernant uniquement la page web affichée.
Pour chacun d'entre eux donne la position de leur centre avec une coordonnée x,y.
La taille de l'écran est de {width} x {height}.

Organise ta réponse de manière claire et structurée, en regroupant les éléments par type ou par zone logique.
Pour chaque élément, indique :
1. Son type (bouton, champ texte, image, etc.)
2. Son contenu ou libellé
3. Sa position exacte (x, y)
4. Son état si pertinent (actif, inactif, coché, etc.)

Format suggéré :
[Type d'élément]
Position: x ≈ X, y ≈ Y
Description: [description détaillée]
État: [si applicable]"""

        # Créer le message avec l'image
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )
        
        # Sauvegarder l'analyse
        if save_analysis(message.content[0].text):
            print("Analyse terminée avec succès")
            return True
            
    except Exception as e:
        print(f"Erreur lors de l'analyse : {str(e)}")
        print(f"Type d'erreur : {type(e)}")
        
    return False

if __name__ == "__main__":
    analyze_screenshot() 