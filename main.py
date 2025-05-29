import streamlit as st
from prioritization_app.data_generation import generate_initial_projects
from prioritization_app.simulation import monte_carlo_simulation, filter_solutions
from prioritization_app.visualization import display_project_distributions, display_general_graphs, display_selected_scenario_distribution, display_stacked_barchart
from prioritization_app.config import get_simulation_config

# --- Session State pour garder les résultats de la simulation ---
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None

# --- Configuration générale ---
config = get_simulation_config()

# Génération des projets
projects = generate_initial_projects(config['n_projects'])

st.write("Tableau des projets - Vous pouvez ajuster la NPV Moyenne et la Variance NPV pour chaque projet :")
editable_projects = st.data_editor(projects, num_rows="dynamic")

# Affichage des distributions des projets individuels avant simulation
st.write("Visualisation des distributions des projets :")
display_project_distributions(editable_projects)

# Affichage du stacked barchart pour les budgets des projets avant simulation
st.write("Visualisation des budgets cumulés par année :")
display_stacked_barchart(editable_projects, config['first_year'])

# Lancer la simulation - Bouton dans le panneau à gauche
if st.sidebar.button("Lancer la simulation"):
    # Lancer la simulation Monte Carlo
    st.session_state.simulation_results = monte_carlo_simulation(editable_projects, config['budget_max_per_year_kEUR'], config['max_iterations'])

    # Filtrer les solutions viables
    filtered_solutions = filter_solutions(st.session_state.simulation_results, config['profitability_threshold_kEUR'])

    # Si des solutions sont disponibles, afficher les deux premiers graphiques
    if len(filtered_solutions):
        display_general_graphs(filtered_solutions, config['profitability_threshold_kEUR'])

        # Liste déroulante pour sélectionner un scénario
        selected_scenario = st.selectbox(
            "Sélectionnez un scénario pour voir sa distribution :",
            [f"Scénario {i+1}" for i in range(len(filtered_solutions))]
        )
        
        # Afficher la distribution du scénario sélectionné
        scenario_index = int(selected_scenario.split()[1]) - 1
        display_selected_scenario_distribution(filtered_solutions[scenario_index], editable_projects, config['first_year'], config['profitability_threshold_kEUR'])
    else:
        st.write("Aucune solution n'a respecté le seuil de rentabilité.")
elif st.session_state.simulation_results is not None:
    # Afficher les résultats sauvegardés
    filtered_solutions = filter_solutions(st.session_state.simulation_results, config['profitability_threshold_kEUR'])

    if len(filtered_solutions):
        display_general_graphs(filtered_solutions, config['profitability_threshold_kEUR'])
        
        selected_scenario = st.selectbox(
            "Sélectionnez un scénario pour voir sa distribution :",
            [f"Scénario {i+1}" for i in range(len(filtered_solutions))]
        )
        
        scenario_index = int(selected_scenario.split()[1]) - 1
        display_selected_scenario_distribution(filtered_solutions[scenario_index], editable_projects, config['first_year'], config['profitability_threshold_kEUR'])