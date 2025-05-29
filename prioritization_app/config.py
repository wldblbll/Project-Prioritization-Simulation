import streamlit as st
from datetime import datetime

def get_simulation_config():
    # Checkbox pour choisir si le budget maximum est identique sur toutes les années
    same_budget_all_years = st.sidebar.checkbox("Budget maximum identique pour toutes les années", value=True)

    if same_budget_all_years:
        # Si le budget est le même pour toutes les années, afficher un seul slider
        budget_max_per_year = [st.sidebar.slider('Budget maximum (kEUR)', 500, 5000, 1000)] * 5
    else:
        # Sinon, afficher un slider pour chaque année
        budget_max_per_year = [
            st.sidebar.slider(f'Budget maximum année {i+1} (kEUR)', 500, 5000, 1000)
            for i in range(5)
        ]

    # Saisie de la première année
    first_year = st.sidebar.number_input('Première année', value=datetime.now().year, min_value=1900, max_value=2100)

    return {
        'n_projects': st.sidebar.slider('Nombre de projets', 10, 100, 50),
        'budget_max_per_year_kEUR': budget_max_per_year,
        'profitability_threshold_kEUR': st.sidebar.slider('Seuil de rentabilité (kEUR)', 50, 1000, 300),
        'max_iterations': st.sidebar.slider('Nombre maximum d\'itérations', 10, 10000, 1000),
        'first_year': first_year,  # Ajout de l'année de départ
        'same_budget_all_years': same_budget_all_years  # Statut de la checkbox
    }