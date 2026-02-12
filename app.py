import asyncio
import sys

if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass

import streamlit as st
from boamp_scraper import scrape_boamp
from ai_summarizer import summarize_tender
from database import setup_db, save_annonce, get_all_annonces

st.set_page_config(page_title="Chasseur de Marchés", page_icon="🎯")
setup_db()

st.title("🎯 Chasseur de Marchés Publics")

keyword = st.text_input("Rechercher un métier")

if st.button("Lancer la détection 🚀"):
    if keyword:
        # On utilise st.write au lieu de status pour éviter le bug d'affichage
        message_zone = st.info("⏳ Recherche en cours... regarde ton terminal VS Code pour le détail.")
        
        tenders = scrape_boamp(keyword)
        
        if tenders:
            for t in tenders:
                resume = summarize_tender(t['objet'])
                save_annonce(t['id'], t['titre'], resume, t['link'])
            message_zone.success("✅ Terminé ! Actualisation...")
            st.rerun()
        else:
            message_zone.error("❌ Échec : Le site BOAMP ne répond pas ou aucun résultat.")
    else:
        st.warning("Écris un mot-clé !")

st.divider()

# Affichage simple
annonces = get_all_annonces()
for titre, resume, lien, date in annonces:
    with st.expander(f"📌 {titre}"):
        st.write(resume)
        st.link_button("Voir l'offre", lien)