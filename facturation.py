def calculer_total_TTC(prix, quantite, taux_tva=0.2):
    return prix * quantite * (1 + taux_tva)

def appliquer_remise(prix, remise):
    total = calculer_total_TTC(prix, 1)
    return total - remise