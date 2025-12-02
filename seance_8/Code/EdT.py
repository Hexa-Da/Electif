import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="cpmpy")
import cpmpy as cp  # pyright: ignore[reportMissingImports]
import affichage

class Cours():
    uniq_id = 0
    def __init__(self, heures, nom):
        self.nb_heures = heures
        self.nom = nom
        self.id = Cours.uniq_id
        Cours.uniq_id += 1

    def __repr__(self):
        return "{id: " + str(self.id) + ", nom: " + self.nom + ", nb_heure: " + str(self.nb_heures) + "}"


class Classe():
    uniq_id = 0
    def __init__(self, cours):
        self.cours = cours
        self.id = Classe.uniq_id
        Classe.uniq_id += 1

    def __repr__(self):
        return repr(self.cours)

# Ces quelques définitions vous permettent de tester votre code.
cours1 = Cours(2, "Cours1")
cours2 = Cours(4, "Cours2")
cours3 = Cours(3, "Cours3")

# À partir de la section 3, vous devriez pouvoir utiliser ce dictionnaire.
# Si vous voulez tester avec plus de cours différents, déclarez les au dessus et complétez la liste ci-dessous.
cours = dict([(c.id, c) for c in [cours1, cours2, cours3]])

classe1 = Classe([cours1, cours2])
classe2 = Classe([cours2, cours3])

# À partir de la section 4, vous devriez pouvoir utiliser ce tableau de classes. 
# Si vous voulez tester avec plus de classes, pensez à les ajouter à ce tableau.
classes = [classe1, classe2]

# Un planning est un tableau de 5 (jours) × 7 (créneau/jour) = 35 cases.
# Dans chaque case, il doit y avoir: 1 indicatif de cours, 1 indicatif de classe
# Nous avons donc un tableau à 3 dimensions

print(f"Paramètres du problème :")
max_cours = len(cours)
print(f"max_cours: {max_cours}")
max_classe = len(classes)
print(f"max_classe: {max_classe}")

# On considère des journées de 7h, avec 5 jours par semaine.
creneau_par_jour = 7
nb_jour = 5
# On a donc 35 créneaux horaires par semaine. Nos créneaux sont donc numérotés de 0 à 34.
max_creneau = creneau_par_jour * nb_jour
print(f"max_creneau: {max_creneau}")
# À partir de la section 5, vous devriez pouvoir gérer plusieurs salles en parallèle. Vous pouvez augmenter ou diminuer le nombre de salles en changeant la variable ci-dessous.
max_salles = 3
print(f"max_salles: {max_salles}")

# ÉTAPE 1 : VARIABLES DE DÉCISIONS
# Tableau 2D de booléens : allocation[creneau][cours_id]
# True si le cours cours_id est placé au créneau creneau
planning = cp.boolvar(shape=(max_creneau, max_salles, max_cours, max_classe))

# ETAPE 2 : AJOUTER LES CONTRAINTES
m = cp.Model()

# Contrainte 1 : Une classe ne peut pas avoir deux cours en même temps
# Pour chaque créneau ET chaque classe, au plus un cours peut être assigné
for creneau in range(max_creneau):
    for classe_id in range(max_classe):
        m += sum(planning[creneau, :, :, classe_id]) <= 1

# Contrainte 2 : Chaque cours doit avoir nb_heures créneaux pour chaque classe qui le suit
for classe_id, classe in enumerate(classes):
    for c in classe.cours:  # Pour chaque cours de cette classe
        m += sum(planning[:, :, c.id, classe_id]) == c.nb_heures

# Contrainte 3 : Une classe ne peut pas suivre un cours qui n'est pas dans sa liste
for classe_id, classe in enumerate(classes):
    cours_de_la_classe = [c.id for c in classe.cours]
    for cours_id in range(max_cours):
        if cours_id not in cours_de_la_classe:
            # Cette classe ne doit jamais avoir ce cours
            m += sum(planning[:, :, cours_id, classe_id]) == 0

# Contrainte 4 : Une salle ne peut pas avoir deux cours en même temps
for creneau in range(max_creneau):
    for salle in range(max_salles):
        m += sum(planning[creneau, salle, :, :]) <= 1

# ÉTAPE 3 : TROUVER UNE SOLUTION
# Résoudre le modèle
if m.solve():
    print("\nSolution trouvée !")
    solution = planning.value()
    affichage.afficher_solution(solution, cours, classes, max_salles)
    
else:
    print("Aucune solution trouvée !")
    solution = None