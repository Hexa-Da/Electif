import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import du fichier CSV avec le séparateur point-virgule
df = pd.read_csv('fr-esr-parcours-et-reussite-des-bacheliers-en-licence.csv', 
                 sep=';', 
                 encoding='utf-8')

# Ne garder que toutes les colonnes sauf les 5 dernières (statistiques L3 non utiles ici)
df = df.iloc[:, :-5]

def make_dict(df, key_col, val_col):
    # Construit un dict unique key_col -> val_col
    # en retirant NaN et doublons exacts
    return (df[[key_col, val_col]]
            .dropna(subset=[key_col, val_col])
            .drop_duplicates(subset=[key_col, val_col])
            .set_index(key_col)[val_col]
            .to_dict())

# Supprimer les colonnes d'intitulés
label_cols = ['Grande discipline', 'Discipline', 'Secteur disciplinaire']
df = df.drop(columns=label_cols)

# Supprimer les colonnes d'intitulés
label_cols2 = ['Série ou type de Bac', 'Âge au bac', 'Sexe', 'Mention au Bac']
df = df.drop(columns=label_cols2)

# Remplacer tous les NaN par 0.0
df = df.fillna(0.0)

df = df.drop(columns="Année de cohorte des données sur le passage entre L1 et L2")


# Supprimer toutes les lignes avec Id Secteur disciplinaire = 7 (santé)
df = df.drop(df.index[df['Id Secteur disciplinaire'] == 7])

print(f"\nDimensions du DataFrame (après nettoyage) : {df.shape}\n")

"""
Total d'élèves dans l'échantillon (somme des effectifs de néobacheliers)
"""
eff = pd.to_numeric(df['Effectif de néobacheliers de la cohorte'], errors='coerce').fillna(0).sum()
print(f"Nombre d'élèves dans l'échantillon : {int(eff)}\n")

"""
Trouvez le nombre de passage en L2 en 1 an, le nombre de redoublement en L1 et 
le nombre de passage en L2 en 2 ans pour chaque mention. 
"""

# Colonnes de stats à agréger
cols = ['Passage en L2 en 1 an', 'Redoublement en L1', 'Passage en L2 en 2 ans']

# S'assurer que ce sont bien des numériques
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# Agréger par mention (ID) et sommer
statistiques_par_mention = (
    df.groupby('Id Mention au Bac', as_index=True)[cols]
      .sum()
      .sort_index()
)

print(statistiques_par_mention)
print()
