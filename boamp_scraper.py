import requests
from datetime import datetime, timedelta

def scrape_boamp(keyword="site web"):
    # On cherche sur 30 jours pour être sûr d'avoir des résultats
    date_min = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    url = "https://api.dila.fr/opendata/boamp/v1.1/search"
    
    # On teste avec et sans majuscule pour le mot-clé
    params = {"keyword": keyword.lower(), "datemiseaservice_min": date_min}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # On augmente le timeout à 30 secondes car les serveurs de l'État rament souvent
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return []

        data = response.json()
        items = data.get('item', [])
        
        if not items:
            return []

        if isinstance(items, dict):
            items = [items]

        results = []
        for item in items[:8]:
            results.append({
                'id': str(item.get('id')),
                'titre': item.get('titre', 'Marché Public'),
                'objet': item.get('objet', 'Pas de description'),
                'link': f"https://www.boamp.fr/pages/avis/?idweb={item.get('id')}"
            })
        return results
    except Exception as e:
        print(f"Erreur API : {e}")
        return []