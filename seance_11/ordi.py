from __future__ import annotations
import asyncio
import time
from typing import Self
import matplotlib.pyplot as plt

class Tache(): 
    def __init__(self, nom_unite: str, duree: int, continuation: list[Self], nom_tache=None):
        self.duree = duree
        self.continuation = continuation
        self.unite = nom_unite
        self.nom = nom_tache

    async def executer(self) -> list[Self]:
        await asyncio.sleep(self.duree)
        return self.continuation

class UniteExecution():
    def __init__(self, nom: str, ordi: Ordinateur, taches: list[Tache]):
        self.nom = nom
        self.ordi = ordi 
        self.taches = taches

    async def demarrer(self): 
        while True:
            if self.taches:
                tache = self.taches.pop(0)
                self.log(f"Démarrage de la tache {tache.nom}")
                temps_debut = time.time_ns() - self.ordi.temps_debut
                continuations = await tache.executer()
                temps_fin = time.time_ns() - self.ordi.temps_debut
                self.ordi.log_tache(self.nom, temps_debut, temps_fin, tache.nom)
                self.log(f"Fin de la tache {tache.nom}")
                for c in continuations:
                    self.ordi.ajouter_tache(c)
                self.ordi.terminer_tache()
            else:
                if self.ordi.nb_taches_restantes() == 0:
                    break
                await asyncio.sleep(0)

    def ajouter_tache(self, tache: Tache) -> None:
        self.taches.append(tache)

    def log(self, msg: str) -> int: 
        temps = time.time_ns() - self.ordi.temps_debut
        print(f"[{self.nom} @ {temps}] {msg}")
        return temps

class Ordinateur():
    def __init__(self, unites: list[str]): 
        self.unites = {}
        for nom_unite in unites:
            self._ajouter_unite(UniteExecution(nom_unite, self, []))
        self._nb_taches = 0
        self.temps_debut = time.time_ns()

    def _ajouter_unite(self, unite: UniteExecution) -> bool:
        if self.unites.get(unite.nom) == None:
            self.unites[unite.nom] = unite
            return True
        else:
            return False

    def ajouter_tache(self, tache: Tache) -> None:
        unite = self.unites.get(tache.unite)
        if unite:
            unite.ajouter_tache(tache)
            self._nb_taches += 1

    def terminer_tache(self) -> None:
        self._nb_taches -= 1

    def nb_taches_restantes(self) -> int:
        return self._nb_taches

    async def demarrer(self) -> None:
        self._init_log()
        tasks = [asyncio.create_task(unite.demarrer()) for unite in self.unites.values()]
        await asyncio.gather(*tasks)
        self._fin_log()

    def _init_log(self) -> None:
        self.unit_idx = {name: idx + 1 for idx, name in enumerate(self.unites)}
        fig, ax = plt.subplots()
        self._ax = ax
        self._ax.set_yticks([idx for name, idx in self.unit_idx.items()], labels = [name for name, idx in self.unit_idx.items()])

    def log_tache(self, nom_unite: str, debut: int, fin: int, nom_tache: str | None) -> None:
        self._ax.barh(self.unit_idx[nom_unite], fin - debut, left=debut, height=0.5, align='center')
        plt.text(debut + (fin - debut)/2, self.unit_idx[nom_unite], nom_tache, horizontalalignment="center")

    def _fin_log(self) -> None:
        self._ax.set_xlim(left=0, right = time.time_ns() - self.temps_debut)
        self._ax.set_xlabel("Temps d'exécution (ns)")
        self._ax.set_ylabel("Unité d'exécution")
        self._ax.set_title("Diagramme d'exécution des tâches")
        plt.show()
        

def exemple():
    ordi = Ordinateur(["CPU", "Mémoire", "Carte réseau"])
    mem = Tache("Mémoire", 2, [Tache("Carte réseau", 1, [], nom_tache="Envoi message"), Tache("CPU", 2, [], nom_tache="Calcul après mémoire")], nom_tache="Lecture message")
    cpu1 = Tache("CPU", 1, [mem], nom_tache="Calcul message")
    cpu2 = Tache("CPU", 1, [], nom_tache="Autre calcul")
    ordi.ajouter_tache(cpu1)
    ordi.ajouter_tache(cpu2)
    asyncio.run(ordi.demarrer())

if __name__ == "__main__":
    exemple()