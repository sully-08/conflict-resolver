def calculer_prix_total(prix_unitaire, quantite, reduction=0):
    total = prix_unitaire * quantite
    return total - reduction
