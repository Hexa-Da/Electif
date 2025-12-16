## Séance 1 / TD1

### Thèmes abordés
- Introduction à Python : fonctions de base, boucles, conditions
- Algorithmes de validation d'ISBN-10
- Manipulation de chaînes de caractères

### Techniques utilisées
- Fonctions Python (HelloWorld, FizzBuzz, triangle de Pascal)
- Boucles et conditions (for, if/elif/else)
- Validation d'ISBN avec calcul de somme de contrôle
- Manipulation de chaînes (isdigit, vérification de format)

## Séance 2 / TD2

### Thèmes abordés
- Programmation orientée objet en Python
- Implémentation de classes et itérateurs
- Génération automatique d'ISBN-10 valides

### Techniques utilisées
- Classes Python (ISBN10, ISBN10Generator)
- Itérateurs personnalisés (__iter__, __next__)
- Propriétés (@property)
- Générateurs infinis
- Gestion d'erreurs (ValueError)

## Séance 3 / TD3

### Thèmes abordés
- Traitement du signal audio numérique
- Analyse spectrale avec transformée de Fourier (FFT)
- Génération et manipulation de signaux sonores

### Techniques utilisées
- Génération de signaux sinusoïdaux (numpy)
- Transformée de Fourier rapide (scipy.fft)
- Analyse spectrale (fftfreq, magnitude)
- Filtres audio (passe-bas, passe-haut avec scipy.signal)
- Superposition et concaténation de signaux
- Sauvegarde de fichiers WAV (scipy.io.wavfile)
- Visualisation avec matplotlib

## Séance 4 / TD4

### Thèmes abordés
- Introduction à l'analyse de données avec pandas
- Nettoyage et préparation de données
- Statistiques descriptives sur les parcours étudiants

### Techniques utilisées
- Chargement de CSV avec pandas (read_csv, séparateurs)
- Nettoyage de données (drop, fillna, drop_duplicates)
- Création de dictionnaires de mapping
- Groupement de données (groupby)
- Calculs statistiques (somme, agrégation)
- Conversion de types (pd.to_numeric)

## Séance 5 / TD5

### Thèmes abordés
- Analyse approfondie des parcours et de la réussite des bacheliers en licence
- Statistiques par mention, filière et sexe
- Impact de la filière du Bac sur la validation de la L1

### Techniques utilisées
- Tableaux croisés (pivot_table)
- Groupement multi-niveaux (groupby avec plusieurs colonnes)
- Calcul de proportions et taux de validation
- Visualisations avancées avec matplotlib (camembert, barres empilées)
- Création de graphiques multi-panneaux (subplots)
- Préparation de données pour visualisation

## Séance 6 / TD6

### Thèmes abordés
- Parsing de langages avec funcparserlib
- Structures de données pour représenter la musique
- Synthèse audio à partir de descriptions textuelles

### Techniques utilisées
- Tokenisation et parsing (funcparserlib)
- Grammaires récursives (forward_decl)
- Structures de données (NoteDef, Son, Sequence, Superposition)
- Méthodes de synthèse (synthesize)
- Concaténation et superposition de pistes audio
- Traitement de fichiers texte

## Séance 7 / TD7

### Thèmes abordés
- Théorie des graphes avec NetworkX
- Analyse de données de transport public (format GTFS)
- Algorithmes de parcours et optimisation de trajets

### Techniques utilisées
- Bibliothèque NetworkX pour la manipulation de graphes
- Lecture de fichiers CSV (données GTFS : stops, trips, stop_times)
- Calcul de distances géodésiques (geopy.distance)
- Composantes connexes (nx.connected_components)
- Degré des nœuds et centralité
- Plus courts chemins (nx.shortest_path, Dijkstra)
- Calcul de toutes les distances (nx.all_pairs_dijkstra_path_length)
- Visualisation de graphes sur carte (plotly, pandas)

## Séance 8 / TD8

### Thèmes abordés
- Programmation par contraintes (Constraint Programming)
- Génération automatique d'emplois du temps
- Modélisation de problèmes d'optimisation combinatoire

### Techniques utilisées
- Bibliothèque CPMpy pour la résolution de contraintes
- Variables de décision booléennes (boolvar)
- Modélisation de contraintes (Model, solve)
- Tableaux multidimensionnels pour représenter le planning
- Contraintes sur les créneaux, cours, classes et salles
- Résolution SAT (satisfiabilité)
- Affichage formaté de solutions

## Séance 9 / TD9

### Thèmes abordés
- Programmation réseau avec TCP/IP et asyncio
- Communication client-serveur asynchrone
- Interfaces utilisateur textuelles avec Textual
- Protocoles de communication (JSON sur TCP)
- Sécurité des applications réseau

### Techniques utilisées
- Connexions TCP asynchrones (asyncio.open_connection)
- StreamReader et StreamWriter pour la communication bidirectionnelle
- Bibliothèque Textual pour les interfaces TUI (Text User Interface)
- Format JSON pour la sérialisation des messages
- Gestion asynchrone des événements (await, async/await)
- Parsing JSON (json.loads, json.dumps)
- Encodage/décodage UTF-8 (encode, decode)
- Gestion des buffers réseau (drain)
- Boucles infinies asynchrones pour la réception continue
- Identification des vulnérabilités de sécurité (chiffrement, rate limiting, validation)

## Séance 10 / TD10

### Thèmes abordés
- Développement d'applications web avec Django
- Intégration d'un solveur de contraintes dans une application web
- Gestion de formulaires HTML et requêtes POST
- Modèles de données et ORM Django
- Templates Django et langage de template
- Génération automatique d'emplois du temps via interface web

### Techniques utilisées
- Framework web Django (modèles, vues, templates, URLs)
- Modèles de données Django (models.Model, CharField, IntegerField)
- ORM Django (objects.all(), order_by(), save())
- Gestion de requêtes HTTP (request.POST, request.GET)
- Templates Django avec boucles ({% for %}) et variables ({{ }})
- Formulaires HTML avec méthode POST et tokens CSRF
- Intégration de solveur externe (edt_solver avec CPMpy)
- Parsing de données POST (request.POST.get())
- Gestion d'erreurs (IntegrityError, try/except)
- Mapping de données entre base de données et solveur
- Conversion de QuerySets en listes pour garantir l'ordre
- Construction de contextes pour les templates
- Affichage de solutions dans des tableaux HTML