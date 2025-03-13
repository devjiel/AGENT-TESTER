"""
Module pour l'intégration de LangChain avec Anthropic
"""
import os
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from utils.config_loader import ConfigLoader

# Initialisation de la configuration
config = ConfigLoader()

def get_chat_model(temperature: float = 0.7, max_tokens_to_sample: int = 1000) -> ChatAnthropic:
    """
    Obtient un modèle de chat Anthropic via LangChain
    
    Args:
        temperature (float): Température pour la génération de texte
        max_tokens_to_sample (int): Nombre maximum de tokens à générer
        
    Returns:
        ChatAnthropic: Le modèle de chat Anthropic
    """
    # Vérifier que la clé API est présente
    if "ANTHROPIC_API_KEY" not in os.environ:
        raise ValueError("La clé API Anthropic n'est pas définie. Utilisez: export ANTHROPIC_API_KEY=votre-clé")
    
    return ChatAnthropic(
        model_name="claude-3-sonnet-20240229",
        temperature=temperature,
        max_tokens_to_sample=max_tokens_to_sample,
        timeout=60,
        stop=None
    )