import requests

def scrape_boamp(keyword="test"):
    url = f"https://www.boamp.fr/pages/recherche/?q={keyword}"
    # On utilise un User-Agent très standard
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # On tente de joindre le site
        response = requests.get(url, headers=headers, timeout=15)
        
        # On crée un résultat qui nous affiche le code HTTP reçu
        return [{
            "id": "DEBUG",
            "titre": f"DIAGNOSTIC : Code {response.status_code}",
            "objet": "Si le code est 403, Streamlit est bloqué. Si c'est 200, le site répond mais on lit mal les données.",
            "link": "#"
        }]
    except Exception as e:
        return [{
            "id": "ERROR",
            "titre": "Erreur de connexion",
            "objet": str(e),
            "link": "#"
        }]