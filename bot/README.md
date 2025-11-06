# LinearBot

Mattermost's bot for Linear pour la gestion des issues Linear depuis les conversations Mattermost.

## Fonctionnalités
- `/linear set-team YYY` : Associe la team Mattermost à la team Linear
- `/linear create "Titre"` : Crée une issue dans Linear
- `/linear list status` : Liste les issues par statut
- Webhook pour recevoir les updates Linear et les publier sur Mattermost

## Configuration
- Les credentials et paramètres sont passés en variables d'environnement :
  - `LINEAR_API_TOKEN` : Token API Linear
  - `MATTERMOST_TOKEN` : Token Bot Mattermost
  - `MATTERMOST_URL` : URL du serveur Mattermost
  - `LINEARBOT_CONFIG_PATH` : Chemin du fichier de configuration

## Démarrage
```bash
# Construire le conteneur
cd bot
sudo docker build -t linearbot .

# Lancer le bot
sudo docker run -e LINEAR_API_TOKEN=... -e MATTERMOST_TOKEN=... -e MATTERMOST_URL=... -e LINEARBOT_CONFIG_PATH=/app/config.json -p 8080:8080 linearbot
```
