import pandas as pd
import numpy as np

def generate_initial_projects(n_projects=50):
    np.random.seed(42)  # Pour la reproductibilité
    projects = []
    for i in range(n_projects):
        budget_years = [np.random.randint(50, 500) for _ in range(5)]  # Budget pour 5 ans entre 50kEUR et 500kEUR
        mean_result = np.random.randint(10, 200)  # NPV moyenne entre 10kEUR et 200kEUR
        stddev_result = np.random.randint(5, 50)  # Variance (incertitude) entre 5kEUR et 50kEUR
        projects.append({
            'Projet': f'Projet {i+1}',
            'Budget année 1 (kEUR)': budget_years[0],
            'Budget année 2 (kEUR)': budget_years[1],
            'Budget année 3 (kEUR)': budget_years[2],
            'Budget année 4 (kEUR)': budget_years[3],
            'Budget année 5 (kEUR)': budget_years[4],
            'NPV Moyenne (kEUR)': mean_result,
            'Variance NPV (kEUR)': stddev_result
        })
    return pd.DataFrame(projects)