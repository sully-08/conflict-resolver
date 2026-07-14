def calculer_total(prix, quantite, remise=0):
    """Calcule le total d'une facture."""
    total = prix * quantite
    return total - remise