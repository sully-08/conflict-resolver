def calculer_total(prix, quantite):
    return prix * quantite

def appliquer_remise(prix, remise):
    total = calculer_total(prix, 1)
    return total - remise