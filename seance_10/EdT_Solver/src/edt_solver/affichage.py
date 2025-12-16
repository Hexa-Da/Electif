creneau_par_jour = 7
nb_jour = 5
max_creneau = creneau_par_jour * nb_jour

def build_timetable(solution, instance, ensemble_cours=None, ensemble_salles=None, ensemble_classes=None):
    max_cours = len(instance.cours)
    max_classe = len(instance.classes)
    max_salles = len(instance.salles)

    def intitule_cours(idx):
        if ensemble_cours is None:
            return idx
        else:
            return ensemble_cours[idx].intitule_cours
        
    def numero_salle(idx):
        if ensemble_salles is None:
            return idx
        else:
            return ensemble_salles[idx].numero

    def numero_classe(idx):
        if ensemble_classes is None:
            return idx
        else:
            return ensemble_classes[idx].classe

    def creneau_vers_jour(idx):
        return int(idx/creneau_par_jour)

    def creneau_vers_horaire(idx):
        return idx%creneau_par_jour

    timetable = {}

    for jour in range(nb_jour):
        timetable[jour] = {}
        for creneau in range(creneau_par_jour):
            timetable[jour][creneau] = {}
            for salle in range(max_salles):
                timetable[jour][creneau][salle] = None

    for creneau in range(max_creneau):
        for salle in range(max_salles):
            for cours in range(max_cours):
                for classe in range(max_classe):
                    if solution[creneau][salle][cours][classe]:
                        timetable[creneau_vers_jour(creneau)][creneau_vers_horaire(creneau)][salle] = (intitule_cours(cours), numero_classe(classe), numero_salle(salle))

    return timetable


def afficher_solution(solution, instance_solver):
    max_salles = len(instance_solver.salles)

    def jour_idx_vers_nom(idx):
        if idx == 0:
            return " Lundi   "
        if idx == 1:
            return " Mardi   "
        if idx == 2:
            return " Mercredi"
        if idx == 3:
            return " Jeudi   "
        if idx == 4:
            return " Vendredi"
        return "         "

    timetable = build_timetable(solution, instance_solver)

    s = ""
    for jour in range(nb_jour):
        s += "||" + jour_idx_vers_nom(jour)
        for salle in range(max_salles-1):
            s += "          "
    s += "||\n"
    for jour in range(nb_jour):
        s += "|" 
        for salle in range(max_salles):
            s += f"| Salle {salle} "
    s += "||\n"
            

    for creneau in range(creneau_par_jour):
        for jour in range(nb_jour):
            s += "|"
            for salle in range(max_salles):
                s += "|"
                if timetable[jour][creneau][salle] is None:
                    s += f"         "
                else:
                    cours, classe = timetable[jour][creneau][salle]
                    s += f" G{classe}  C{cours}  "
        s += "||\n"
    return (s, timetable)
