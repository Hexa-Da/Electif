from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse

import edt_solver
import pdb

from .models import Cours, Salle, Classe

def index(request):
    context = {}
    return render(request, "edt/index.html", context)

def salles(request):
    salles = Salle.objects.all()
    context = {
            "salles": salles,
    }
    return render(request, "edt/salles.html", context)

def ajout_salle(request):
    try: 
        s = Salle(numero=request.POST["salle_numero"])
        s.save()
        return HttpResponse("Salle ajoutée")
    except IntegrityError:
        return HttpResponse("La salle " + str(request.POST["salle_numero"]) + " existe déjà.")

def cours(request):
    cours = Cours.objects.all()
    context = {
            "cours": cours,
    }
    return render(request, "edt/cours.html", context)

def ajout_cours(request):
    intitule_cours = request.POST["intitule_cours"]
    quota_heures = request.POST["quota_heures"]
    try: 
        c = Cours(intitule_cours=intitule_cours, quota_horaire=int(quota_heures))
        c.save()
        return HttpResponse("Cours ajouté")
    except IntegrityError:
        return HttpResponse("Le cours " + str(intitule_cours) + " existe déjà.")

def classe(request):
    classes = Classe.objects.all()
    context = {
            "classes": classes,
    }
    return render(request, "edt/classe.html", context)

def ajout_classe(request):
    try: 
        s = Classe(classe=request.POST["classe_id"])
        s.save()
        return HttpResponse("Classe ajoutée")
    except IntegrityError:
        return HttpResponse("La classe " + str(request.POST["classe_id"]) + " existe déjà.")

def curriculum(request):
    classes = Classe.objects.all()
    cours = Cours.objects.all()
    context = {
        "classes": classes,
        "cours": cours,
    }
    return render(request, "edt/curriculum.html", context)

def calculer_edt(request):
    solver = edt_solver.Instance(5, 7)
    
    # Récupérer tous les cours, salles et classes de la base de données
    # Convertir en listes pour garantir l'ordre et permettre l'indexation
    cours_db = list(Cours.objects.all())
    salles_db = list(Salle.objects.all())
    # IMPORTANT : Trier les classes par numéro pour les ajouter dans l'ordre (1, 2, 3, etc.)
    classes_db = list(Classe.objects.all().order_by('classe'))
    
    # Vérifier qu'il y a au moins des cours, salles et classes
    if not cours_db or not salles_db or not classes_db:
        context = {
            "solution": {},
            "error": "Veuillez d'abord ajouter des cours, salles et classes."
        }
        return render(request, "edt/edt.html", context)
    
    # Ajouter tous les cours à l'instance du solver
    for cours in cours_db:
        solver.ajouter_cours(cours.intitule_cours, cours.quota_horaire)
    
    # Ajouter toutes les salles à l'instance du solver
    for salle in salles_db:
        solver.ajouter_salle(str(salle.numero))
    
    # Utiliser la requête POST pour inscrire les classes aux bons cours
    # Les classes sont ajoutées dans l'ordre (classe 1, puis 2, etc.)
    for classe in classes_db:
        intitules_cours_classe = []
        for cours in cours_db:
            # Vérifier si la checkbox pour cette classe et ce cours est cochée
            # Format du nom : "classe-cours" (ex: "1-Python")
            checkbox_name = f"{classe.classe}-{cours.intitule_cours}"
            if request.POST.get(checkbox_name) == "on":
                # La classe est inscrite à ce cours
                intitules_cours_classe.append(cours.intitule_cours)
        # Ajouter la classe avec ses cours au solver
        if intitules_cours_classe:
            solver.ajouter_classe(intitules_cours_classe)
    
    # Vérifier qu'au moins une classe a été ajoutée
    if len(solver.classes) == 0:
        context = {
            "solution": {},
            "error": "Aucune classe n'a été inscrite à des cours. Veuillez sélectionner au moins un cours pour une classe."
        }
        return render(request, "edt/edt.html", context)
    
    solution = solver.resoudre()
    
    # Vérifier si une solution a été trouvée
    if solution is None:
        context = {
            "solution": {},
            "error": "Aucune solution trouvée. Le problème peut être insoluble avec les contraintes données."
        }
        return render(request, "edt/edt.html", context)
    
    timetable = edt_solver.affichage.build_timetable(solution, solver, cours_db, salles_db, classes_db)
    context = {
            "solution": timetable,
    }
    return render(request, "edt/edt.html", context)
