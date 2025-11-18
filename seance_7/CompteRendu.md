# Exercices sur les graphes

## 1. Introduction

### 1.1 Fichiers fournis

#### Question 1 : 

La classe Routes a un seul champ : routes (dictionnaire d'identifiants de route vers objets Route)

#### Question 2 :

- Classe : Stations (ligne 85)
- Fonction : Retourne les coordonnées (latitude, longitude) d'une station à partir de son identifiant, en utilisant la station parente si nécessaire
- Type de retour : tuple (latitude, longitude)

## 2. Création de graphe

#### Question 3 :

```markdown
Algorithme : Créer_Graphe_Transport(arrêts, routes)

Entrée :
- `arrêts` : liste d'arrêts (identifiés par leur ID)
- `routes` : liste de routes, où chaque route est une liste de paires `(id_départ, id_arrivée)`

Sortie :
- `graphe` : un graphe dont les nœuds sont les arrêts et les arêtes sont les segments

---

Déroulement de l’algorithme :

1. Initialiser un graphe vide
   - `graphe ← Créer_Graphe_Vide()`

2. Ajouter tous les arrêts comme nœuds du graphe :
   - Pour chaque `arrêt` dans `arrêts` :
       - `id_arrêt ← obtenir_id(arrêt)`
       - `Ajouter_Nœud(graphe, id_arrêt)`

3. Parcourir toutes les routes et ajouter les arêtes :
   - Pour chaque `route` dans `routes` :
       - (Chaque route est une liste de segments `(id_départ, id_arrivée)`)
       - Pour chaque `segment` dans `route` :
           - `(id_départ, id_arrivée) ← segment`
           - Si `id_départ` et `id_arrivée` existent dans les nœuds du graphe alors :
               - Si l'arête `(id_départ, id_arrivée)` n'existe pas déjà dans le graphe alors :
                   - `Ajouter_Arête(graphe, id_départ, id_arrivée)`

4. Retourner le graphe
   - `retourner graphe`
```

#### Question 4 :

Application de l'algorithme ci-dessus à la méthode `get_nx_graph(self, stations)` de la classe `Routes` dans le fichier `routes.py` pour quelle renvoie un graph avec les distances adaptés entre chaque neouds.

## 3. Manipulations de graphes

### 3.1 Composantes connexes

#### Questions 5 :

**Méthode utilisée :**

1. **Trouver toutes les composantes connexes :**
   - `composantes = list(nx.connected_components(graph))`
   - Conversion en liste pour pouvoir itérer plusieurs fois

2. **Calculer le nombre total de composantes :**
   - `nb_composantes = len(composantes)`

3. **Pour chaque composante, calculer le nombre de nœuds :**
   - Parcours de toutes les composantes avec `enumerate(composantes)`
   - Pour chaque composante, calcul de sa taille avec `len(composante)`
   - Stockage des tailles dans une liste `tailles_composantes`

4. **Identifier la plus grande composante connexe :**
   - Utilisation de `max(composantes, key=len)` pour trouver la composante avec le plus grand nombre de nœuds
   - Stockage dans la variable `component` pour utilisation ultérieure

5. **Créer le sous-graphe de la plus grande composante :**
   - `subgraph = graph.subgraph(component)`

**Résultat :** Le code affiche le nombre total de composantes connexes ainsi que leur taille et identifie la taille de la plus grande composante. 

### 3.2 Degrés des nœuds

#### Question 6 :

Pour trouver l'arrêt le mieux desservi (celui avec le plus de voisins), il suffit de trouver le neoud avec le degré maximum. 

### 3.3 Plus courrt chemin

#### Question 7 :

NetworkX propose la fonction `nx.shortest_path()` pour calculer le chemin le plus court entre deux nœuds :

- nx.shortest_path(G, source, target, weight=None)
    - G : le graphe
    - source : nœud de départ
    - target : nœud d'arrivée
    - weight : attribut des arêtes à utiliser comme poids (optionnel)

- Fonctions complémentaires :
    - nx.shortest_path_length(G, source, target, weight=None) : retourne uniquement la longueur du chemin
    - nx.dijkstra_path(G, source, target, weight='weight') : utilise explicitement l'algorithme de Dijkstra
    - nx.dijkstra_path_length(G, source, target, weight='weight') : longueur avec Dijkstra

#### Question 8 :

```markdown
Algorithme : Trouver_Arrêt_Plus_Proche(distance)

Entrée : 
- `distance` : dictionnaire de dictionnaires où distance[source][destination] contient la distance entre source et destination

Sortie : 
- `arrêt_optimal` : l'identifiant de l'arrêt qui minimise la somme des distances vers tous les autres arrêts

---

Début de l'algoritme :
    // Initialiser les variables
    arrêt_optimal ← NULL
    somme_minimale ← +∞
    
    // Obtenir la liste de tous les arrêts (clés du dictionnaire distance)
    arrêts ← clés(distance)
    
    // Pour chaque arrêt, calculer la somme des distances vers tous les autres
    POUR CHAQUE arrêt DANS arrêts FAIRE
        somme_distances ← 0
        
        // Parcourir tous les autres arrêts
        POUR CHAQUE autre_arrêt DANS arrêts FAIRE
            SI arrêt ≠ autre_arrêt ALORS
                // Ajouter la distance entre arrêt et autre_arrêt
                somme_distances ← somme_distances + distance[arrêt][autre_arrêt]
            FIN SI
        FIN POUR
        
        // Vérifier si cette somme est la plus petite trouvée jusqu'à présent
        SI somme_distances < somme_minimale ALORS
            somme_minimale ← somme_distances
            arrêt_optimal ← arrêt
        FIN SI
    FIN POUR
    
    RETOURNER arrêt_optimal
FIN
```

#### Question 9 :

La documentation de NetworkX propose la fonction `nx.all_pairs_dijkstra_path_length` qui retoune un générateur de tuples qui nous permet de créer le dictionnaire de dictionnaires "distances" qui répertorie toutes les distances entre les arrêts.

- nx.all_pairs_dijkstra_path_length(G, weight)
    - G : le graphe
    - weight : attribut des arêtes à utiliser comme poids (ici distance)

#### Question 10 :

voir implémentation fichier : `Fluo.py`

## Résultat de notre étude 

### Partie 1
- Nombre de composantes connexes : 96
- Taille de la plus grande composante connexe : 968 nœuds

### Partie 2
- Arrêt le mieux desservi : LUNEVILLE Cité Scolaire Arrivée (ID: 16431)
- Nombre de voisins : 14
- Localisation : (48.5972719, 6.505069)

### Partie 4
- Chemin le plus court : [('Vélodrome', 16043), ('Joseph Laurent', 128305), ('Castelnau', 128302), ('VILLERS-LES-NANCY STAN ESIAL Mutualité', 16506), ('Grange aux Moines', 61399), ('MARON Cimetière', 16254), ('MARON Charles de Gaulle', 16135)]
- Longueur du chemin : 11.410354249914443 km

### Partie 4
- Arrêt qui minimise la distance par rapport aux autres : NANCY République
- Coordonnées de l'arrêt optimal : (48.6883609, 6.1765378)