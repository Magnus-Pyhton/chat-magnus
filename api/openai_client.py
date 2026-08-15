import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY nicht gefunden. Bitte in .env Datei setzen.")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_code(self, prompt, language="auto"):
        """Generiert Code basierend auf einer Beschreibung"""
        try:
            system_prompt = f"Du bist ein Experte Programmierer. Schreibe sauberen, gut dokumentierten Code in {language if language != 'auto' else 'der gewünschten Sprache'}. Füge Kommentare hinzu und befolge Best Practices."
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                "success": True,
                "code": response.choices[0].message.content,
                "language": language
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def chat_with_context(self, message, context=""):
        """Chat-Funktion mit optionalem Kontext"""
        try:
            system_prompt = "Du bist ein hilfreicher Assistent. Wenn du Web-Suchergebnisse im Kontext hast, verwende sie für deine Antworten und zitiere sie angemessen."
            
            full_message = message
            if context:
                full_message = f"{message}\n\nKontext aus Web-Suche:\n{context}"
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_message}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_search_need(self, message):
        """Analysiert ob eine Web-Suche benötigt wird"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "Analysiere ob die Frage des Benutzers eine Web-Suche benötigt. Antworte mit 'SEARCH: <query>' wenn Suche nötig ist, oder 'DIRECT' wenn du aus deinem Wissen antworten kannst."
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            analysis = response.choices[0].message.content
            return analysis
        except Exception as e:
            return "DIRECT"  # Fallback zu direkter Antwort
    
    def generate_image(self, prompt, size="1024x1024", quality="standard", style="vivid"):
        """Generiert Bilder mit DALL-E 3"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size,
                quality=quality,
                style=style
            )
            
            images = []
            for img in response.data:
                images.append({
                    "url": img.url,
                    "revised_prompt": getattr(img, 'revised_prompt', prompt)
                })
            
            return {
                "success": True,
                "images": images
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def edit_image(self, image_data, prompt):
        """Bearbeitet vorhandene Bilder mit DALL-E 2"""
        try:
            # DALL-E 2 benötigt RGBA-Bilder
            from PIL import Image
            import io
            
            # Konvertiere zu RGBA
            img = Image.open(io.BytesIO(image_data))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Speichere als Bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            response = self.client.images.edit(
                image=img_bytes,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            images = []
            for img in response.data:
                images.append({
                    "url": img.url
                })
            
            return {
                "success": True,
                "images": images
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }