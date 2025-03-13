"""
Module de gestion des chemins
"""
import os

# Chemins des répertoires de données
DATA_DIR = "data"
SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
ANALYSES_DIR = os.path.join(DATA_DIR, "analyses")

# Chemins des fichiers
INTERFACE_DESCRIPTION_FILE = os.path.join(ANALYSES_DIR, "interface_description.txt") 