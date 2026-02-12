import os
from openai import OpenAI
from dotenv import load_dotenv

# Charge les variables du fichier .env (pour le local)
load_dotenv()

# Récupère la clé API de manière sécurisée
# En local, il lira le fichier .env
# Sur Streamlit Cloud, il lira ce que tu as mis dans "Secrets"
api_key = os.getenv("OPENAI_API_KEY")

# Initialisation du client OpenAI
client = OpenAI(api_key=api_key)

def summarize_tender(text):
    """
    Analyse le texte brut d'un appel d'offres et génère un résumé structuré.
    """
    if not text or len(text) < 10:
        return "⚠️ Pas de description détaillée disponible pour cette offre."
    
    # Le Prompt : C'est ici qu'on définit la qualité de l'analyse "vendable"
    prompt = f"""Tu es un expert en marchés publics. 
    Résume l'offre suivante de manière ultra-claire pour un chef d'entreprise :
    
    1. 🎯 OBJET DU MARCHÉ : (L'essentiel en une phrase)
    2. 💰 BUDGET ESTIMÉ : (Indique le montant ou 'Non précisé')
    3. 📅 DATE LIMITE : (Indique la date exacte de dépôt)
    
    Texte de l'annonce : 
    {text[:2000]}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant business concis et précis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur d'analyse IA : {str(e)}"