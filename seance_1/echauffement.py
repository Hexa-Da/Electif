################################# Échauffement #################################

def HelloWorld():
    print("Hello, World!")

def Boucle():
    for i in range(11):
        print(i)

def FizzBuzz():
    for i in range(51):
        if i%3 == 0 and i%5 == 0:
            print("FizzBuzz")
        elif i%3 == 0:
            print("Fizz")
        elif i%5 == 0:
            print("Buzz")
        else :
            print(i)

def triangle_pascal(n):
    triangle = []
    for i in range(n):
        ligne = []
        for j in range(i + 1):
            if j == 0 or j == i:
                # Les bords sont toujours 1
                ligne.append(1)
            else:
                # Chaque élément est la somme des deux éléments au-dessus
                ligne.append(triangle[i-1][j-1] + triangle[i-1][j])
        triangle.append(ligne)
    return triangle

def afficher_triangle(triangle):
    n = len(triangle)
    for i, ligne in enumerate(triangle):
        # Ajouter des espaces pour centrer
        espaces = " " * (n - i - 1)
        print(espaces + " ".join(str(x) for x in ligne))


if __name__ == "__main__":
    #HelloWorld()
    #Boucle()
    #FizzBuzz()
    triangle = triangle_pascal(6)
    afficher_triangle(triangle)
        
        
        
