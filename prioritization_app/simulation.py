import numpy as np

def monte_carlo_simulation(projects, budget_max_per_year_kEUR, max_iterations=1000):
    solutions = []
    seen_combinations = set()

    for _ in range(max_iterations):
        selected_projects = []
        total_budget_per_year = np.zeros(5)
        total_result_distribution = np.zeros(1000)

        projects_sample = projects.sample(frac=1).reset_index(drop=True)

        for _, project in projects_sample.iterrows():
            project_budget_per_year = [
                project['Budget année 1 (kEUR)'],
                project['Budget année 2 (kEUR)'],
                project['Budget année 3 (kEUR)'],
                project['Budget année 4 (kEUR)'],
                project['Budget année 5 (kEUR)']
            ]

            # Vérification du respect du budget pour chaque année
            if np.all(total_budget_per_year + project_budget_per_year <= budget_max_per_year_kEUR):
                total_budget_per_year += project_budget_per_year
                selected_projects.append(project['Projet'])

                result_distribution = np.random.normal(project['NPV Moyenne (kEUR)'], project['Variance NPV (kEUR)'], 1000)
                total_result_distribution += result_distribution
            else:
                continue

        selected_projects_tuple = tuple(sorted(selected_projects))
        if selected_projects_tuple not in seen_combinations and selected_projects:
            seen_combinations.add(selected_projects_tuple)
            solutions.append({
                'selected_projects': selected_projects,
                'total_budget_per_year': total_budget_per_year,
                'total_result_distribution': total_result_distribution
            })

    return solutions

def filter_solutions(solutions, profitability_threshold_kEUR):
    valid_solutions = []

    for solution in solutions:
        prob_above_threshold = np.mean(solution['total_result_distribution'] > profitability_threshold_kEUR)

        if prob_above_threshold > 0:
            solution['prob_above_threshold'] = prob_above_threshold
            valid_solutions.append(solution)

    valid_solutions.sort(key=lambda x: x['prob_above_threshold'], reverse=True)

    return valid_solutions