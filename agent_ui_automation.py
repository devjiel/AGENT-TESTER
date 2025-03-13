"""
Module d'automatisation UI
"""
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import pyautogui
import time

# Création du modèle Claude
model = ChatAnthropic(
    model_name="claude-3-sonnet-20240229",
    timeout=60,
    stop=None
)

# Fonction pour simuler un clic
def click_action(coordinates):
    try:
        # Gestion des coordonnées au format "x ≈ 597, y ≈ 474"
        if '≈' in coordinates:
            x = int(coordinates.split(',')[0].split('≈')[1].strip())
            y = int(coordinates.split(',')[1].split('≈')[1].strip())
        # Gestion des coordonnées au format simple "597,474"
        else:
            x = int(coordinates.split(',')[0].strip())
            y = int(coordinates.split(',')[1].strip())
            
        # Ajouter un petit délai pour la sécurité
        time.sleep(0.5)
        # Déplacer la souris et cliquer
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click()
        return f"Clic effectué aux coordonnées ({x}, {y})"
    except (ValueError, IndexError) as e:
        return f"Erreur de format des coordonnées. Format attendu: 'x,y' ou 'x ≈ X, y ≈ Y'. Erreur: {str(e)}"

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
    llm=model,
    tools=tools,
    prompt=prompt
)

# Création de l'exécuteur d'agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Fonction principale pour utiliser l'agent
def process_ui_action(text: str, search_query: str):
    return agent_executor.invoke({
        "input": f"À partir de cette description d'interface : {text}\nEffectue une recherche Google avec le texte : {search_query}",
        "tools": ", ".join([tool.name for tool in tools]),
        "tool_names": ", ".join([f"'{tool.name}'" for tool in tools]),
        "agent_scratchpad": ""
    }) 