from .openai_client import OpenAIClient
from .web_scraper import perform_web_search
import sys

# Encoding-sichere Ausgabe
def safe_print(text):
    """Druckt Text mit Encoding-Fallback"""
    if isinstance(text, str):
        try:
            print(text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
        except:
            print(text)
    else:
        print(text)

class ChatBot:
    def __init__(self, api_key=None):
        self.openai_client = OpenAIClient(api_key=api_key)
    
    def chat_with_internet(self, message):
        """Chat-Funktion mit Internet-Suche wenn nötig"""
        try:
            # Encoding-sichere Nachricht
            message = message.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            
            # Analysiere ob Web-Suche benötigt wird
            analysis = self.openai_client.analyze_search_need(message)
            
            context = ""
            used_search = False
            
            if analysis.startswith("SEARCH:"):
                search_query = analysis.replace("SEARCH:", "").strip()
                safe_print(f"Suche nach: {search_query}")
                
                # Führe Web-Suche durch
                search_results = perform_web_search(search_query)
                
                if search_results:
                    used_search = True
                    context = "\n\nRelevante Informationen aus Web-Suche:\n"
                    for i, result in enumerate(search_results, 1):
                        # Encoding-sichere Text-Extraktion
                        title = result.get('title', '')
                        snippet = result.get('snippet', '')
                        
                        # Encoding-sichere String-Verarbeitung
                        if isinstance(title, str):
                            title = title.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                        if isinstance(snippet, str):
                            snippet = snippet.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                        
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
                "error": str(e)
            }