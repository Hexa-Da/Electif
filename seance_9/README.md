# Application de Chat TCP - Séance 9

## Description

Application de chat en ligne de commande utilisant TCP/IP pour la communication avec un serveur distant. L'application utilise la bibliothèque `textual` pour l'interface utilisateur et `asyncio` pour la gestion asynchrone des connexions réseau.

## Fonctionnalités implémentées

### 1. Connexion au serveur (`connection`)
- Établit une connexion TCP asynchrone au serveur `vassor.org` sur le port `12346`
- Envoie les identifiants (login et password) au format JSON
- Reçoit et vérifie l'accusé de réception d'authentification
- Affiche un message de succès ou quitte le programme en cas d'erreur

### 2. Envoi de messages (`send_message`)
- Formate le message au format JSON
- Envoie le message encodé en bytes au serveur
- Utilise `drain()` pour s'assurer que les données sont bien envoyées

### 3. Réception de messages (`get_new_message`)
- Boucle infinie qui écoute les messages entrants
- Décode et parse les messages JSON reçus
- Affiche les messages dans l'interface utilisateur

## Installation et utilisation

### Prérequis

```bash
pip install textual asyncio
```

### Lancement de l'application

```bash
cd seance_9/Code
python chat.py
```

### Utilisation

1. **Connexion** : Au lancement, une fenêtre de connexion apparaît
   - Entrez votre identifiant dans le champ "Identifiant"
   - Entrez votre mot de passe dans le champ "Mot de passe"
   - Appuyez sur Entrée pour vous connecter

2. **Envoi de messages** : Une fois connecté
   - Tapez votre message dans le champ en bas de l'écran
   - Appuyez sur Entrée pour envoyer le message

3. **Réception de messages** : Les messages reçus s'affichent automatiquement dans la zone de chat

## Détails techniques

### Protocole de communication

- **Format des messages** : JSON
- **Encodage** : UTF-8 (bytes)
- **Séparation des messages** : Lignes (terminées par `\n`)

### Messages d'authentification

**Envoi** :
```json
{"login": "votre_login", "password": "votre_password"}
```

**Réception** :
- Succès : Message d'accusé de réception
- Erreur : Le programme se ferme avec un message d'erreur

### Messages de chat

**Envoi** :
```json
{"message": "votre_message"}
```

**Réception** :
```json
{"message": "message_reçu"}
```

### Architecture

- **`connection()`** : Gère l'authentification et retourne les objets `reader` et `writer`
- **`send_message()`** : Envoie un message au serveur
- **`get_new_message()`** : Écoute et affiche les messages entrants en continu
- **`ChatApp`** : Application principale avec interface utilisateur
- **`ConnectScreen`** : Écran modal pour la connexion

## Serveur

- **Adresse** : `vassor.org`
- **Port** : `12345`
- **Protocole** : TCP/IP

## Bot de test

Un bot de test est disponible dans `bot.py` pour tester les limites du serveur. 

### Utilisation du bot

```bash
# Mode spam : envoie un nombre défini de messages
python bot.py <login> <password> spam <count> <delay>

# Mode flood : envoie des messages sans délai pour saturer
python bot.py <login> <password> flood
```

### Exemples

```bash
# Envoyer 1000 messages avec un délai de 0.01 seconde
python bot.py PaulAntoine 795528 spam 1000 0.01

# Flood le serveur
python bot.py PaulAntoine 795528 flood
```

## Problèmes de sécurité identifiés

Le protocole de chat présente plusieurs vulnérabilités :

1. **Pas de chiffrement** : Les mots de passe et messages sont transmis en clair
2. **Pas de rate limiting** : Un utilisateur peut envoyer un nombre illimité de messages rapidement
3. **Pas de validation des entrées** : Le serveur peut recevoir des messages malformés ou très longs
4. **Pas d'authentification continue** : Une fois connecté, pas de vérification périodique
5. **Pas de protection contre le spam** : Pas de limite sur le nombre de messages par seconde
6. **Gestion d'erreurs limitée** : Les erreurs peuvent causer des crashes
7. **Pas de timeout** : Les connexions peuvent rester ouvertes indéfiniment
8. **Messages en JSON non validés** : Le serveur fait confiance au format des messages reçus
