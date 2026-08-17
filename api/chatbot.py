from .openai_client import OpenAIClient

class ChatBot:
    def __init__(self, api_key=None):
        self.openai_client = OpenAIClient(api_key=api_key)
    
    def chat_with_internet(self, message):
        """Chat-Funktion ohne Web-Suche-Analyse (um Encoding-Probleme zu vermeiden)"""
        try:
            # Direkte Antwort ohne Such-Analyse
            result = self.openai_client.chat_with_context(message, "")
            
            if result["success"]:
                result["used_web_search"] = False
                return result
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }