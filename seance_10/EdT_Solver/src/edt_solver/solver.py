import cpmpy as cp

class Cours():
    uniq_id = 0
    def __init__(self, heures, nom):
        self.nb_heures = heures
        self.nom = nom
        self.id = Cours.uniq_id
        Cours.uniq_id += 1

    def __repr__(self):
        return "{id: " + str(self.id) + ", nom: " + self.nom + ", nb_heures: " + str(self.nb_heures) + "}"

    def reset():
        Cours.uniq_id = 0


class Classe():
    uniq_id = 0
    def __init__(self, cours):
        self.cours = cours
        self.id = Classe.uniq_id
        Classe.uniq_id += 1

    def __repr__(self):
        return "{cours: " + repr(self.cours) + ", id: " + repr(self.id) + "}"

    def reset():
        Classe.uniq_id = 0

class Instance():
    def __init__(self, nb_jour: int, creneau_par_jour: int):
        self.nb_jour = nb_jour
        self.creneau_par_jour = creneau_par_jour
        self.cours = {}
        self.classes = []
        self.salles = []
        Cours.reset()
        Classe.reset()

    def __trouver_cours__(self, intitule: str):
        cours_ok = [ self.cours[c] for c in self.cours if self.cours[c].nom == intitule ]
        if not cours_ok:
            return None
        else:
            return cours_ok[0]

    def ajouter_cours(self, intitule: str, quota: int):
        cours = Cours(quota, intitule)
        self.cours[cours.id] = cours

    def ajouter_classe(self, intitules_cours: list[str]):
        cours = [ self.__trouver_cours__(c) for c in intitules_cours ]
        classe = Classe(cours)
        self.classes.append(classe)

    def ajouter_salle(self, nom: str):
        self.salles.append(nom)

    def resoudre(self):
        max_cours = len(self.cours)
        max_classe = len(self.classes)
        max_salles = len(self.salles)
        max_creneau = self.nb_jour * self.creneau_par_jour

        planning = cp.boolvar(shape=(max_creneau, max_salles, max_cours, max_classe), name="alloc")
        m = cp.Model(
                # Pas deux cours en même temps pour une classe donnée
                cp.all(
                    cp.sum([planning[time][salle][cours][classe] for salle in range(max_salles) for cours in range(max_cours)]) <= 1
                    for time in range(max_creneau)
                    for classe in range(max_classe)
                ),

                # Pas deux cours dans la même salle en même temps
                cp.all(
                    cp.sum([planning[time][salle][cours][classe] for classe in range(max_classe) for cours in range(max_cours)] ) <= 1
                    for time in range(max_creneau)
                    for salle in range(max_salles)
                )
        )
        cours_idx = 0
        for classe in self.classes:
            for cours_idx in classe.cours:
                m += (cp.sum(planning[time][salle][cours_idx.id][classe.id] for time in range(max_creneau) for salle in range(max_salles)) == self.cours[cours_idx.id].nb_heures)
        m.solve()
        solution = planning.value()
        return solution

def solution_to_dict(solution):
    """
    Prend une solution sous forme d'un tableau de bouléens à 4 dimensions (le numéro du créneau, la salle, le cours et la classe) et renvoie un dictionnaire à plusieurs niveau : Heure -> Jour -> Salle -> {Cours et Classe} ou None.

    Ne fonctionne que pour 35 créneaux
    """
    dictionnaire = { 9: {}, 10: {}, 11: {}, 13: {}, 14: {}, 15: {}, 16: {}}
    for heure in dictionnaire: 
        print(heure)


