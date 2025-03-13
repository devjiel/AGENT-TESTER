"""
Point d'entrée principal de l'application
"""
from orchestrator import Orchestrator

def main():
    # Initialiser l'orchestrateur
    orchestrator = Orchestrator()
    
    # Exécuter le workflow
    search_query = "Anthropic Claude"
    result = orchestrator.run_workflow(search_query)
    
    print(f"Résultat du workflow: {result}")

if __name__ == "__main__":
    main() 