import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def safe_text(text):
    """Encoding-sichere Text-Konvertierung"""
    if text is None:
        return ""
    if isinstance(text, bytes):
        try:
            return text.decode('utf-8', errors='ignore')
        except:
            return text.decode('latin-1', errors='ignore')
    elif isinstance(text, str):
        return text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    else:
        return str(text)

def safe_print(text):
    """Encoding-sichere Print-Funktion"""
    if text is None:
        return
    text = safe_text(text)
    try:
        print(text)
    except Exception as e:
        pass  # Ignoriere Print-Fehler

def scrape_web(url):
    """Scrapt eine Webseite und extrahiert relevante Inhalte"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Explizites Encoding für deutsche Umlaute
        response.encoding = response.apparent_encoding
        if 'charset' not in response.headers.get('content-type', ''):
            response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
        
        # Entferne Scripts und Styles
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Extrahiere Informationen mit Encoding-Handling
        title = ""
        if soup.title:
            title = soup.title.string.strip() if soup.title.string else ""
        elif soup.h1:
            title = soup.h1.string.strip() if soup.h1.string else ""
        
        content = soup.get_text(separator=' ', strip=True)
        
        # Meta-Informationen
        meta_description = ""
        meta_keywords = ""
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_description = meta_desc.get('content', '')
        
        meta_key = soup.find('meta', attrs={'name': 'keywords'})
        if meta_key:
            meta_keywords = meta_key.get('content', '')
        
        # Links extrahieren mit Encoding-Handling
        links = []
        for link in soup.find_all('a', href=True):
            try:
                href = link['href']
                text = link.get_text(strip=True)
                if href and text:
                    absolute_url = urljoin(url, href)
                    # Encoding-sichere Text-Extraktion
                    if isinstance(text, str):
                        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                    links.append({"url": absolute_url, "text": text})
            except Exception as e:
                print(f"Fehler beim Extrahieren eines Links: {e}")
                continue
        
        return {
            "success": True,
            "url": url,
            "title": title,
            "content": content[:10000],  # Limitiere Content-Länge
            "meta": {
                "description": meta_description,
                "keywords": meta_keywords
            },
            "links": links[:20]  # Limitiere Anzahl Links
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def safe_print(text):
    """Encoding-sichere Print-Funktion"""
    if text is None:
        return
    text = safe_text(text)
    try:
        print(text)
    except Exception as e:
        print(f"Print-Fehler: {e}")

def perform_web_search(query):
    """Führt eine einfache Web-Suche durch (simuliert)"""
    # Encoding-sichere Query
    query = safe_text(query)
    
    # In einer echten Implementierung würde hier eine Search-API verwendet
    # Für dieses Beispiel verwenden wir DuckDuckGo und Google als Beispiele
    
    search_engines = [
        f"https://duckduckgo.com/html/?q={quote(query)}",
        f"https://www.google.com/search?q={quote(query)}"
    ]
    
    results = []
    
    for search_url in search_engines:
        try:
            scraped = scrape_web(search_url)
            if scraped["success"]:
                snippets = extract_search_snippets(scraped["content"])
                results.extend(snippets[:3])  # Max 3 Ergebnisse pro Engine
                
                if len(results) >= 5:
                    break
        except Exception as e:
            safe_print(f"Suchfehler für {search_url}: {e}")
    
    return results

def extract_search_snippets(html_content):
    """Extrahiert Suchergebnis-Snippets aus HTML"""
    snippets = []
    
    # Einfache Regex-basierte Extraktion für Suchergebnisse
    # Dies ist eine vereinfachte Implementierung
    title_pattern = r'<a[^>]*class="result__a"[^>]*>([^<]+)</a>'
    snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>([^<]+)</a>'
    
    titles = re.findall(title_pattern, html_content)
    descriptions = re.findall(snippet_pattern, html_content)
    
    for i, title in enumerate(titles[:5]):
        description = descriptions[i] if i < len(descriptions) else "Keine Beschreibung verfügbar"
        snippets.append({
            "title": title,
            "snippet": description
        })
    
    return snippets