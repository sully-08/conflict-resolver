"""
test_module5.py — Test unitaire du Module 5 : Explication en langage naturel
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module5_explication import build_prompt, explain_conflict, _fallback_explanation

print("=" * 55)
print("  TEST MODULE 5 — Explication (LLM / Gemini)")
print("=" * 55)

# Rapport de comparaison simulé pour les tests
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
    "calls_at_risk": [{"name": "calculerTaxe", "args": [], "in_function": "f"}]
}

RAPPORT_SIGNATURE = {
    "conflict_type": "SEMANTIQUE_SIGNATURE",
    "removed_functions": [],
    "added_functions": [],
    "param_changes": {
        "calculer_total": {
            "version_a": ["prix", "quantite", "devise"],
            "version_b": ["prix", "quantite"]
        }
    },
    "calls_at_risk": []
}

# ── Test 1 : construction du prompt ──────────────────────────────
print("\n[Test 1] Construction du prompt")
prompt = build_prompt("return x + y", "return x * y", RAPPORT_INTRA)
assert "VERSION A" in prompt,             "ÉCHEC : section VERSION A absente"
assert "VERSION B" in prompt,             "ÉCHEC : section VERSION B absente"
assert "DIAGNOSTIC STRUCTUREL" in prompt, "ÉCHEC : section DIAGNOSTIC absente"
assert "INTRA_METHODE" in prompt,         "ÉCHEC : type de conflit absent du prompt"
assert "return x + y" in prompt,          "ÉCHEC : code A absent du prompt"
assert "return x * y" in prompt,          "ÉCHEC : code B absent du prompt"
print("  → Prompt correctement construit : OK")
print(f"  → Longueur du prompt      : {len(prompt)} caractères")

# ── Test 2 : prompt inclut les infos de renommage ────────────────
print("\n[Test 2] Prompt avec infos de renommage")
prompt2 = build_prompt("def calculerTaxe(): pass", "def calculerTVA(): pass", RAPPORT_RENOMMAGE)
assert "calculerTaxe" in prompt2, "ÉCHEC : fonction supprimée absente du prompt"
assert "calculerTVA"  in prompt2, "ÉCHEC : fonction ajoutée absente du prompt"
print("  → Fonctions renommées présentes dans le prompt : OK")

# ── Test 3 : prompt inclut les changements de signature ──────────
print("\n[Test 3] Prompt avec changement de signature")
prompt3 = build_prompt(
    "def calculer_total(prix, quantite, devise): pass",
    "def calculer_total(prix, quantite): pass",
    RAPPORT_SIGNATURE
)
assert "calculer_total" in prompt3, "ÉCHEC : fonction modifiée absente du prompt"
assert "devise"         in prompt3, "ÉCHEC : paramètre 'devise' absent du prompt"
print("  → Changements de signature présents dans le prompt : OK")

# ── Test 4 : fallback statique — INTRA_METHODE ───────────────────
print("\n[Test 4] Fallback statique — INTRA_METHODE")
fallback = _fallback_explanation(RAPPORT_INTRA)
assert "NATURE DU CONFLIT"      in fallback, "ÉCHEC : section 1 absente"
assert "DIFFÉRENCES OBSERVÉES"  in fallback, "ÉCHEC : section 2 absente"
assert "RISQUES POTENTIELS"     in fallback, "ÉCHEC : section 3 absente"
assert "INTRA_METHODE"          in fallback, "ÉCHEC : type absent du fallback"
print("  → Structure du fallback correcte : OK")

# ── Test 5 : fallback statique — RENOMMAGE ───────────────────────
print("\n[Test 5] Fallback statique — STRUCTUREL_RENOMMAGE")
fallback2 = _fallback_explanation(RAPPORT_RENOMMAGE)
assert "calculerTaxe" in fallback2, "ÉCHEC : fonction supprimée absente du fallback"
assert "calculerTVA"  in fallback2, "ÉCHEC : fonction ajoutée absente du fallback"
print("  → Fonctions renommées dans le fallback : OK")

# ── Test 6 : fallback statique — SIGNATURE ───────────────────────
print("\n[Test 6] Fallback statique — SEMANTIQUE_SIGNATURE")
fallback3 = _fallback_explanation(RAPPORT_SIGNATURE)
assert "calculer_total" in fallback3, "ÉCHEC : fonction absente du fallback"
assert "devise"         in fallback3, "ÉCHEC : paramètre absent du fallback"
print("  → Changement de signature dans le fallback : OK")

# ── Test 7 : appel API réel (Gemini) ─────────────────────────────
print("\n[Test 7] Appel API Gemini (réel)")
code_a = "def f(x):\n    return x + 1"
code_b = "def f(x):\n    return x * 2"
explication = explain_conflict(code_a, code_b, RAPPORT_INTRA)
assert isinstance(explication, str),  "ÉCHEC : la réponse doit être une chaîne"
assert len(explication) > 50,         "ÉCHEC : réponse trop courte"
# Vérifie qu'au moins une section est présente (API ou fallback)
has_section = any(s in explication for s in [
    "NATURE DU CONFLIT", "DIFFÉRENCES", "RISQUES", "conflit", "Type identifié"
])
assert has_section, "ÉCHEC : aucune section de résultat détectée"
print(f"  → Réponse reçue ({len(explication)} caractères) : OK")
print(f"  → Aperçu : {explication[:5000].strip()}...")

print("\n" + "=" * 55)
print("  MODULE 5 — Tous les tests sont passés ")
print("=" * 55)
