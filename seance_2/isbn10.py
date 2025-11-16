"""
Module ISBN10 - Classe représentant les ISBN-10.

Ce module contient une classe ISBN10 qui représente un ISBN-10 complet,
avec un constructeur acceptant les 9 premiers caractères et calculant
automatiquement le 10ème caractère (chiffre de contrôle).
"""

from collections.abc import Iterable

# Définition des exports publics
__all__ = ['ISBN10', 'ISBN10Generator', 'iter_isbn10']



class ISBN10(Iterable):
    """
    Classe représentant un ISBN-10 complet.
    
    Le constructeur accepte les 9 premiers caractères de l'ISBN-10
    et calcule automatiquement le 10ème caractère (chiffre de contrôle).
    
    Cette classe hérite de Iterable, permettant d'itérer sur les caractères
    de l'ISBN-10 complet.
    """
    
    def __init__(self, neuf_premiers_caracteres):
        """
        Constructeur de la classe ISBN10.
        
        Args:
            neuf_premiers_caracteres (str): Les 9 premiers caractères de l'ISBN-10
            
        Raises:
            ValueError: Si les premiers caractères ne sont pas valides
        """
        # Validation des neuf premiers caractères
        if not isinstance(neuf_premiers_caracteres, str):
            raise ValueError("Les premiers caractères doivent être une chaîne de caractères de 9 chiffres")  
        if len(neuf_premiers_caracteres) != 9:
            raise ValueError("Les premiers caractères doivent contenir exactement 9 chiffres")        
        for i, char in enumerate(neuf_premiers_caracteres):
            if not char.isdigit():
                raise ValueError(f"Le caractère à la position {i+1} doit être un chiffre de 0 à 9")
        
        # Stocker les 9 premiers caractères
        self._neuf_premiers_caracteres = neuf_premiers_caracteres
        
        # Calculer le chiffre de contrôle
        self._chiffre_controle = self._calculer_chiffre_controle()
        
        # Construire l'ISBN complet
        self._isbn_complet = self._neuf_premiers_caracteres + self._chiffre_controle
        
        # Initialiser l'index pour l'itération
        self._index = 0
    
    def _calculer_chiffre_controle(self):
        """
        Calcule le chiffre de contrôle selon l'algorithme ISBN-10.
        
        Returns:
            str: Le chiffre de contrôle ('0'-'9' ou 'X')
        """
        # Calculer la somme pondérée
        somme_controle = 0
        for i in range(9):
            ci = int(self._neuf_premiers_caracteres[i])
            somme_controle += ci * (10 - i)  # Pondération décroissante de 10 à 2
        
        # Calculer le chiffre de contrôle
        reste = somme_controle % 11
        
        if reste == 0:
            return '0'
        elif reste == 1:
            return 'X'
        else:
            return str(11 - reste)
    
    def __iter__(self):
        """
        Méthode requise par l'interface Iterable.
        Initialise l'itération et retourne l'objet lui-même.
        
        Returns:
            ISBN10: L'objet lui-même pour permettre l'itération
        """
        self._index = 0
        return self
    
    def __next__(self):
        """
        Méthode requise par l'interface Iterator.
        Retourne le caractère suivant lors de l'itération.
        
        Returns:
            str: Le caractère suivant de l'ISBN-10
            
        Raises:
            StopIteration: Quand tous les caractères ont été parcourus
        """
        if self._index < len(self._isbn_complet):
            caractere = self._isbn_complet[self._index]
            self._index += 1
            return caractere
        else:
            raise StopIteration
    
    @property
    def neuf_premiers_caracteres(self):
        """Retourne les 9 premiers caractères de l'ISBN."""
        return self._neuf_premiers_caracteres
    
    @property
    def chiffre_controle(self):
        """Retourne le chiffre de contrôle calculé."""
        return self._chiffre_controle
    
    @property
    def isbn_complet(self):
        """Retourne l'ISBN-10 complet."""
        return self._isbn_complet
    
    def __str__(self):
        """Représentation de l'ISBN-10."""
        return self._isbn_complet
        


def verifier_isbn_complet(isbn_complet):
    """
    Vérification complète de la validité d'un l'ISBN-10.
    Par defaut notre constructeur crée un ISBN-10 valide.
    
    Args:
        isbn_complet (str): L'ISBN-10 complet (10 caractères)
    
    Returns:
        bool: True si l'ISBN est valide, False sinon
    """
    # Calculer la somme de contrôle selon l'algorithme standard
    somme_controle = 0
    for i in range(9):
        ci = int(isbn_complet[:9][i])
        somme_controle += ci * (10 - i)
    
    # Ajouter la contribution du chiffre de contrôle
    if isbn_complet[9] == 'X':
        somme_controle += 10
    else:
        somme_controle += int(isbn_complet[9])
    
    # L'ISBN est valide si la somme est divisible par 11
    return somme_controle % 11 == 0


class ISBN10Generator:
    """
    Itérateur infini générant des ISBN-10 valides.

    - Parcourt séquentiellement tous les préfixes de 9 chiffres (000000000 → 999999999).
    - Après 999999999, repart à 000000000 (comportement infini).
    """

    def __init__(self, start=0):
        if not isinstance(start, int):
            raise ValueError("start doit être un entier compris entre 0 et 999999999")
        if start < 0 or start > 999999999:
            raise ValueError("start doit être compris entre 0 et 999999999")
        self._current = start

    def __iter__(self):
        return self

    def __next__(self):
        # zfill(9) ajoute des zéros à gauche pour avoir une chaîne de 9 caractères
        # Par exemple: str(123).zfill(9) donne "000000123"
        prefixe = str(self._current).zfill(9)
        isbn_obj = ISBN10(prefixe)
        # Incrément et bouclage
        if self._current == 999999999:
            self._current = 0
        else:
            self._current += 1
        return isbn_obj.isbn_complet


def iter_isbn10(start=0):
    """
    Renvoie un itérateur infini d'ISBN-10 (chaînes) valides.

    Args:
        start (int): préfixe initial entre 0 et 999999999

    Returns:
        ISBN10Generator: itérateur infini
    """
    return ISBN10Generator(start=start)


# Exemples de test et démonstration
if __name__ == "__main__":
    print("\n=== Démonstration du module ISBN10 ===\n")
    
    # Test 1: Création d'un ISBN-10 à partir des 9 premiers caractères
    print("1. Création d'un ISBN-10:")
    try:
        isbn1 = ISBN10("030640615")
        print(f"   ISBN créé: {isbn1}")
        print(f"   Neuf premiers caractères: {isbn1.neuf_premiers_caracteres}")
        print(f"   Chiffre de contrôle: {isbn1.chiffre_controle}")
        print(f"   ISBN complet: {isbn1.isbn_complet}")
    except ValueError as e:
        print(f"   Erreur: {e}")
    
    # Test 2: Création d'un ISBN-10 avec X comme chiffre de contrôle
    print("\n2. Création d'un ISBN-10 avec 'X':")
    try:
        isbn2 = ISBN10("830640615")
        print(f"   ISBN créé: {isbn2}")
        print(f"   Chiffre de contrôle: {isbn2.chiffre_controle}")
    except ValueError as e:
        print(f"   Erreur: {e}")
    
    # Test 3: Test de verifier_isbn_complet
    print("\n3. Test de vérification d'ISBN-10 complets:")
    isbn_valide = "0306406152"
    print(f"   ISBN valide : {isbn_valide} --> {verifier_isbn_complet(isbn_valide)}")
    isbn_invalide = "0306406153"
    print(f"   ISBN invalide : {isbn_invalide} --> {verifier_isbn_complet(isbn_invalide)}")
    isbn_valide_x = "012345678X"
    print(f"   ISBN valide avec X : {isbn_valide_x} --> {verifier_isbn_complet(isbn_valide_x)}")
    isbn_invalide_x = "012345677X" 
    print(f"   ISBN invalide avec X : {isbn_invalide_x} --> {verifier_isbn_complet(isbn_invalide_x)}")
    
    # Test 4: Générateur infini d'ISBN-10
    print("\n4. Générateur infini d'ISBN-10 (10 premiers à partir de 0):")
    gen = iter_isbn10(start=0)
    exemples = [next(gen) for i in range(10)]
    print(f"   Exemples: {exemples}")

    # Test 5: Gestion d'erreurs
    print("\n5. Gestion d'erreurs:")
    try:
        ISBN10("12345678")  # Trop court
    except ValueError as e:
        print(f"   ISBN trop court: {e}")
    try:
        ISBN10("1234567890")  # Trop long
    except ValueError as e:
        print(f"   ISBN trop long: {e}")
    try:
        ISBN10("12345678a")  # Caractère non numérique
    except ValueError as e:
        print(f"   Caractère non numérique: {e}")

    # Test 6: Test d'itération
    print("\n6. Test d'itération:")
    isbn_iter = ISBN10("123456789")
    print(f"   ISBN pour test d'itération: {isbn_iter}")
    print("   Caractères individuels:")
    for i, caractere in enumerate(isbn_iter):
        print(f"    Position {i+1}: '{caractere}'")

print("\n=== Fin de la démonstration ===\n")