"""
Programme de statistiques sur les ISBN-10.
Génère un grand nombre d'ISBN aléatoires et calcule la proportion d'ISBN valides.
"""

import isbn
import gen_isbn
import time


def calculer_statistiques_isbn(nombre_isbn=1000000):
    """
    Calcule les statistiques sur un grand nombre d'ISBN générés aléatoirement.
    
    Args:
        nombre_isbn (int): Nombre d'ISBN à générer et tester
    Returns:
        dict: Dictionnaire contenant les statistiques calculées
    """

    print(f"Génération et validation de {nombre_isbn:,} ISBN...")
    
    # Mesurer le temps d'exécution
    debut = time.time()
    
    isbn_valides = 0
    isbn_invalides = 0
    
    # Générer et tester les ISBN
    for i in range(nombre_isbn):
        # Générer un ISBN aléatoire
        isbn_genere = gen_isbn.randISBN()
        
        # Vérifier s'il est valide
        if isbn.verifier_isbn(isbn_genere):
            isbn_valides += 1
        else:
            isbn_invalides += 1
        
        # Afficher le progrès tous les 100 ISBN
        if (i + 1) % 100 == 0:
            pourcentage = ((i + 1) / nombre_isbn) * 100
            barre = "#" * int(pourcentage // 2)
            espaces = " " * (50 - len(barre))
            print(f"\rProgrès: [{barre}{espaces}] {pourcentage:.1f}%", end="", flush=True)
    
    fin = time.time()
    temps_execution = fin - debut
    
    # Calculer les statistiques
    proportion_valides = (isbn_valides / nombre_isbn) * 100 
    proportion_invalides = (isbn_invalides / nombre_isbn) * 100 
    
    return {
        'total': nombre_isbn,
        'valides': isbn_valides,
        'invalides': isbn_invalides,
        'proportion_valides': proportion_valides,
        'proportion_invalides': proportion_invalides,
        'temps_execution': temps_execution
    }


def afficher_statistiques(stats):
    print("\n" + "="*60)
    print("STATISTIQUES DES ISBN-10 GÉNÉRÉS ALÉATOIREMENT")
    print("="*60)

    print(f"Nombre total d'ISBN générés: {stats['total']:,}")
    print(f"ISBN valides: {stats['valides']:,} ({stats['proportion_valides']:.2f}%)")
    print(f"ISBN invalides: {stats['invalides']:,} ({stats['proportion_invalides']:.2f}%)")
    print(f"Temps d'exécution: {stats['temps_execution']:.2f} secondes")
    print(f"Vitesse: {stats['total']/stats['temps_execution']:.0f} ISBN/seconde")
    print("="*60 + "\n")


def main():    
    # Demander le nombre d'ISBN à générer
    try:
        nombre = input("\nNombre d'ISBN à générer (défaut: 1,000,000): ").strip()
        if nombre:
            nombre_isbn = int(nombre)
        else:
            nombre_isbn = 1000000
    except ValueError:
        print("Valeur invalide")
        exit()
    
    # Calculer les statistiques
    stats = calculer_statistiques_isbn(nombre_isbn)
    
    # Afficher les résultats
    afficher_statistiques(stats)

if __name__ == "__main__":
    main()
