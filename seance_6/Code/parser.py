from funcparserlib.lexer import make_tokenizer, TokenSpec, Token
from funcparserlib.parser import *
from typing import List
from mixer import *

def _tokenize(s: str) -> List[Token]:
    specs = [
        TokenSpec("ws", r"\s+"),  # Ajouter les blancs
        TokenSpec("majuscule", r"[A-Z]"),  # Ajouter les majuscules
        TokenSpec("chiffre", r"[0-9]"),  # Ajouter les chiffres        
        TokenSpec("equal", r"="),
        TokenSpec("pipe", r"[|]"),
        TokenSpec("comma", r","),
        TokenSpec("semicolon", r";"),
        TokenSpec("debut-son", r"[{]"),
        TokenSpec("fin-son", r"[}]"),
    ]
    tokenizer = make_tokenizer(specs)
    return [t for t in tokenizer(s) if t.type != "ws"]

class NoteDef:
    def __init__(self, nom, frequence):
        self.nom = nom
        self.frequence = frequence

    def __repr__(self):
        return self.nom + "=" + str(self.frequence) + "Hz"

class Son:
    def __init__(self, nom, duree_millisecondes):
        self.nom = nom
        self.nb_ticks = float(duree_millisecondes)

    def __repr__(self):
        return self.nom + ":" + str(self.nb_ticks)

    def duree(self):
        return self.nb_ticks

    def synthesize(self, notes):
        return note(notes[self.nom], self.nb_ticks, 4) # 4 harmoniques par défaut.

class Sequence:
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return self.notes.__repr__()

    def duree(self):
        return sum([n.duree() for n in self.notes])

    def synthesize(self, notes):
        return concatener_signaux([n.synthesize(notes) for n in self.notes])

class Superposition:
    def __init__(self, lignes):
        if not all([p.duree() == lignes[0].duree() for p in lignes]):
            print("Toutes les pistes n'ont pas la même durée : " + str([p.duree() for p in lignes]))
        self.lignes = lignes

    def __repr__(self):
        return self.lignes.__repr__()

    def duree(self):
        return max([p.duree() for p in self.lignes])

    def synthesize(self, notes):
        return superposer_signaux([n.synthesize(notes) for n in self.lignes])

def concat_pistes(premiere, autres):
    total = [premiere]
    total.extend(autres)
    return total

nombre = many(tok("chiffre")) >> (lambda p: int(''.join(p))) # fourni
freq = nombre
nom = tok("majuscule") + tok("chiffre") >> (lambda l: ''.join(l)) # fourni

# note_def : nom '=' freq → (nom, freq) pour créer un dict
note_def = nom + tok("equal") + freq >> (lambda x: (x[0], x[2]))

# son : nom ',' nombre ';' → Son(nom, nombre)
son = nom + tok("comma") + nombre + tok("semicolon") >> (lambda x: Son(x[0], x[2]))

# piste : note | '{' piste* '}' | '{' piste ('|' piste)* '}'
piste = forward_decl()

def make_sequence(pistes):
    #Convertit une liste de pistes en Sequence
    if len(pistes) == 0:
        return Sequence([])
    if len(pistes) == 1:
        return pistes[0]
    return Sequence(pistes)

def make_superposition(pistes):
    #Convertit une liste de pistes en Superposition
    if len(pistes) == 1:
        return pistes[0]
    return Superposition(pistes)

# Parser pour une superposition (avec au moins un '|')
piste_superposee = tok("debut-son") + piste + many(tok("pipe") + piste) + tok("fin-son") >> (
    lambda x: make_superposition([x[1]] + [p[1] for p in x[2]])
)

# Parser pour une séquence (sans '|')
piste_seule = tok("debut-son") + many(piste) + tok("fin-son") >> (lambda x: make_sequence(x[1]))

# Une piste peut être un son, une superposition (avec '|'), ou une séquence (sans '|')
# L'ordre est important : essayer d'abord la superposition, puis la séquence
piste.define(son | piste_superposee | piste_seule)

fichier = (many(note_def) >> (lambda array: dict(array))) + piste

def parse(s):
    tokens = _tokenize(s)
    return fichier.parse(tokens)


if __name__ == "__main__":
    with open("musique.txt", 'r') as file:
        donnees = file.read()
        spec = parse(donnees)
        signal = spec[1].synthesize(spec[0])
        sauvegarder("signal.wav", signal)