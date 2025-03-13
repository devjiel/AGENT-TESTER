# Agent Tester

Un agent automatisé pour tester des interfaces web avec Claude et LangChain.

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Une clé API Anthropic (pour Claude)

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/devjiel/agent-tester.git
cd agent-tester
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Exporter votre clé API Anthropic :
```bash
# Sur Windows (PowerShell)
$env:ANTHROPIC_API_KEY="votre-clé-api"

# Sur Linux/Mac
export ANTHROPIC_API_KEY="votre-clé-api"
```

2. Configurer l'application dans `config.yaml` :
```yaml
paths:
  data_dir: "data"  # Répertoire principal des données

browser:
  url: "https://www.google.fr"
  wait_time: 2
```

Le système crée automatiquement les sous-répertoires suivants :
- `data/screenshots` : pour les captures d'écran
- `data/analyses` : pour les analyses d'interface

## Utilisation

Lancer le script principal :
```bash
python main.py
```

## Structure du Projet

- `main.py` : Point d'entrée de l'application
- `orchestrator.py` : Gestion du workflow d'automatisation
- `agent_analyzer.py` : Analyse des captures d'écran avec Claude
- `agent_ui_automation.py` : Automatisation de l'interface utilisateur
- `screen_utils.py` : Utilitaires de capture d'écran
- `browser_utils.py` : Utilitaires de navigation web
- `config.yaml` : Configuration de l'application
- `utils/config_loader.py` : Utilitaire de chargement de la configuration avec fonctions pour accéder aux chemins