# 📊 Copublications Inria 
# 📊 Copublications Internationales Inria

Objectif : analyser les collaborations entre chercheurs et institutions à partir des publications Inria déposées dans l'archive ouverte HAL (https://inria.hal.science)

Composants principaux de Copublis:
A Copublis.ipynb -> tableau xlsx des copublications par auteur Inria, co-auteurs étrangers, affiliation directe, institution, pays.
B ville_boost.ipynb  -> ajout des villes  dans le tableau précédent : 1 tableau xslx pour analyse et 1 tableau csv pour le Dashboard
C Dashboard : un ensemble de fichiers pythons pour l'interface graphique de présentation des résultats
  

--- A - Spécifications Copublis.ipynb ---
Prérequis:
--> outil pour lancer les scripts (Anaconda/Jupyter Notebook, Visual Studio Code, etc.)
--> avoir les droits en écriture dans le répertoire où se trouve le script: Ce script extrait les données de HAL au format XML-TEI et les enregistre dans un sous-répertoire
--> mémoire nécessaire : env. 1Go pour 100 000 dépôts hal (fichiers .xml)

Traitements :
- identification des chercheurs Inria, en cas d'affiliations multiples, on supprime les autres affiliations (maintient des affiliations directes à un centre ou au Siège)
- identification des chercheurs étrangers
- identification des institutions tutelles des affiliations primaires
- exclusion des publications franco-françaises
- nettoyage du texte et des codes invisibles

Résultat:
fichier xlsx par auteur Inria: une ligne pour chaque co-auteur étranger, avec affiliations et pays.

--- B - Spécifications ville_boost.ipynb ---
- cities500 contenant une copie du fichier cities500.txt (https://download.geonames.org/export/dump/)
- dossier Geonames_contryInfo contenant une copie du fichier countryInfo.txt (https://download.geonames.org/export/dump/)
- ainsi qu'un fichier contenant des villes associées à certaines structures d'Aurehal (ID_Aurehal_Ville_Etat_Latitude_Longitude.xlsx)
- Le résultat est nettoyé (caractères non latins, caractères invisibles)
Sortie:
- fichier xslx avec titre de colonnes en anglais pour exploitation autonome
- fichier csv pour le Dashboard


--- C - Spécifications Dashboard ---
L’interface propose des filtres, des indicateurs clés (KPI), des graphiques, un réseau de copublications et une carte interactive des collaborations.

## 🚀 Fonctionnalités

- **Tableau de bord interactif**
  - Nombre total de publications, villes, auteurs Inria, auteurs copubliants.
  - Publications par année (bar chart).
  - Répartition par villes et organismes (camemberts).
  - Génération d’un nuage de mots (WordCloud) à partir des mots-clés.

- **Réseau de copublications**
  - Graphe interactif représentant les liens entre auteurs Inria, copubliants et villes.

- **Carte interactive**
  - Localisation des villes italiennes impliquées dans des copublications.
  - Arcs reliant Inria Sophia aux villes partenaires (épaisseur proportionnelle au nombre de publications).
  - Zoom et navigation sur la carte.

---

## 📂 Données attendues

Le script charge un fichier **Excel** (par défaut : `Copubliants_par_auteur_Inria_Bordeaux_Sophia`) contenant les colonnes suivantes :  

- `HalID` : identifiant de la publication  
- `Auteurs_FR` : auteur Inria  
- `Auteurs_copubliants` : auteur dans le monde
- `Ville_en_fr` : ville (en français)  
- `Organisme_copubliant` : organisme associé  
- `Année` : année de publication  
- `Equipe` : équipe de recherche Inria  
- `Latitude`, `Longitude` : coordonnées géographiques pour la carte
- `Mots-cles` *(optionnel)* : mots-clés associés aux publications  

---

## 🛠️ Installation

1. **Cloner ce dépôt** (ou copier le script).  
2. Créer un environnement virtuel et installer les dépendances :  

```bash
pip install -r requirements.txt




