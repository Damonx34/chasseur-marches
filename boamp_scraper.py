import requests
from bs4 import BeautifulSoup
import random

def scrape_boamp(keyword="informatique"):
    print(f"--- 🕵️ SCRAPING DIRECT DU BOAMP POUR : {keyword} ---")
    
    # URL de recherche directe sur le site (pas l'API)
    url = f"https://www.boamp.fr/pages/recherche/?q={keyword}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.google.com/"
    }

    try:
        # On tente de récupérer la page
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ Erreur site : {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche les cartes d'annonces (les classes du BOAMP)
        items = soup.find_all('div', class_='list-item')
        
        if not items:
            print("⚠️ Aucune annonce visible sur la page.")
            return []

        results = []
        for item in items[:6]: # On prend les 6 premières
            try:
                title_tag = item.find('h2', class_='item-title') or item.find('a')
                link_tag = item.find('a', href=True)
                content_tag = item.find('div', class_='item-content')
                
                if title_tag and link_tag:
                    results.append({
                        'id': str(random.randint(100000, 999999)),
                        'titre': title_tag.get_text().strip(),
                        'objet': content_tag.get_text().strip() if content_tag else "Consultez l'annonce pour plus de détails.",
                        'link': "https://www.boamp.fr" + link_tag['href']
                    })
            except Exception:
                continue
                
        print(f"✅ {len(results)} annonces extraites par scraping !")
        return results

    except Exception as e:
        print(f"💥 Erreur Scraping : {e}")
        return []