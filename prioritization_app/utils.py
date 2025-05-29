# utils.py - pour des fonctions utilitaires, si besoin à l'avenir
# Vous pouvez ajouter ici des fonctions qui seront réutilisées à travers différents fichiers du projet.
# Cela permet de centraliser certaines logiques de traitement et d'éviter les duplications.

def format_currency(value, unit='kEUR'):
    """
    Formate une valeur numérique avec une unité monétaire.
    Ex: 1000 -> '1000 kEUR'
    """
    return f"{value} {unit}"