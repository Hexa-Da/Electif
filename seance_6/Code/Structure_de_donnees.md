# Explication de la structure de donnée

## Correspondance des groupes selon la grammaire

Pour la chaîne : 
```bash
C3 = 262 E3 = 330 G3 = 392 { C3, 5; { C3, 5; | E3, 5; | G3, 5; } }
```

### Analyse selon la grammaire :

#### Structure du fichier :
fichier := note_def* piste

#### Définitions de notes (note_def) :
1. C3 = 262 → note_def (nom=C3, freq=262)
2. E3 = 330 → note_def (nom=E3, freq=330)
3. G3 = 392 → note_def (nom=G3, freq=392)

#### Piste principale :
{ C3, 5; { C3, 5; | E3, 5; | G3, 5; } }

#### Décomposition récursive de la piste :
- { ... } → séquence (Sequence)
    - Premier élément : C3, 5; → note (nom=C3, durée=5)
    - Deuxième élément : { C3, 5; | E3, 5; | G3, 5; } → superposition (Superposition)
        - { ... } → Superposition
            - C3, 5; → note (nom=C3, durée=5)
            - | → séparateur
            - E3, 5; → note (nom=E3, durée=5)
            - | → séparateur
            - G3, 5; → note (nom=G3, durée=5)

## Schéma de la structure de données en mémoire

```bash
Dictionnaire des notes (notes):
{
  'C3': 262,
  'E3': 330,
  'G3': 392
}

Structure de la piste:
Sequence(
  notes=[
    Son(nom='C3', nb_ticks=5.0),
    Superposition(
      lignes=[
        Son(nom='C3', nb_ticks=5.0),
        Son(nom='E3', nb_ticks=5.0),
        Son(nom='G3', nb_ticks=5.0)
      ]
    )
  ]
)
```