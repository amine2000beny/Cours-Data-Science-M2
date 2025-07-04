# 🏡 Airbnb Price Prediction

## bjectif du projet

Ce projet vise à prédire le **logarithme du prix** (`log_price`) de logements Airbnb à partir de leurs caractéristiques (type, localisation, équipements, etc.).  
Le but est d'appliquer un pipeline complet de **data science** :

- Exploration des données
- Nettoyage et feature engineering
- Entraînement et comparaison de modèles de machine learning
- Prédictions sur un jeu de test inconnu

---

## Fichiers fournis

- `airbnb_train.csv` : jeu de données d'entraînement (avec la cible `log_price`)
- `airbnb_test.csv` : jeu de test à prédire (sans `log_price`)
- `prediction_example.csv` : format attendu pour le rendu
- `Explication.txt` : description des variables
- `Projet_description.md` : consignes détaillées

---

## Étapes réalisées

### 1. Analyse exploratoire (EDA)

- Inspection des types, valeurs manquantes, outliers
- Visualisation des distributions (`log_price`, `accommodates`, etc.)
- Carte de répartition géographique (latitude/longitude)
- Analyse des variables catégorielles (`room_type`, `property_type`, etc.)

### 2. Prétraitement et Feature Engineering

- Imputation des valeurs manquantes par la moyenne
- Conversion des booléens (`t/f` → `1/0`)
- Nettoyage des pourcentages (`host_response_rate`)
- Extraction de nouvelles features :
  - Longueur de description
  - Nombre d’équipements (`amenities`)
  - Ancienneté de l’hôte (`host_since`)
- Encodage One-Hot des variables catégorielles

### 3. Modélisation & évaluation

- Modèles testés :
  - Linear Regression
  - Ridge
  - Lasso
  - Random Forest
  - XGBoost
- Métrique utilisée : **Root Mean Squared Error (RMSE)**

| Modèle             | RMSE   |
|--------------------|--------|
| Baseline (mean)    | 0.7159 |
| Linear Regression  | 0.5840 |
| Ridge              | 0.4770 |
| Lasso              | 0.5834 |
| Random Forest      | 0.4117 |
| ✅ XGBoost          | 0.4016 ✅

Le modèle final retenu est **XGBoost**.

### 4. Prédiction finale

- Nettoyage du test identique au train
- Alignement exact des colonnes
- Prédiction du `log_price` pour chaque ligne du test
- Génération du fichier `prediction.csv` :


id,prediction
14282777,4.965303
17029381,6.070183
...
