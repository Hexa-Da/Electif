# Définition des exports publics
__all__ = ['verifier_isbn']

def verifier_isbn(isbn):
    """
    Vérifie si un ISBN-10 est valide selon l'algorithme de contrôle.
    
    Args:
        isbn (str): La chaîne de caractères représentant l'ISBN à vérifier
    Returns:
        bool: True si l'ISBN est valide, False sinon
    """
    
    # Vérifier que l'ISBN a exactement 10 caractères
    if len(isbn) != 10:
        return False
    
    # Vérifier que les 9 premiers caractères sont des chiffres
    for i in range(9):
        if not isbn[i].isdigit():
            return False
    
    # Vérifier que le 10ème caractère est un chiffre ou 'X'
    if not (isbn[9].isdigit() or isbn[9] == 'X'):
        return False
    
    # Calculer la somme de contrôle
    somme_controle = 0
    for i in range(9):
        ci = int(isbn[i])
        somme_controle += ci * (11 - (i + 1))  # i+1 car l'index commence à 0
    
    # Appliquer le modulo 11 à la somme totale
    s_controle = somme_controle % 11
    
    # Calculer la valeur de contrôle
    valeur_controle = 11 - (somme_controle % 11)
    
    # Déterminer le caractère de contrôle attendu
    if s_controle == 0:
        caractere_attendu = '0'
    elif valeur_controle == 10:
        caractere_attendu = 'X'
    else:
        caractere_attendu = str(valeur_controle)
    
    # Vérifier si le caractère de contrôle correspond
    return isbn[9] == caractere_attendu


# Exemples de test
if __name__ == "__main__":
    # Test avec des ISBN valides et invalides
    test_cases = [
        "0306406152",  # ISBN valide
        "830640615X",  # ISBN valide avec X
        "1234567890",  # ISBN invalide
        "0306406153",  # ISBN invalide (mauvais caractère de contrôle)
        "030640615",   # ISBN trop court
        "03064061523", # ISBN trop long
        "03064061X2",  # ISBN invalide (X au mauvais endroit)
    ]
    
    print("Tests de vérification ISBN-10:")
    for isbn in test_cases:
        result = verifier_isbn(isbn)
        print(f"ISBN: {isbn} -> {'Valide' if result else 'Invalide'}")
