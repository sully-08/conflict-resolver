def calculer_total_TTC(prix, quantite, taux_tva=0.2):
    return prix * quantite * (1 + taux_tva)

def appliquer_remise(prix, remise):
<<<<<<< HEAD
    total = calculer_total(prix, 1)
    return total - remise

def generer_facture(client, prix, quantite):
    total = calculer_total(prix, quantite)
    return {"client": client, "total": total}
=======
    total = calculer_total_TTC(prix, 1)
    return total - remise
>>>>>>> feature/refactoring
