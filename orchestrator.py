"""
Module d'orchestration
"""
from agent_ui_automation import process_ui_action
from agent_analyzer import analyze_screenshot
from browser_utils import open_google
from screen_utils import take_screenshot
from paths import INTERFACE_DESCRIPTION_FILE

class Orchestrator:
    def __init__(self):
        self.interface_description_path = INTERFACE_DESCRIPTION_FILE

    def open_browser(self):
        """Ouvre le navigateur sur Google"""
        if not open_google():
            raise Exception("Impossible d'ouvrir le navigateur sur Google")

    def capture_screen(self):
        """Capture l'écran actuel"""
        screenshot_path = take_screenshot()
        if screenshot_path is None:
            raise Exception("Impossible de prendre une capture d'écran")
        return screenshot_path

    def analyze_interface(self):
        """Analyse l'interface et génère une description"""
        if not analyze_screenshot():
            raise Exception("Erreur lors de l'analyse de l'interface")

    def read_interface_description(self):
        """Lit la description de l'interface"""
        try:
            with open(self.interface_description_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture de la description : {str(e)}")

    def execute_search(self, search_query: str):
        """Exécute une recherche Google"""
        try:
            interface_description = self.read_interface_description()
            result = process_ui_action(interface_description, search_query)
            return result["output"]
        except Exception as e:
            raise Exception(f"Erreur lors de l'exécution de la recherche : {str(e)}")

    def run_workflow(self, search_query: str):
        """Exécute le workflow complet"""
        try:
            print("1. Ouverture du navigateur...")
            self.open_browser()

            print("2. Capture d'écran...")
            self.capture_screen()

            print("3. Analyse de l'interface...")
            self.analyze_interface()

            print("4. Exécution de la recherche...")
            result = self.execute_search(search_query)
            
            print("\nRésultat :")
            print(result)
            
            return True
            
        except Exception as e:
            print(f"Erreur dans le workflow : {str(e)}")
            return False 