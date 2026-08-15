from .openai_client import OpenAIClient
from .web_scraper import perform_web_search

class ChatBot:
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    def chat_with_internet(self, message):
        """Chat-Funktion mit Internet-Suche wenn nötig"""
        try:
            # Analysiere ob Web-Suche benötigt wird
            analysis = self.openai_client.analyze_search_need(message)
            
            context = ""
            used_search = False
            
            if analysis.startswith("SEARCH:"):
                search_query = analysis.replace("SEARCH:", "").strip()
                print(f"Suche nach: {search_query}")
                
                # Führe Web-Suche durch
                search_results = perform_web_search(search_query)
                
                if search_results:
                    used_search = True
                    context = "\n\nRelevante Informationen aus Web-Suche:\n"
                    for i, result in enumerate(search_results, 1):
                        context += f"\n{i}. {result['title']}\n{result['snippet']}\n"
            
            # Generiere Antwort mit oder ohne Kontext
            result = self.openai_client.chat_with_context(message, context)
            
            if result["success"]:
                result["used_web_search"] = used_search
                return result
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }