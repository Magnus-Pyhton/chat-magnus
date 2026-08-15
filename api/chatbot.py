from .openai_client import OpenAIClient
from .web_scraper import perform_web_search, safe_print, safe_text
import os

# Encoding auf UTF-8 erzwingen
os.environ['PYTHONIOENCODING'] = 'utf-8'

class ChatBot:
    def __init__(self, api_key=None):
        self.openai_client = OpenAIClient(api_key=api_key)
    
    def chat_with_internet(self, message):
        """Chat-Funktion mit Internet-Suche wenn nötig"""
        try:
            # Encoding-sichere Nachricht
            message = safe_text(message)
            
            # Analysiere ob Web-Suche benötigt wird
            analysis = self.openai_client.analyze_search_need(message)
            
            context = ""
            used_search = False
            
            if analysis.startswith("SEARCH:"):
                search_query = safe_text(analysis.replace("SEARCH:", "").strip())
                safe_print(f"Suche nach: {search_query}")
                
                # Führe Web-Suche durch
                search_results = perform_web_search(search_query)
                
                if search_results:
                    used_search = True
                    context = "\n\nRelevante Informationen aus Web-Suche:\n"
                    for i, result in enumerate(search_results, 1):
                        # Encoding-sichere Text-Extraktion
                        title = safe_text(result.get('title', ''))
                        snippet = safe_text(result.get('snippet', ''))
                        
                        context += f"\n{i}. {title}\n{snippet}\n"
            
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
                "error": safe_text(str(e))
            }