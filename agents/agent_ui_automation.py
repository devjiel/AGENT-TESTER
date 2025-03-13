"""
Module d'automatisation UI
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import pyautogui
import time
import re
import json
from utils.config_loader import ConfigLoader
from clients.langchain_client import get_chat_model

# Initialisation
config = ConfigLoader()

# Chargement des paramètres de calibration
OFFSET_X = 0
OFFSET_Y = 0
SCALE_X = 1.0
SCALE_Y = 1.0

# Fonction pour simuler un clic
def click_action(coordinates):
    try:
        # Extraire les coordonnées avec regex pour supporter différents formats
        # Formats supportés : "x = 123, y = 456", "x = 123 y = 456", "123, 456", "x≈123, y≈456"
        
        # Recherche des nombres avec regex
        numbers = re.findall(r'\d+', coordinates)
        
        if len(numbers) >= 2:
            x = int(numbers[0])
            y = int(numbers[1])
        else:
            raise ValueError(f"Format de coordonnées non reconnu: {coordinates}")
            
        # Ajouter un petit délai pour la sécurité
        time.sleep(0.5)
        
        # Déplacer la souris et cliquer
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click()
        
        return f"Clic effectué aux coordonnées ({x}, {y})"
    except Exception as e:
        return f"Erreur lors du clic: {str(e)}"

# Fonction pour simuler la saisie de texte
def type_text(text):
    try:
        # Ajouter un petit délai pour la sécurité
        time.sleep(0.5)
        # Saisir le texte
        pyautogui.typewrite(text, interval=0.1)
        return f"Texte saisi : {text}"
    except Exception as e:
        return f"Erreur lors de la saisie du texte : {str(e)}"

# Création des outils
tools = [
    Tool(
        name="ClickAt",
        func=click_action,
        description="Clique à une position spécifique. Input format: 'x,y'"
    ),
    Tool(
        name="TypeText",
        func=type_text,
        description="Saisit du texte dans un champ. Input: le texte à saisir"
    )
]

# Définition du template pour le prompt
template = """Tu es un assistant qui aide à interagir avec une interface utilisateur.
Tu dois analyser le texte fourni qui décrit une interface et effectuer les actions nécessaires.

Pour effectuer une recherche Google, tu dois :
1. Cliquer sur la barre de recherche Google
2. Saisir le texte de la recherche

Tu as accès aux outils suivants:
{tools}

Utilise le format suivant:

Question: la question à répondre
Thought: tu devrais toujours penser à ce qu'il faut faire
Action: l'action à prendre, devrait être une des [{tool_names}]
Action Input: l'entrée à l'action
Observation: le résultat de l'action
... (ce format Thought/Action/Action Input/Observation peut se répéter N fois)
Thought: J'ai maintenant la réponse finale
Final Answer: la réponse finale à la question

Question: {input}
{agent_scratchpad}"""

# Création du prompt
prompt = PromptTemplate(template=template, input_variables=["input", "tools", "tool_names", "agent_scratchpad"])

# Création de l'agent
agent = create_react_agent(
    llm=get_chat_model(),
    tools=tools,
    prompt=prompt
)

# Création de l'exécuteur d'agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Fonction principale pour utiliser l'agent
def process_ui_action(text: str, search_query: str, calibration=None):
    """
    Traite une requête utilisateur et effectue les actions nécessaires sur l'interface
    
    Args:
        text (str): Description de l'interface
        search_query (str): Requête de l'utilisateur
        calibration (dict, optional): Paramètres de calibration. Exemple: {'offset_x': 5, 'offset_y': -10}
    
    Returns:
        dict: Résultat des actions effectuées
    """
    # Appliquer la calibration si fournie
    if calibration:
        set_calibration(
            calibration.get('offset_x', OFFSET_X),
            calibration.get('offset_y', OFFSET_Y),
            calibration.get('scale_x', SCALE_X),
            calibration.get('scale_y', SCALE_Y)
        )
    
    # Ajouter des instructions supplémentaires pour améliorer la précision
    enhanced_prompt = f"""
À partir de cette description d'interface : 
{text}

Effectue une recherche Google avec le texte : {search_query}

ATTENTION: La précision des coordonnées est cruciale. Assure-toi de cliquer exactement aux coordonnées spécifiées.
Utilise les coordonnées exactes fournies dans la description de l'interface.
"""
    
    # Exécuter l'agent avec le prompt amélioré
    return agent_executor.invoke({
        "input": enhanced_prompt,
        "tools": ", ".join([tool.name for tool in tools]),
        "tool_names": ", ".join([f"'{tool.name}'" for tool in tools]),
        "agent_scratchpad": ""
    })

def set_calibration(offset_x=0, offset_y=0, scale_x=1.0, scale_y=1.0):
    """
    Définit les paramètres de calibration pour les coordonnées
    
    Args:
        offset_x (int): Décalage horizontal en pixels
        offset_y (int): Décalage vertical en pixels
        scale_x (float): Facteur d'échelle horizontal
        scale_y (float): Facteur d'échelle vertical
    """
    global OFFSET_X, OFFSET_Y, SCALE_X, SCALE_Y
    OFFSET_X = offset_x
    OFFSET_Y = offset_y
    SCALE_X = scale_x
    SCALE_Y = scale_y
    
    print(f"Nouveaux paramètres de calibration appliqués:")
    print(f"Décalage: ({offset_x}, {offset_y}) pixels")
    print(f"Échelle: ({scale_x}, {scale_y})")

def load_calibration(file_path='calibration.json'):
    """
    Charge les paramètres de calibration depuis un fichier JSON
    
    Args:
        file_path (str): Chemin vers le fichier de calibration
    """
    import os
    if not os.path.exists(file_path):
        print(f"Fichier de calibration {file_path} non trouvé, utilisation des valeurs par défaut")
        return
    
    try:
        with open(file_path, 'r') as f:
            params = json.load(f)
            set_calibration(
                params.get('offset_x', 0),
                params.get('offset_y', 0),
                params.get('scale_x', 1.0),
                params.get('scale_y', 1.0)
            )
    except Exception as e:
        print(f"Erreur lors du chargement des paramètres de calibration: {str(e)}")

def save_calibration(file_path='calibration.json'):
    """
    Enregistre les paramètres de calibration actuels dans un fichier JSON
    
    Args:
        file_path (str): Chemin vers le fichier de calibration
    """
    try:
        params = {
            'offset_x': OFFSET_X,
            'offset_y': OFFSET_Y,
            'scale_x': SCALE_X,
            'scale_y': SCALE_Y
        }
        with open(file_path, 'w') as f:
            json.dump(params, f, indent=2)
        print(f"Paramètres de calibration enregistrés dans {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des paramètres de calibration: {str(e)}")

# Essayer de charger les paramètres de calibration au démarrage
try:
    load_calibration()
except Exception as e:
    print(f"Erreur lors du chargement initial de la calibration: {str(e)}") 