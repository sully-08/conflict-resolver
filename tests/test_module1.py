"""
test_module1.py — Test unitaire du Module 1 : Détection des conflits
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module1_detection import detect_conflicts, detect_conflicts_in_text

print("=" * 55)
print("  TEST MODULE 1 — Détection des conflits")
print("=" * 55)

# ── Test 1 : fichier AVEC conflit ────────────────────────────────
print("\n[Test 1] Fichier avec un conflit")
code_avec_conflit = """\
def calcul(x):
<<<<<<< branche_a
    return x + 1
=======
    return x * 2
>>>>>>> branche_b
"""
rapport = detect_conflicts_in_text(code_avec_conflit, "calcul.py")
assert rapport["has_conflict"] == True,        "ÉCHEC : conflit non détecté"
assert rapport["conflict_count"] == 1,         "ÉCHEC : nombre de zones incorrect"
assert rapport["conflict_zones"][0]["start_line"] == 2
print("  → Conflit détecté         : OK")
print(f"  → Nombre de zones         : {rapport['conflict_count']}")
print(f"  → Ligne début / fin       : {rapport['conflict_zones'][0]}")

# ── Test 2 : fichier SANS conflit ────────────────────────────────
print("\n[Test 2] Fichier sans conflit")
code_propre = """\
def calcul(x):
    return x + 1
"""
rapport2 = detect_conflicts_in_text(code_propre, "propre.py")
assert rapport2["has_conflict"] == False, "ÉCHEC : faux positif détecté"
print("  → Aucun faux positif       : OK")

# ── Test 3 : plusieurs zones de conflit ──────────────────────────
print("\n[Test 3] Fichier avec deux zones de conflit")
code_double = """\
<<<<<<< A
x = 1
=======
x = 2
>>>>>>> B
<<<<<<< A
y = 10
=======
y = 20
>>>>>>> B
"""
rapport3 = detect_conflicts_in_text(code_double, "double.py")
assert rapport3["conflict_count"] == 2, "ÉCHEC : deux zones attendues"
print(f"  → Deux zones détectées    : OK ({rapport3['conflict_count']} zones)")

# ── Test 4 : via la fonction principale detect_conflicts ─────────
print("\n[Test 4] Fonction detect_conflicts() sur plusieurs fichiers")
fichiers = {
    "ok.py":      "def f(): return 1",
    "conflit.py": "<<<<<<< A\nx=1\n=======\nx=2\n>>>>>>> B\n"
}
resultats = detect_conflicts(fichiers)
assert len(resultats) == 1,                    "ÉCHEC : un seul fichier en conflit attendu"
assert resultats[0]["filename"] == "conflit.py"
print(f"  → 1 fichier en conflit retourné : OK")

print("\n" + "=" * 55)
print("  MODULE 1 — Tous les tests sont passés ✓")
print("=" * 55)
