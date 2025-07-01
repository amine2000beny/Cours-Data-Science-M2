import streamlit as st
import pandas as pd
import joblib

#  Chargement du modèle
model = joblib.load("titanic_pipeline.pkl")

# Titre
st.title(" Titanic Survival Predictor")
st.markdown("Prédisez vos chances de survie à bord du Titanic.")

# Collecte des entrées utilisateur
st.header(" Entrez vos informations :")

col1, col2 = st.columns(2)

with col1:
    Pclass = st.selectbox("Classe (Pclass)", [1, 2, 3])
    Sex = st.selectbox("Sexe", ["male", "female"])
    Embarked = st.selectbox("Port d'embarquement", ["S", "C", "Q"])

with col2:
    Age = st.slider("Âge", 0, 100, 25)
    Fare = st.slider("Prix du billet (Fare)", 0.0, 600.0, 32.0)
    SibSp = st.number_input("Nombre de frères/soeurs ou conjoint(s) à bord (SibSp)", 0, 10, 0)
    Parch = st.number_input("Nombre de parents/enfants à bord (Parch)", 0, 10, 0)

# Calcul de la feature ingénierée
FamilySize = SibSp + Parch

# Affichage résumé
st.subheader(" Résumé des données saisies :")
st.write({
    "Pclass": Pclass,
    "Sex": Sex,
    "Age": Age,
    "Fare": Fare,
    "Embarked": Embarked,
    "FamilySize": FamilySize
})

#  Prédiction
if st.button(" Prédire la survie"):
    input_df = pd.DataFrame([{
        "Pclass": Pclass,
        "Sex": Sex,
        "Age": Age,
        "Fare": Fare,
        "Embarked": Embarked,
        "FamilySize": FamilySize
    }])
    
    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][pred]

    if pred == 1:
        st.success(f" Vous auriez survécu ! (probabilité : {proba:.2%})")
    else:
        st.error(f" Vous n'auriez pas survécu. (probabilité : {proba:.2%})")

# Footer
st.markdown("---")
st.markdown(" *Modèle entraîné sur les données publiques du Titanic avec sklearn.*")
