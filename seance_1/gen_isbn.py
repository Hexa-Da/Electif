import random

# Définition des exports publics
__all__ = ['randISBN']

def randISBN():
    # Générer les 9 premiers chiffres
    isbn = ""
    for _ in range(9):
        isbn += str(random.randint(0, 9))
    
    # Générer le caractère de contrôle
    isbn += random.choice([str(random.randint(0, 9)), 'X'])
        
    return isbn

if __name__ == "__main__":
    print(randISBN())
