"""
test_module4.py — Test unitaire du Module 4 : Comparaison structurelle
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module3_ast         import analyze_versions
from module4_comparaison import compare_asts

print("=" * 55)
print("  TEST MODULE 4 — Comparaison structurelle")
print("=" * 55)

# ── Test 1 : conflit INTRA_METHODE ───────────────────────────────
print("\n[Test 1] Classification INTRA_METHODE")
code_a = """\
def traiter(montant):
    if montant > 0:
        return montant * 1.2
"""
code_b = """\
def traiter(montant):
    print(f"montant={montant}")
    if montant >= 0:
        return montant * 1.2
"""
ast_a, ast_b = analyze_versions(code_a, code_b)
rapport = compare_asts(ast_a, ast_b)
assert rapport["conflict_type"] == "INTRA_METHODE", \
    f"ÉCHEC : attendu INTRA_METHODE, obtenu {rapport['conflict_type']}"
assert rapport["param_changes"]      == {},  "ÉCHEC : aucun changement de params attendu"
assert rapport["removed_functions"]  == [],  "ÉCHEC : aucune suppression attendue"
print(f"  → Type détecté            : {rapport['conflict_type']}  ✓")

# ── Test 2 : conflit STRUCTUREL_RENOMMAGE ────────────────────────
print("\n[Test 2] Classification STRUCTUREL_RENOMMAGE")
code_a2 = """\
def calculerTVA(prix, taux):
    return prix * taux

def appliquer_remise(prix):
    return calculerTVA(prix, 0.2)
"""
code_b2 = """\
def calculerTaxe(prix, taux):
    return prix * taux

def generer_facture(prix):
    taxe = calculerTaxe(prix, 0.2)
    return prix + taxe
"""
ast_a2, ast_b2 = analyze_versions(code_a2, code_b2)
rapport2 = compare_asts(ast_a2, ast_b2)
assert rapport2["conflict_type"] == "STRUCTUREL_RENOMMAGE", \
    f"ÉCHEC : attendu STRUCTUREL_RENOMMAGE, obtenu {rapport2['conflict_type']}"
assert "calculerTVA" in rapport2["removed_functions"] or \
       "calculerTaxe" in rapport2["added_functions"],  "ÉCHEC : renommage non détecté"
print(f"  → Type détecté            : {rapport2['conflict_type']}  ✓")
print(f"  → Supprimées              : {rapport2['removed_functions']}")
print(f"  → Ajoutées                : {rapport2['added_functions']}")
print(f"  → Appels à risque         : {[c['name'] for c in rapport2['calls_at_risk']]}")

# ── Test 3 : conflit SEMANTIQUE_SIGNATURE ────────────────────────
print("\n[Test 3] Classification SEMANTIQUE_SIGNATURE")
code_a3 = """\
def calculer_total(prix, quantite, devise):
    return prix * quantite
"""
code_b3 = """\
def calculer_total(prix, quantite):
    return prix * quantite
"""
ast_a3, ast_b3 = analyze_versions(code_a3, code_b3)
rapport3 = compare_asts(ast_a3, ast_b3)
assert rapport3["conflict_type"] == "SEMANTIQUE_SIGNATURE", \
    f"ÉCHEC : attendu SEMANTIQUE_SIGNATURE, obtenu {rapport3['conflict_type']}"
assert "calculer_total" in rapport3["param_changes"], \
    "ÉCHEC : changement de paramètres non détecté"
ch = rapport3["param_changes"]["calculer_total"]
assert "devise" in ch["version_a"],   "ÉCHEC : 'devise' attendu dans version A"
assert "devise" not in ch["version_b"],"ÉCHEC : 'devise' absent de version B attendu"
print(f"  → Type détecté            : {rapport3['conflict_type']}  ✓")
print(f"  → Paramètres modifiés     : {rapport3['param_changes']}")

# ── Test 4 : code identique → INTRA_METHODE ──────────────────────
print("\n[Test 4] Versions identiques → INTRA_METHODE")
code_id = "def f(x): return x"
ast_id1, ast_id2 = analyze_versions(code_id, code_id)
rapport4 = compare_asts(ast_id1, ast_id2)
assert rapport4["conflict_type"] == "INTRA_METHODE"
assert rapport4["param_changes"]     == {}
assert rapport4["removed_functions"] == []
assert rapport4["added_functions"]   == []
print(f"  → Type                    : {rapport4['conflict_type']}  ✓")
print(f"  → Aucune différence       : OK")

print("\n" + "=" * 55)
print("  MODULE 4 — Tous les tests sont passés ✓")
print("=" * 55)
