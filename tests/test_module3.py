"""
test_module3.py — Test unitaire du Module 3 : Analyse syntaxique AST
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module3_ast import parse_code, analyze_versions

print("=" * 55)
print("  TEST MODULE 3 — Analyse syntaxique (AST)")
print("=" * 55)

# ── Test 1 : détection d'une fonction ───────────────────────────
print("\n[Test 1] Détection d'une définition de fonction")
code = """\
def calculer(x, y):
    return x + y
"""
ast = parse_code(code)
assert "calculer" in ast["elements"]["functions"], "ÉCHEC : fonction non détectée"
assert ast["has_errors"] == False,                 "ÉCHEC : erreur AST inattendue"
print(f"  → Fonctions détectées     : {ast['elements']['functions']}")
print(f"  → Erreurs AST             : {ast['has_errors']}")

# ── Test 2 : extraction des paramètres ──────────────────────────
print("\n[Test 2] Extraction des paramètres")
assert ast["elements"]["parameters"]["calculer"] == ["x", "y"], \
    "ÉCHEC : paramètres incorrects"
print(f"  → Paramètres de calculer  : {ast['elements']['parameters']['calculer']}")

# ── Test 3 : détection des appels de fonctions ──────────────────
print("\n[Test 3] Détection des appels de fonctions")
code2 = """\
def traiter(a):
    result = calculer(a, 10)
    print(result)
    return result
"""
ast2  = parse_code(code2)
noms  = [c["name"] for c in ast2["elements"]["calls"]]
assert "calculer" in noms, "ÉCHEC : appel 'calculer' non détecté"
assert "print"    in noms, "ÉCHEC : appel 'print' non détecté"
print(f"  → Appels détectés         : {noms}")

# ── Test 4 : code incomplet (robustesse Tree-sitter) ────────────
print("\n[Test 4] Code incomplet — robustesse Tree-sitter")
code_incomplet = """\
def f(x):
    if x > 0:
        return x +
"""
ast3 = parse_code(code_incomplet)
assert "f" in ast3["elements"]["functions"], "ÉCHEC : fonction non détectée malgré erreur"
print(f"  → Fonction détectée malgré erreur syntaxique : OK")
print(f"  → has_errors              : {ast3['has_errors']}")

# ── Test 5 : plusieurs fonctions ────────────────────────────────
print("\n[Test 5] Plusieurs fonctions dans le même code")
code4 = """\
def addition(a, b):
    return a + b

def soustraction(a, b):
    return a - b

def multiplier(a, b, c):
    return a * b * c
"""
ast4 = parse_code(code4)
fonctions = ast4["elements"]["functions"]
assert len(fonctions) == 3,         "ÉCHEC : 3 fonctions attendues"
assert "addition"     in fonctions
assert "soustraction" in fonctions
assert "multiplier"   in fonctions
print(f"  → Fonctions détectées     : {fonctions}")
print(f"  → Paramètres             : {ast4['elements']['parameters']}")

# ── Test 6 : analyze_versions ────────────────────────────────────
print("\n[Test 6] analyze_versions() sur deux versions")
code_a = "def f(x): return x + 1"
code_b = "def f(x, y): return x + y"
ast_a, ast_b = analyze_versions(code_a, code_b)
assert "f" in ast_a["elements"]["functions"]
assert "f" in ast_b["elements"]["functions"]
assert ast_a["elements"]["parameters"]["f"] == ["x"]
assert ast_b["elements"]["parameters"]["f"] == ["x", "y"]
print("  → Deux AST générés correctement : OK")

print("\n" + "=" * 55)
print("  MODULE 3 — Tous les tests sont passés ✓")
print("=" * 55)
