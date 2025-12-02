# Programmation par contraintes

## Question 1 - Formalisation de la contrainte 2

La contrainte 2 stipule que chaque cours doit avoir un unique créneau alloué :

$$\forall 0 < \text{cours\_id} \leq m, \sum_{0 < \text{creneau} \leq n} \text{allocation}[\text{creneau}][\text{cours\_id}] = 1$$

## Question 2 - Création des variables de décisions et ajout des contraintes

```bash
# ÉTAPE 1 : VARIABLES DE DÉCISIONS
# Tableau 2D de booléens : allocation[creneau][cours_id]
# True si le cours cours_id est placé au créneau creneau
planning = cp.boolvar(shape=(max_creneau, max_cours))

# ETAPE 2 : AJOUTER LES CONTRAINTES
m = cp.Model()

# Contrainte 1 : Il ne doit pas y avoir deux cours en même temps
# Pour chaque créneau, au plus un cours peut être assigné
for creneau in range(max_creneau):
    m += sum(planning[creneau, :]) <= 1

# Contrainte 2 : Chaque cours doit avoir un unique créneau alloué
# Pour chaque cours, il doit être assigné à exactement un créneau
for cours_id in range(max_cours):
    m += sum(planning[:, cours_id]) == 1
```

## Quesstion 3 - Premier solution 

```bash
# ÉTAPE 3 : TROUVER UNE SOLUTION
# Résoudre le modèle
if m.solve():
    # Il existe plusieurs solutions, on en choisit une arbitrairement
    print("\nSolution trouvée !")
    solution = planning.value()
    
    # Affichage sommaire de la solution
    print("\nEmploi du temps :")
    for creneau in range(max_creneau):
        for cours_id in range(max_cours):
            if solution[creneau][cours_id]:
                jour = creneau // creneau_par_jour
                heure = creneau % creneau_par_jour
                print(f"  Jour {jour + 1}, Créneau {heure + 1} : {cours[cours_id].nom}")
else:
    print("Aucune solution trouvée !")
    solution = None
```

## Question 4 - Cours de 2h

Modification de la $2^{nd}$ contrainte :

$$\forall 0 < \text{cours\_id} \leq m, \sum_{0 < \text{creneau} \leq n} \text{allocation}[\text{creneau}][\text{cours\_id}] = 2$$

## Question 5 - Adaptation de la $2^{nd}$ contrainte

La contrainte 2 devient :

$$\forall 0 < \text{cours\_id} \leq m, \sum_{0 < \text{creneau} \leq n} \text{allocation}[\text{creneau}][\text{cours\_id}] = \text{cours}[\text{cours\_id}].\text{nb\_heures}$$

## Question 6 - Adaptation de `EdT.py`

Il suffit de modifier la $2^{nd}$ contrainte :

```bash
# Contrainte 2 : Chaque cours doit avoir exactement nb_heures créneaux
for cours_id in range(max_cours):
    m += sum(planning[:, cours_id]) == cours[cours_id].nb_heures
```

On peut aussi adapté l'affichage :

```bash
for cours_id, c in cours.items():
        creneaux_assignes = []
        for creneau in range(max_creneau):
            if solution[creneau][cours_id]:
                jour = creneau // creneau_par_jour + 1
                heure = creneau % creneau_par_jour + 1
                creneaux_assignes.append(f"Jour {jour} H{heure}")
        print(f"{c.nom} ({c.nb_heures}h) : {', '.join(creneaux_assignes)}")
```

## Question 7 - Contrainte sur les classes

Une classe ne peut pas suivre un cours qui n'est pas dans sa liste, ce qui se formalise par :

$$\forall 0 < \text{classe\_id} \leq p, \forall \text{cours\_id} \notin \{\text{c.id} \mid \text{c} \in \text{classes}[\text{classe\_id}].\text{cours}\},$$

$$\sum_{0 < \text{creneau} \leq n} \text{allocation}[\text{creneau}][\text{cours\_id}][\text{classe\_id}] = 0$$

## Question 8 - Adaptation de `EdT.py` à la nouvelle contrainte 

$1^{er}$ contrainte :

```bash
# Contrainte 1 : Une classe ne peut pas avoir deux cours en même temps
# Pour chaque créneau ET chaque classe, au plus un cours peut être assigné
for creneau in range(max_creneau):
    for classe_id in range(max_classe):
        m += sum(planning[creneau, :, classe_id]) <= 1
```

$2^{nd}$ contrainte :

```bash
# Contrainte 2 : Chaque cours doit avoir nb_heures créneaux pour chaque classe qui le suit
for classe_id, classe in enumerate(classes):
    for c in classe.cours:  # Pour chaque cours de cette classe
        m += sum(planning[:, c.id, classe_id]) == c.nb_heures
```

on adapte également l'affichage :

```bash 
for classe_id, classe in enumerate(classes):
        print(f"\nClasse {classe_id} (cours: {[c.nom for c in classe.cours]}) :")
        for creneau in range(max_creneau):
            for cours_id in range(max_cours):
                if solution[creneau][cours_id][classe_id]:
                    jour = creneau // creneau_par_jour + 1
                    heure = creneau % creneau_par_jour + 1
                    print(f"Jour {jour} H{heure} : {cours[cours_id].nom}")
```

## Question 9 - Contrainte sur les salles

on ajoute une $4^{ème}$ dimenssion au tableau et une $4^{ème}$ contrainte :

```bash
# Contrainte 4 : Une salle ne peut pas avoir deux cours en même temps
for creneau in range(max_creneau):
    for salle in range(max_salles):
        m += sum(planning[creneau, salle, :, :]) <= 1
```