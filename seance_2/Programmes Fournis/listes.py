class GenerateurListe():
	def __init__(self):
		self.l = []

	def obtenirListe(self):
		return self.l

class MaClasse():
	def __init__(self, liste):
		self.l = liste

	def inserer_valeur(self, valeur):
		self.l.append(valeur)

	def __repr__(self):
		return f"{self.l}"

# On créé un générateur de listes
g = GenerateurListe()

# On initialise deux instances vide de la classe
m1 = MaClasse(g.obtenirListe())
m2 = MaClasse(g.obtenirListe())

# On insère une valeur dans m1
m1.inserer_valeur(1)
# On affiche m2 (toujours vide)
print(m2)
