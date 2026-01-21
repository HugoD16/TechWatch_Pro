# TechWatch_Pro
Agrégateur dynamique de veille en Cybersécurité.

## Fonctionnement
Ce projet utilise un script **Python** pour scanner des flux RSS (CERT-FR, etc.), filtre les alertes par mots-clés et génère un fichier JSON. L'interface **JavaScript** consomme ensuite ces données pour un affichage dynamique.

## 🛠️Stack
- Python (feedparser)
- JavaScript (Fetch API)
- Automation via Systemd Timer (Arch Linux)
