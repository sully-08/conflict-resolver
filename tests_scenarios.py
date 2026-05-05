"""
tests_scenarios.py — Tests des 3 scénarios de conflits
Scénario 1 : Conflit intra-méthode
Scénario 2 : Conflit structurel par renommage
Scénario 3 : Conflit sémantique / changement de signature
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import run_pipeline, print_final_report


# ══════════════════════════════════════════════════════════════════
# SCÉNARIO 1 : Conflit intra-méthode
# Dev A modifie la condition d'un if
# Dev B ajoute un log dans la même fonction
# ══════════════════════════════════════════════════════════════════

SCENARIO_1 = {
    "traitement.py": """\
def traiter_commande(montant):
<<<<<<< feature/validation
    if montant > 0:
        return montant * 1.2
=======
    print(f"Traitement commande : {montant}")
    if montant >= 0:
        return montant * 1.2
>>>>>>> feature/logging
"""
}

# ══════════════════════════════════════════════════════════════════
# SCÉNARIO 2 : Conflit structurel par renommage
# Dev A renomme calculerTaxe() en calculerTVA()
# Dev B ajoute une fonction qui appelle l'ancienne calculerTaxe()
# ══════════════════════════════════════════════════════════════════

SCENARIO_2 = {
    "facturation.py": """\
<<<<<<< feature/refactoring
def calculerTVA(prix, taux):
    return prix * taux

def appliquer_remise(prix):
    return calculerTVA(prix, 0.2)
=======
def calculerTaxe(prix, taux):
    return prix * taux

def generer_facture(prix):
    taxe = calculerTaxe(prix, 0.2)
    return prix + taxe
>>>>>>> feature/facturation
"""
}

# ══════════════════════════════════════════════════════════════════
# SCÉNARIO 3 : Conflit sémantique / changement de signature
# Dev A ajoute un paramètre obligatoire 'devise' à calculer_total()
# Dev B utilise calculer_total() sans ce nouveau paramètre
# ══════════════════════════════════════════════════════════════════

SCENARIO_3 = {
    "paiement.py": """\
<<<<<<< feature/multi-devise
def calculer_total(prix, quantite, devise):
    taux = {"EUR": 1.0, "USD": 1.1}.get(devise, 1.0)
    return prix * quantite * taux

def payer(prix, qte, devise):
    return calculer_total(prix, qte, devise)
=======
def calculer_total(prix, quantite):
    return prix * quantite

def appliquer_coupon(prix, qte, reduction):
    total = calculer_total(prix, qte)
    return total - reduction
>>>>>>> feature/coupons
"""
}


# ══════════════════════════════════════════════════════════════════
# EXÉCUTION DES TESTS
# ══════════════════════════════════════════════════════════════════

def run_all_tests():
    scenarios = [
        ("SCÉNARIO 1 — Conflit intra-méthode",           SCENARIO_1),
        ("SCÉNARIO 2 — Conflit structurel (renommage)",   SCENARIO_2),
        ("SCÉNARIO 3 — Conflit sémantique (signature)",   SCENARIO_3),
    ]

    all_results = {}

    for titre, fichiers in scenarios:
        print("\n\n" + "▓"*60)
        print(f"  {titre}")
        print("▓"*60)
        results = run_pipeline(fichiers)
        print_final_report(results)
        all_results[titre] = results

    # Tableau de synthèse
    print("\n\n" + "="*60)
    print("  TABLEAU DE SYNTHÈSE DES TESTS")
    print("="*60)
    print(f"{'Scénario':<40} {'Type détecté':<25} {'Blocs'}")
    print("-"*60)
    for titre, results in all_results.items():
        for r in results:
            print(f"{titre[:38]:<40} {r['conflict_type']:<25} #{r['block_index']}")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
