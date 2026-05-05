"""
test_module6.py — Test unitaire du Module 6 : Aide à la résolution
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module6_resolution import generate_resolution, RESOLUTION_GUIDES

print("=" * 55)
print("  TEST MODULE 6 — Aide à la résolution")
print("=" * 55)

EXPLICATION = "Explication de test générée par le LLM."

RAPPORT_INTRA = {
    "conflict_type": "INTRA_METHODE",
    "removed_functions": [],
    "added_functions": [],
    "param_changes": {},
    "calls_at_risk": []
}

RAPPORT_RENOMMAGE = {
    "conflict_type": "STRUCTUREL_RENOMMAGE",
    "removed_functions": ["calculerTaxe"],
    "added_functions": ["calculerTVA"],
    "param_changes": {},
    "calls_at_risk": [{"name": "calculerTaxe", "args": [], "in_function": "facture"}]
}

RAPPORT_SIGNATURE = {
    "conflict_type": "SEMANTIQUE_SIGNATURE",
    "removed_functions": ["payer"],
    "added_functions": ["appliquer_coupon"],
    "param_changes": {
        "calculer_total": {
            "version_a": ["prix", "quantite", "devise"],
            "version_b": ["prix", "quantite"]
        }
    },
    "calls_at_risk": []
}

RAPPORT_MIXTE = {
    "conflict_type": "MIXTE",
    "removed_functions": ["ancienne_fn"],
    "added_functions": ["nouvelle_fn"],
    "param_changes": {"f": {"version_a": ["x"], "version_b": ["x", "y"]}},
    "calls_at_risk": [{"name": "ancienne_fn", "args": [], "in_function": "g"}]
}

# ── Test 1 : guide INTRA_METHODE ─────────────────────────────────
print("\n[Test 1] Guide pour INTRA_METHODE")
res = generate_resolution(RAPPORT_INTRA, EXPLICATION)
assert res["conflict_type"] == "INTRA_METHODE",   "ÉCHEC : mauvais type"
assert res["titre"]         != "",                "ÉCHEC : titre vide"
assert len(res["actions"])  >= 3,                 "ÉCHEC : pas assez d'actions"
assert res["analyse_conflit"] == EXPLICATION,     "ÉCHEC : explication non transmise"
assert res["notes_specifiques"] == [],            "ÉCHEC : notes non vides attendues vides"
print(f"  → Titre                   : {res['titre']}")
print(f"  → Nombre d'actions        : {len(res['actions'])}")
print(f"  → Notes spécifiques       : {res['notes_specifiques']}")

# ── Test 2 : guide STRUCTUREL_RENOMMAGE ──────────────────────────
print("\n[Test 2] Guide pour STRUCTUREL_RENOMMAGE")
res2 = generate_resolution(RAPPORT_RENOMMAGE, EXPLICATION)
assert res2["conflict_type"] == "STRUCTUREL_RENOMMAGE", "ÉCHEC : mauvais type"
assert len(res2["actions"])  >= 4,                      "ÉCHEC : pas assez d'actions"
notes = res2["notes_specifiques"]
assert any("calculerTaxe" in n for n in notes), "ÉCHEC : fonction supprimée absente des notes"
assert any("calculerTVA"  in n for n in notes), "ÉCHEC : fonction ajoutée absente des notes"
assert any("Appels"       in n for n in notes), "ÉCHEC : appels à risque absents des notes"
print(f"  → Titre                   : {res2['titre']}")
print(f"  → Notes spécifiques       :")
for note in notes:
    print(f"      {note}")

# ── Test 3 : guide SEMANTIQUE_SIGNATURE ──────────────────────────
print("\n[Test 3] Guide pour SEMANTIQUE_SIGNATURE")
res3 = generate_resolution(RAPPORT_SIGNATURE, EXPLICATION)
assert res3["conflict_type"] == "SEMANTIQUE_SIGNATURE", "ÉCHEC : mauvais type"
notes3 = res3["notes_specifiques"]
assert any("calculer_total" in n for n in notes3), "ÉCHEC : fonction modifiée absente"
assert any("devise"         in n for n in notes3), "ÉCHEC : paramètre absent des notes"
print(f"  → Titre                   : {res3['titre']}")
print(f"  → Notes spécifiques       :")
for note in notes3:
    print(f"      {note}")

# ── Test 4 : guide MIXTE ─────────────────────────────────────────
print("\n[Test 4] Guide pour MIXTE")
res4 = generate_resolution(RAPPORT_MIXTE, EXPLICATION)
assert res4["conflict_type"] == "MIXTE", "ÉCHEC : mauvais type"
assert len(res4["actions"])  >= 3,       "ÉCHEC : pas assez d'actions"
print(f"  → Titre                   : {res4['titre']}")
print(f"  → Nombre d'actions        : {len(res4['actions'])}")

# ── Test 5 : type inconnu → fallback MIXTE ───────────────────────
print("\n[Test 5] Type inconnu → fallback sur MIXTE")
rapport_inconnu = {
    "conflict_type": "TYPE_INEXISTANT",
    "removed_functions": [], "added_functions": [],
    "param_changes": {}, "calls_at_risk": []
}
res5 = generate_resolution(rapport_inconnu, EXPLICATION)
assert res5["titre"] == RESOLUTION_GUIDES["MIXTE"]["titre"], \
    "ÉCHEC : fallback MIXTE attendu pour type inconnu"
print(f"  → Fallback activé         : {res5['titre']}  ✓")

# ── Test 6 : vérification des clés du résultat ───────────────────
print("\n[Test 6] Structure complète du résultat")
cles_attendues = [
    "conflict_type", "titre", "analyse_conflit",
    "enjeux", "actions", "notes_specifiques"
]
for cle in cles_attendues:
    assert cle in res, f"ÉCHEC : clé '{cle}' absente du résultat"
print(f"  → Clés présentes          : {list(res.keys())}")
print("  → Structure complète      : OK")

print("\n" + "=" * 55)
print("  MODULE 6 — Tous les tests sont passés ✓")
print("=" * 55)
