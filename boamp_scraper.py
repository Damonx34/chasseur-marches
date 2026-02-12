import requests
from datetime import datetime, timedelta

def scrape_boamp(keyword="site web"):
    print(f"--- 🛰️ DÉBUT DU SCAN POUR : {keyword} ---")
    
    # On réduit à 15 jours pour que la réponse soit plus légère
    date_min = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    url = "https://api.dila.fr/opendata/boamp/v1.1/search"
    
    params = {
        "keyword": keyword,
        "datemiseaservice_min": date_min
    }

    try:
        print("📡 Envoi de la requête à l'API...")
        # On réduit le timeout à 10 secondes pour ne pas attendre pour rien
        response = requests.get(url, params=params, timeout=10)
        
        print(f"🌐 Code réponse : {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Le serveur BOAMP refuse la connexion.")
            return []

        data = response.json()
        items = data.get('item', [])
        
        if not items:
            print("Empty: Aucun marché trouvé pour ce mot-clé.")
            return []

        if isinstance(items, dict):
            items = [items]

        results = []
        for item in items[:5]: # On prend les 5 premiers pour tester
            results.append({
                'id': str(item.get('id')),
                'titre': item.get('titre', 'Sans titre'),
                'objet': item.get('objet', 'Pas de description'),
                'link': f"https://www.boamp.fr/pages/avis/?idweb={item.get('id')}"
            })
        
        print(f"✅ Succès : {len(results)} marchés récupérés.")
        return results

    except Exception as e:
        print(f"💥 ERREUR RÉSEAU : {e}")
        return []