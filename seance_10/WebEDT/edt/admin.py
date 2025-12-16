from django.contrib import admin

from .models import Cours, Classe, Salle

# Register your models here.
admin.site.register(Cours)
admin.site.register(Classe)
admin.site.register(Salle)
