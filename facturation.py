def calculer_total(prix, quantite):
    return prix * quantite

def appliquer_remise(prix, remise):
    total = calculer_total(prix, 1)
    return total - remise

def generer_facture(client, prix, quantite):
    total = calculer_total(prix, quantite)
    return {"client": client, "total": total}