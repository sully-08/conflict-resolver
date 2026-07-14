def calculer_montant_TTC(prix_unitaire, quantite, taux_tva=0.18):
    montant_ht = prix_unitaire * quantite
    return montant_ht * (1 + taux_tva)
