<<<<<<< HEAD
def calculer_prix_total(prix_unitaire, quantite, reduction=0):
    total = prix_unitaire * quantite
    return total - reduction
=======
def calculer_montant_TTC(prix_unitaire, quantite, taux_tva=0.18):
    montant_ht = prix_unitaire * quantite
    return montant_ht * (1 + taux_tva)
>>>>>>> feature/refactoring
