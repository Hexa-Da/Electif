creneau_par_jour = 7
nb_jour = 5
max_creneau = creneau_par_jour * nb_jour

def afficher_solution(solution, cours, classes, max_salles):
    max_cours = len(cours)
    max_classe = len(classes)

    def creneau_vers_jour(idx):
        return int(idx/creneau_par_jour)

    def creneau_vers_horaire(idx):
        return idx%creneau_par_jour

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
                        timetable[creneau_vers_jour(creneau)][creneau_vers_horaire(creneau)][salle] = (cours, classe)

    s = ""
    for jour in range(nb_jour):
        s += "||" + jour_idx_vers_nom(jour)
        for salle in range(max_salles-1):
            s += "          "
    print(s + "||")
    s = ""
    for jour in range(nb_jour):
        s += "|" 
        for salle in range(max_salles):
            s += f"| Salle {salle} "
    print(s + "||")
            

    for creneau in range(creneau_par_jour):
        s = ""
        for jour in range(nb_jour):
            s += "|"
            for salle in range(max_salles):
                s += "|"
                if timetable[jour][creneau][salle] is None:
                    s += f"         "
                else:
                    cours, classe = timetable[jour][creneau][salle]
                    s += f" G{classe}  C{cours}  "
        print(s + "||")
