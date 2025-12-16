from django.db import models

# Create your models here.

class Cours(models.Model):
    intitule_cours = models.CharField(max_length=200, unique=True)
    quota_horaire = models.IntegerField(default=0)

    def __str__(self):
        return self.intitule_cours

class Classe(models.Model):
    classe = models.IntegerField(unique=True)
    def __str__(self):
        return str(self.classe)

class Salle(models.Model):
    numero = models.IntegerField(unique=True)
    def __str__(self):
        return "Salle " + str(self.numero)
