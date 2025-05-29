import plotly.graph_objs as go
import streamlit as st
import numpy as np
import pandas as pd

def display_project_distributions(projects):
    fig = go.Figure()

    for i, project in projects.iterrows():
        distribution = np.random.normal(project['NPV Moyenne (kEUR)'], project['Variance NPV (kEUR)'], 1000)
        
        fig.add_trace(go.Histogram(
            x=distribution,
            name=project['Projet'],
            opacity=0.6,
            nbinsx=50
        ))

    fig.update_layout(
        title="Distributions des NPV pour chaque projet",
        xaxis_title="Valeurs de NPV (kEUR)",
        yaxis_title="Fréquence",
        barmode='overlay'
    )

    st.plotly_chart(fig)

# --- Stacked Barchart pour visualiser le budget total par année et par projet ---
def display_stacked_barchart(projects, first_year, title="Budget cumulé par année pour chaque projet"):
    fig = go.Figure()

    # Renommer les années dynamiquement en fonction de la première année
    x_axis_labels = [f"Année {i+1} ({first_year + i})" for i in range(5)]
    years = ['Budget année 1 (kEUR)', 'Budget année 2 (kEUR)', 'Budget année 3 (kEUR)', 'Budget année 4 (kEUR)', 'Budget année 5 (kEUR)']

    for i, project in projects.iterrows():
        fig.add_trace(go.Bar(
            x=x_axis_labels,
            y=[project[year] for year in years],
            name=project['Projet']
        ))

    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title="Années",
        yaxis_title="Budget cumulé (kEUR)",
        legend_title="Projets"
    )

    st.plotly_chart(fig)

def display_general_graphs(solutions, profitability_threshold_kEUR):
    fig = go.Figure()

    for i, solution in enumerate(solutions):
        fig.add_trace(go.Histogram(
            x=solution['total_result_distribution'],
            name=f"Scénario {i+1}: {len(solution['selected_projects'])} projets",
            opacity=0.6
        ))

    fig.add_vline(x=profitability_threshold_kEUR, line=dict(color="red", dash="dash"), annotation_text="Seuil de rentabilité", annotation_position="top right")
    fig.update_layout(
        title="Distribution des résultats des scénarios retenus",
        xaxis_title="Résultats (kEUR)",
        yaxis_title="Fréquence",
        barmode='overlay'
    )
    st.plotly_chart(fig)

    budget_list = [solution['total_budget_per_year'].sum() for solution in solutions]
    prob_list = [solution['prob_above_threshold'] for solution in solutions]
    project_list = [', '.join(solution['selected_projects']) for solution in solutions]

    scenario_labels = [f"Scénario {i+1}" for i in range(len(solutions))]
    hover_text = [f"{label}: {projects}" for label, projects in zip(scenario_labels, project_list)]

    fig_summary = go.Figure()
    fig_summary.add_trace(go.Scatter(x=budget_list, y=prob_list, mode='markers', text=hover_text, marker=dict(size=10),
                                     hoverinfo="text+name", name="Scénarios"))
    fig_summary.update_layout(
        title="Synthèse des solutions",
        xaxis_title="Budget total (kEUR)",
        yaxis_title="Probabilité de dépassement du seuil de rentabilité",
        hovermode='closest'
    )
    st.plotly_chart(fig_summary)

    # Affichage du tableau des scénarios retenus
    st.write("Tableau des scénarios retenus:")
    scenario_data = {
        'Scénario': scenario_labels,
        'Budget total (kEUR)': budget_list,
        'Probabilité (> seuil)': prob_list,
        'Projets sélectionnés': project_list
    }
    scenario_df = pd.DataFrame(scenario_data)
    st.dataframe(scenario_df)

def display_selected_scenario_distribution(solution, projects, first_year, profitability_threshold_kEUR):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=solution['total_result_distribution'],
        name=f"Scénario : {len(solution['selected_projects'])} projets",
        opacity=0.6
    ))

    fig.add_vline(x=profitability_threshold_kEUR, line=dict(color="red", dash="dash"), annotation_text="Seuil de rentabilité", annotation_position="top right")

    prob_below_threshold = np.mean(solution['total_result_distribution'] < profitability_threshold_kEUR)
    fig.add_annotation(text=f"Probabilité (< seuil) : {prob_below_threshold:.2f}",
                       xref="paper", yref="paper", x=0.5, y=1.1, showarrow=False)

    fig.update_layout(
        title=f"Distribution des résultats (Budget total : {solution['total_budget_per_year'].sum()} kEUR)",
        xaxis_title="Résultats (kEUR)",
        yaxis_title="Fréquence",
        barmode='overlay'
    )

    st.plotly_chart(fig)

    # Afficher la liste des projets sélectionnés
    st.write("Projets dans ce scénario :")
    st.write(', '.join(solution['selected_projects']))

    # Extraire les budgets des projets sélectionnés
    selected_projects_df = projects[projects['Projet'].isin(solution['selected_projects'])]

    # Afficher le stacked barchart pour les budgets des projets sélectionnés
    display_stacked_barchart(selected_projects_df, first_year, title="Budget cumulé par année pour le scénario sélectionné")