import feedparser
import json
import os

# --- CONFIGURATION ---

# Mots-clés pour la veille générale
mots_cles = ["faille", "ransomware", "exploit", "zero-day", "vulnerabilité", "hack", "fuite", "donnée", "sensible", "personnelle", "cert", "cyber"]

# Mots-clés pour déclencher le badge "CRITIQUE"
mots_critiques = ["critique", "rce", "exécution de code", "zero-day", "0-day", "vulnérabilité critique", "activement exploitée"]

# Liste de tes sources de confiance
liste_flux = [
    "https://www.cert.ssi.gouv.fr/feed/", 
    "https://sec.cloudapps.cisco.com/security/center/psirtrss20/CiscoSecurityAdvisory.xml", 
    "https://www.networkworld.com/feed/", 
    "https://korben.info/feed", 
    "https://www.zataz.com/feed/", 
    "https://thehackernews.com/feeds/posts/default", 
    "https://incyber.org/feed/", 
    "https://krebsonsecurity.com/feed/", 
    "http://googleprojectzero.blogspot.com/feeds/posts/default" 
]

# Chemin vers ton dossier portfolio sur Arch Linux
CHEMIN_DESTINATION = '/srv/http/portfolio/data_veille.json'

def recuperer_veille():
    resultats = []
    
    print("--- DÉMARRAGE DE TECHWATCH_PRO ---")
    
    for url in liste_flux:
        print(f"Analyse de : {url}")
        try:
            flux = feedparser.parse(url)
            
            for entry in flux.entries:
                # On récupère le texte global pour l'analyse
                titre = entry.title
                resume = entry.get('summary', '')
                texte_complet = (titre + " " + resume).lower()
                
                # 1. Vérification de la pertinence (Veille Cyber)
                if any(mot in texte_complet for mot in mots_cles):
                    
                    # 2. Analyse de la sévérité (Badge Critique)
                    is_critical = any(crit in texte_complet for crit in mots_critiques)
                    
                    article = {
                        "title": titre,
                        "link": entry.link,
                        "date": entry.get('published', 'Date inconnue'),
                        "source": flux.feed.get('title', 'Source inconnue'),
                        "summary": resume[:200] + "...",
                        "priority": "Haut" if is_critical else "Normal"
                    }
                    resultats.append(article)
                    
        except Exception as e:
            print(f"⚠️ Erreur sur le flux {url} : {e}")

    # --- SAUVEGARDE ---
    try:
        # On trie pour avoir les plus récents (optionnel selon le flux)
        # On sauvegarde les 6 plus pertinents
        with open(CHEMIN_DESTINATION, 'w', encoding='utf-8') as f:
            json.dump(resultats[:6], f, ensure_ascii=False, indent=4)
        
        print(f"\n✅ TERMINÉ : {len(resultats)} articles filtrés.")
        print(f"📂 Fichier mis à jour : {CHEMIN_DESTINATION}")
        
    except PermissionError:
        print(f"\n❌ ERREUR : Permission refusée sur {CHEMIN_DESTINATION}")
        print("💡 Commande à lancer : sudo chown -R $USER:$USER /srv/http/portfolio")

if __name__ == "__main__":
    recuperer_veille()
