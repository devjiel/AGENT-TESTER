"""
Module d'analyse des captures d'écran
"""
import os
import base64
from PIL import Image
from clients.langchain_client import get_chat_model
from utils.config_loader import ConfigLoader
from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage

# Initialisation de la configuration
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
            
        # Créer le prompt pour l'analyse
        prompt = f"""Analyse cette capture d'écran et DÉCRIS UNIQUEMENT LES ÉLÉMENTS INTERACTIFS DE L'INTERFACE UTILISATEUR DE L'APPLICATION TESTÉE.

CONCENTRE-TOI EXCLUSIVEMENT sur les éléments suivants:
- Boutons (boutons de navigation, boutons d'action, etc.)
- Champs de saisie de texte
- Menus déroulants
- Cases à cocher
- Boutons radio
- Sliders
- Onglets
- Liens cliquables
- Images cliquables
- Icônes interactives
- Texte statique

IGNORE COMPLÈTEMENT les éléments suivants:
- Éléments de l'interface du navigateur (barre d'adresse, boutons du navigateur)
- Arrière-plans et décorations
- Tout élément qui n'est pas interactif

Pour chaque élément interactif, donne la position de son centre EXACTE avec des coordonnées x,y au pixel près.
La taille de l'écran est de {width} x {height} pixels.

IMPORTANT: La précision des coordonnées est CRUCIALE car elles seront utilisées pour des clics automatisés. 
Fournis les coordonnées les plus précises possible AU PIXEL PRÈS. N'arrondis pas et n'approxime pas.

Organise ta réponse de manière structurée, en regroupant les éléments par type:
Pour chaque élément interactif, indique:
1. Son type (ex: bouton, champ texte, case à cocher)
2. Son contenu ou libellé
3. Sa position exacte en pixels (x, y) - DOIT ÊTRE PRÉCIS
4. Son état (actif, inactif, coché, etc.)
5. Sa taille approximative en pixels (largeur x hauteur) si visible

Format à utiliser pour chaque élément:
[Type d'élément]
Position: x = X, y = Y (exactement, pas approximativement)
Taille: largeur x hauteur pixels
Description: [description détaillée]
État: [si applicable]"""

        # Vérifier que l'image existe
        if not os.path.exists(screenshot_path):
            raise FileNotFoundError(f"L'image {screenshot_path} n'existe pas")
        
        # Lire l'image et la convertir en base64
        with open(screenshot_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Vérifier que la clé API est présente
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise ValueError("La clé API Anthropic n'est pas définie. Utilisez: export ANTHROPIC_API_KEY=votre-clé")
        
        
        # Créer les messages pour le chat
        messages = [
            SystemMessage(content="Vous êtes un assistant spécialisé dans l'analyse d'interfaces utilisateur pour l'automatisation de tests. Vous identifiez UNIQUEMENT les éléments interactifs avec lesquels un utilisateur peut interagir."),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ])
        ]
        
        # Obtenir la réponse du modèle
        response = get_chat_model().invoke(messages)
        
        # Extraire le contenu de la réponse
        analysis = None
        if hasattr(response, 'content'):
            analysis = str(response.content)
        
        # Sauvegarder l'analyse
        if analysis and save_analysis(analysis):
            print("Analyse terminée avec succès")
            return True
        else:
            print("Échec de l'analyse de l'image")
            
    except Exception as e:
        print(f"Erreur lors de l'analyse : {str(e)}")
        print(f"Type d'erreur : {type(e)}")
        
    return False