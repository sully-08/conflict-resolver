"""
test_module2.py — Test unitaire du Module 2 : Extraction des blocs
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from module1_detection  import detect_conflicts_in_text
from module2_extraction import extract_conflict_blocks, get_code_versions

print("=" * 55)
print("  TEST MODULE 2 — Extraction des blocs")
print("=" * 55)

# ── Test 1 : extraction simple ───────────────────────────────────
print("\n[Test 1] Extraction d'un bloc simple")
code = """\
def f(x):
<<<<<<< LOCAL
    return x + 1
=======
    return x * 2
>>>>>>> REMOTE
"""
rapport = detect_conflicts_in_text(code, "f.py")
blocs   = extract_conflict_blocks(rapport)

assert len(blocs) == 1,                     "ÉCHEC : un bloc attendu"
assert blocs[0]["block_index"] == 1
print("  → 1 bloc extrait           : OK")

code_a, code_b = get_code_versions(blocs[0])
assert "x + 1" in code_a,                  "ÉCHEC : version A incorrecte"
assert "x * 2" in code_b,                  "ÉCHEC : version B incorrecte"
print(f"  → Version A               : {code_a.strip()}")
print(f"  → Version B               : {code_b.strip()}")

# ── Test 2 : labels des branches ─────────────────────────────────
print("\n[Test 2] Labels de branches récupérés")
assert blocs[0]["label_a"] == "LOCAL",     "ÉCHEC : label A incorrect"
print(f"  → Label A                 : {blocs[0]['label_a']}")
print(f"  → Label B                 : {blocs[0]['label_b']}")

# ── Test 3 : deux blocs dans le même fichier ─────────────────────
print("\n[Test 3] Extraction de deux blocs")
code2 = """\
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
rapport2 = detect_conflicts_in_text(code2, "double.py")
blocs2   = extract_conflict_blocks(rapport2)
assert len(blocs2) == 2,                   "ÉCHEC : deux blocs attendus"
a1, b1 = get_code_versions(blocs2[0])
a2, b2 = get_code_versions(blocs2[1])
assert "x = 1" in a1 and "x = 2" in b1
assert "y = 10" in a2 and "y = 20" in b2
print(f"  → Bloc 1 — A: {a1.strip()!r}  B: {b1.strip()!r}  : OK")
print(f"  → Bloc 2 — A: {a2.strip()!r}  B: {b2.strip()!r}  : OK")

# ── Test 4 : contenu multilignes ─────────────────────────────────
print("\n[Test 4] Bloc avec plusieurs lignes par version")
code3 = """\
<<<<<<< A
def f():
    x = 1
    return x
=======
def f():
    x = 2
    y = 3
    return x + y
>>>>>>> B
"""
rapport3 = detect_conflicts_in_text(code3, "multi.py")
blocs3   = extract_conflict_blocks(rapport3)
a3, b3   = get_code_versions(blocs3[0])
assert a3.count("\n") >= 2,                "ÉCHEC : version A multiligne attendue"
assert b3.count("\n") >= 3,                "ÉCHEC : version B multiligne attendue"
print(f"  → Version A ({a3.count(chr(10))+1} lignes)    : OK")
print(f"  → Version B ({b3.count(chr(10))+1} lignes)    : OK")

print("\n" + "=" * 55)
print("  MODULE 2 — Tous les tests sont passés ✓")
print("=" * 55)
