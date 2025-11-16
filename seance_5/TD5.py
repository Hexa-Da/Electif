from turtle import left
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_eleves = pd.read_csv('fr-esr-parcours-et-reussite-des-bacheliers-en-licence.csv', sep = ';')

def make_dict(col1, col2):
    return df_eleves[[col1, col2]].drop_duplicates().set_index(col1).to_dict()[col2]

gd_disc_dict = make_dict('Id Grande discipline', 'Grande discipline')
disc_dict = make_dict('Id Discipline', 'Discipline')
sect_disc_dict = make_dict('Id Secteur disciplinaire', 'Secteur disciplinaire')
serie_dict = make_dict('Id Série ou type de Bac', 'Série ou type de Bac')
age_dict = make_dict('Id Âge au bac', 'Âge au bac')
sexe_dict = make_dict('Id Sexe', 'Sexe')
mention_dict = make_dict('Id Mention au Bac', 'Mention au Bac')
df_eleves.drop(columns = ['Année de cohorte des données sur la réussite en licence',
                          'Effectif de néobacheliers de la cohorte.1',
                          'Obtention de la licence en 3 ans',
                          'Obtention de la licence en 4 ans',
                          'Obtention de la licence en 3 ou 4 ans',
                          'Grande discipline',
                          'Discipline',
                          'Secteur disciplinaire',
                          'Série ou type de Bac',
                          'Série ou type de Bac',
                          'Sexe',
                          'Mention au Bac',
                          'Année de cohorte des données sur le passage entre L1 et L2'],
               inplace = True)
df_eleves.fillna(0.0, inplace = True)
df_eleves.drop(df_eleves[df_eleves['Id Secteur disciplinaire'] == 7].index, inplace = True)

statistiques_par_mention = df_eleves.groupby('Id Mention au Bac')[['Effectif de néobacheliers de la cohorte',
                                              'Passage en L2 en 1 an', 
                                              'Redoublement en L1', 
                                              'Passage en L2 en 2 ans']].sum()
df_passage = df_eleves.pivot_table(index = 'Id Grande discipline',
                                   columns = 'Id Série ou type de Bac',
                                   values = 'Passage en L2 en 1 ou 2 ans',
                                   aggfunc = 'sum')
df_neobacheliers = df_eleves.pivot_table(index = 'Id Grande discipline',
                                         columns = 'Id Série ou type de Bac',
                                         values = 'Effectif de néobacheliers de la cohorte',
                                         aggfunc = 'sum')
df_statistiques_par_filiere = df_passage/df_neobacheliers
df_statistiques_par_filiere.rename(index = gd_disc_dict, inplace = True)
df_statistiques_par_filiere.rename(columns = serie_dict, inplace = True)

# Calculer les effectifs par mention
effectifs_par_mention = df_eleves.groupby('Id Mention au Bac')['Effectif de néobacheliers de la cohorte'].sum()

###################################################### Échauffement ######################################################
""" 
 # Créer le graphique en camembert
plt.figure(figsize=(10, 8)) # Taille de la figure
plt.pie(effectifs_par_mention.values, # Données à afficher
        labels=[mention_dict[id_mention] for id_mention in effectifs_par_mention.index],
        autopct='%1.1f%%',
        startangle=90) # Format des labels (pourcentage) et Angle de départ

plt.title('Répartition des mentions des étudiant·e·s néobacheli·er·ère·s', 
          fontsize=14, fontweight='bold', pad=40) # Ajout de pad entre le titre et le graphique
plt.axis('equal')  # Pour avoir un cercle parfait
plt.show()
"""
################################## Relation entre filière au Bac et validation de la L1 ##################################
""" 
# Créer le graphique en barres
plt.figure(figsize=(14, 8))

# Les colonnes sont les séries de bac, les lignes sont les grandes disciplines
series_bac = df_statistiques_par_filiere.columns
grandes_disciplines = df_statistiques_par_filiere.index

x = np.arange(len(series_bac)) # Position des barres
width = 0.2  # Largeur des barres

# Créer les barres pour chaque grande discipline
for i, discipline in enumerate(grandes_disciplines):
    plt.bar(x + i * width, 
            df_statistiques_par_filiere.loc[discipline], 
            width, 
            label=discipline)

# Configuration du graphique
# Calculer la hauteur maximale pour chaque série de bac
max_heights = df_statistiques_par_filiere.max()
for i, serie in enumerate(series_bac):
    plt.text(x[i] + width * 1.5, max_heights[i] + 0.01, serie, ha='center', va='bottom', fontsize=10)

plt.ylabel('Taux de validation L1 (%)', fontsize=12, fontweight='bold')
plt.title('Taux de validation de la L1 par filière de Bac et discipline universitaire', 
          fontsize=16, fontweight='bold', pad=30, loc="center")
plt.xticks([]) # Supprimer les ticks de l'axe x

# Ajouter la légende
plt.legend(bbox_to_anchor=(1,1), loc='upper right')

# Ajuster la mise en page pour éviter que les labels soient coupés
plt.tight_layout()

# Afficher le graphique
plt.show() 
"""
################################## Relation entre sexe et validation de L1 par filière ##################################

# === PHASE 1 : CALCULS AVEC PANDAS ===

# 1. Données détaillées par sexe et discipline pour les barres empilées
df_sexe_discipline = df_eleves.groupby(['Id Grande discipline', 'Id Sexe']).agg({
    'Effectif de néobacheliers de la cohorte': 'sum',
    'Passage en L2 en 1 an': 'sum',
    'Passage en L2 en 2 ans': 'sum'
}).reset_index()

# Calculer les taux de validation détaillés
df_sexe_discipline['L1_validee_1_an'] = df_sexe_discipline['Passage en L2 en 1 an'] / df_sexe_discipline['Effectif de néobacheliers de la cohorte']
df_sexe_discipline['L1_validee_2_ans'] = df_sexe_discipline['Passage en L2 en 2 ans'] / df_sexe_discipline['Effectif de néobacheliers de la cohorte']
df_sexe_discipline['L1_non_validee'] = 1 - df_sexe_discipline['L1_validee_1_an'] - df_sexe_discipline['L1_validee_2_ans']

# 2. Données globales par sexe et discipline pour les camemberts
df_validation_globale = df_eleves.groupby(['Id Grande discipline', 'Id Sexe']).agg({
    'Effectif de néobacheliers de la cohorte': 'sum',
    'Passage en L2 en 1 ou 2 ans': 'sum'
}).reset_index()

# Calculer les taux de validation globaux
df_validation_globale['taux_validation'] = df_validation_globale['Passage en L2 en 1 ou 2 ans'] / df_validation_globale['Effectif de néobacheliers de la cohorte']
df_validation_globale['taux_non_validation'] = 1 - df_validation_globale['taux_validation']

# Vérifier les données calculées
print("\n=== DONNÉES POUR BARRES EMPILÉES ===\n")
print(df_sexe_discipline.head(8))
print("\n=== DONNÉES POUR CAMEMBERT ===\n")
print(df_validation_globale.head(8))

# Créer des dictionnaires pour faciliter l'accès aux données des disciplines
disciplines_order = ['DSA', 'LLSH', 'SI', 'STAPS']
disciplines_ids = {k: k for k in disciplines_order}  # Les IDs sont déjà les codes

# === PHASE 2 : VISUALISATION AVEC MATPLOTLIB ===

# Créer la figure avec deux sous-graphiques
fig, axes = plt.subplots(4, 2, figsize=(9, 6.75)) # 4 barres a gauche et 4 camemberts a droite
axes_bar = axes[:, 0]  # Toutes les lignes, colonne 0 (barres)
axes_pie = axes[:, 1]  # Toutes les lignes, colonne 1 (camemberts)

# Titre principal
fig.suptitle('Statistiques de validation de L1 en fonction du sexe.', fontsize=19, y=0.965)

# === GRAPHIQUE GAUCHE : Barres empilées horizontales ===

# Titre du premier graphique de barres
# Décaler le titre à gauche avec un contrôle précis
axes_bar[0].text(0.385, 1.3, 'Taille des cohortes en fonction du sexe. \n(Base 100: néobacheliers)', 
                transform=axes_bar[0].transAxes, fontsize=13, 
                va='center', ha='center')

# Positions et largeur des barres
y_positions = [0.75, 1.25]  # Femme en haut, Homme en bas
bar_width = 0.25  # Plus large pour un seul graphique

# Couleurs pour les barres empilées
colors = ['#2E8B57', '#FF8C00', '#DC143C']  # Vert, Orange, Rouge

for i, discipline in enumerate(disciplines_order):
    discipline_id = disciplines_ids[discipline]
    ax_bar = axes_bar[i]
    
    # Données pour cette discipline
    data_femme = df_sexe_discipline[(df_sexe_discipline['Id Grande discipline'] == discipline_id) & 
                                   (df_sexe_discipline['Id Sexe'] == 2)]
    data_homme = df_sexe_discipline[(df_sexe_discipline['Id Grande discipline'] == discipline_id) & 
                                   (df_sexe_discipline['Id Sexe'] == 1)]
    
    if not data_femme.empty and not data_homme.empty:
        # Barre Femme (à gauche)
        femme_data = [data_femme.iloc[0]['L1_validee_1_an'] * 100,
                     data_femme.iloc[0]['L1_validee_2_ans'] * 100,
                     data_femme.iloc[0]['L1_non_validee'] * 100]
        
        # Barre Homme (à droite)
        homme_data = [data_homme.iloc[0]['L1_validee_1_an'] * 100,
                     data_homme.iloc[0]['L1_validee_2_ans'] * 100,
                     data_homme.iloc[0]['L1_non_validee'] * 100]
        
        # Créer les barres empilées
        ax_bar.barh(y_positions[1], femme_data[0], bar_width, 
                color=colors[0])
        ax_bar.barh(y_positions[1], femme_data[1], bar_width, 
                left=femme_data[0], color=colors[1])
        ax_bar.barh(y_positions[1], femme_data[2], bar_width, 
                left=femme_data[0] + femme_data[1], color=colors[2])
        
        ax_bar.barh(y_positions[0], homme_data[0], bar_width, 
                color=colors[0])
        ax_bar.barh(y_positions[0], homme_data[1], bar_width, 
                left=homme_data[0], color=colors[1])
        ax_bar.barh(y_positions[0], homme_data[2], bar_width, 
                left=homme_data[0] + homme_data[1], color=colors[2])

# Configuration du graphique gauche
# Pour chaque graphique de barres individuellement
for i in range(4):
    if i != 3:
        axes_bar[i].set_xticks([])
    axes_bar[i].set_yticks(y_positions)
    axes_bar[i].set_yticklabels(['Homme', 'Femme'])
    axes_bar[i].set_ylabel(disciplines_order[i])

# Axe x pour le dernier graphique de barres
axes_bar[3].set_xlim(0, 105)
    
# Légende pour le dernier graphique de barres
legend_elements_bar = [plt.Rectangle((0,0),1,1, facecolor=colors[0], label='L1 validée en 1 an'),
                   plt.Rectangle((0,0),1,1, facecolor=colors[1], label='L1 validée en 2 ans'),
                   plt.Rectangle((0,0),1,1, facecolor=colors[2], label='L1 non validée')]
axes_bar[3].legend(handles=legend_elements_bar, loc='upper center', bbox_to_anchor=(0.725, -0.5))

# === GRAPHIQUE DROITE : Camemberts ===

# Titre du premier graphique de camemberts
# Décaler le titre à gauche avec un contrôle précis
axes_pie[0].text(2.5, 1.3, 'Validation de L1 en fonction du sexe. \n(Passage en L2 en 1 ou 2 ans)', 
                transform=axes_pie[0].transAxes, fontsize=13, 
                va='center', ha='center')

# Couleurs pour les camemberts
pie_colors = ['#4169E1', '#FF8C00']  # Bleu, Orange

for i, discipline in enumerate(disciplines_order):
    discipline_id = disciplines_ids[discipline]
    ax_pie = axes_pie[i]
    # Données pour cette discipline
    data_femme = df_validation_globale[(df_validation_globale['Id Grande discipline'] == discipline_id) & 
                                      (df_validation_globale['Id Sexe'] == 2)]
    data_homme = df_validation_globale[(df_validation_globale['Id Grande discipline'] == discipline_id) & 
                                      (df_validation_globale['Id Sexe'] == 1)]
    
    if not data_femme.empty and not data_homme.empty:
        # Camembert Homme (gauche)
        homme_values = [data_homme.iloc[0]['taux_validation'] * 100,
                       data_homme.iloc[0]['taux_non_validation'] * 100]
        
        # Camembert Femme (droite)
        femme_values = [data_femme.iloc[0]['taux_validation'] * 100,
                       data_femme.iloc[0]['taux_non_validation'] * 100]
        
        # Position des camemberts
        homme_pos = (1, 0.5)  # Homme à gauche, centré verticalement
        femme_pos = (2.5, 0.5)  # Femme à droite, centré verticalement
        
        # Créer les camemberts
        ax_pie.pie(homme_values, autopct='%1.0f%%',
               colors=pie_colors, startangle=90,counterclock=False, radius=0.45, center=homme_pos)
        ax_pie.pie(femme_values, autopct='%1.0f%%',
               colors=pie_colors, startangle=90,counterclock=False, radius=0.45, center=femme_pos)

        # Configuration du graphique droite
        ax_pie.grid(axis='x', alpha=0.3)
        ax_pie.set_xlim(0, 1)
        ax_pie.set_ylim(0, 1)
        ax_pie.set_aspect('equal')
        ax_pie.axis('off')

# Ajouter les labels des disciplines à droite
for i, discipline in enumerate(disciplines_order):
    axes_pie[i].text(3.35, 0.5, discipline, transform=axes_pie[i].transAxes,
             fontsize=10, va='center', ha='left')

# Ajouter les labels des sexes à droite
axes_pie[3].text(1, -0.2, 'Homme', transform=axes_pie[i].transAxes,
             fontsize=10, va='center', ha='center')
axes_pie[3].text(2.5, -0.2, 'Femme', transform=axes_pie[i].transAxes,
             fontsize=10, va='center', ha='center')

# Légende pour les camemberts
legend_elements_pie = [plt.Rectangle((0,0),1,1, facecolor=pie_colors[0], label='L1 validée'),
                   plt.Rectangle((0,0),1,1, facecolor=pie_colors[1], label='L1 non validée')]
axes_pie[3].legend(handles=legend_elements_pie, loc='upper center', bbox_to_anchor=(3.25, -0.7))

# Ajuster la mise en page pour éviter que les labels soient coupés
plt.tight_layout()
plt.show() 
