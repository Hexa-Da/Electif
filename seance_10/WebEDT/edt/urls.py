from django.urls import path
from . import views

app_name = "edt"
urlpatterns = [
        path("", views.index, name="index"),
        path("salles", views.salles, name="salles"),
        path("ajouter_salle", views.ajout_salle, name="ajout_salle"),
        path("cours", views.cours, name="cours"),
        path("ajouter_cours", views.ajout_cours, name="ajout_cours"),
        path("classes", views.classe, name="classes"),
        path("ajouter_classe", views.ajout_classe, name="ajout_classe"),
        path("curriculum", views.curriculum, name="curriculum"),
        path("calculer_edt", views.calculer_edt, name="calculer_edt"),
]
