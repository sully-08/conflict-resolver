"""
main.py — Système d'aide à la résolution des conflits de fusion Git
Pipeline : Détection → Extraction → AST → Comparaison → Explication → Résolution
"""

import sys
import os

# Permet d'importer les modules depuis le même dossier
sys.path.insert(0, os.path.dirname(__file__))

from modules.module1_detection   import detect_conflicts
from modules.module2_extraction  import extract_conflict_blocks, get_code_versions
from modules.module3_ast         import analyze_versions
from modules.module4_comparaison import compare_asts
from modules.module5_explication import explain_conflict
from modules.module6_resolution  import generate_resolution


def run_pipeline(files: dict) -> list:
    """
    Lance le pipeline complet sur un dictionnaire de fichiers.
    Entrée  : { "nom_fichier.py": "contenu avec marqueurs Git" }
    Sortie  : liste de rapports de résolution (un par bloc de conflit)
    """
    print("\n" + "="*60)
    print("  SYSTÈME D'AIDE À LA RÉSOLUTION DES CONFLITS DE FUSION")
    print("="*60)

    all_results = []

    # ── MODULE 1 : Détection ──────────────────────────────────────
    print("\n -- MODULE 1 : DÉTECTION ──")
    detected_files = detect_conflicts(files)

    if not detected_files:
        print("\n Aucun conflit détecté. Le code est propre.")
        return []

    for file_report in detected_files:
        print(f"\n{'─'*50}")
        print(f"Traitement : {file_report['filename']}")
        print(f"{'─'*50}")

        # ── MODULE 2 : Extraction ─────────────────────────────────
        print("\n── MODULE 2 : EXTRACTION ──")
        blocks = extract_conflict_blocks(file_report)

        for block in blocks:
            print(f"\n   Bloc {block['block_index']} / {len(blocks)}")
            code_a, code_b = get_code_versions(block)

            # ── MODULE 3 : Analyse AST ────────────────────────────
            print("\n── MODULE 3 : ANALYSE AST ──")
            ast_a, ast_b = analyze_versions(code_a, code_b)

            # ── MODULE 4 : Comparaison structurelle ───────────────
            print("\n── MODULE 4 : COMPARAISON STRUCTURELLE ──")
            comparison = compare_asts(ast_a, ast_b)

            # ── MODULE 5 : Explication ────────────────────────────
            print("\n── MODULE 5 : EXPLICATION ──")
            explanation = explain_conflict(code_a, code_b, comparison)

            # ── MODULE 6 : Résolution ─────────────────────────────
            print("\n── MODULE 6 : AIDE À LA RÉSOLUTION ──")
            resolution = generate_resolution(comparison, explanation)

            # Résultat final pour ce bloc
            result = {
                "filename": file_report["filename"],
                "block_index": block["block_index"],
                "conflict_type": comparison["conflict_type"],
                "explanation": explanation,
                "resolution": resolution
            }
            all_results.append(result)

    print("\n" + "="*60)
    print(f"  PIPELINE TERMINÉ — {len(all_results)} conflit(s) analysé(s)")
    print("="*60)
    return all_results


def print_final_report(results: list):
    """Affiche le rapport final lisible pour le développeur."""
    if not results:
        return
    print("\n\n" + "█"*60)
    print("  RAPPORT FINAL POUR LE DÉVELOPPEUR")
    print("█"*60)
    for r in results:
        print(f"\n Fichier : {r['filename']}  |  Bloc #{r['block_index']}")
        print(f"  Type   : {r['conflict_type']}")
        print("\n── EXPLICATION ──")
        print(r["explanation"])
        print("\n── GUIDE DE RÉSOLUTION ──")
        res = r["resolution"]
        print(f"Titre   : {res['titre']}")
        print(f"Enjeux  : {res['enjeux']}")
        print("Actions :")
        for i, a in enumerate(res["actions"], 1):
            print(f"  {i}. {a}")
        if res["notes_specifiques"]:
            print("Notes spécifiques :")
            for note in res["notes_specifiques"]:
                print(f"  {note}")
        print()


# ── Point d'entrée direct ──────────────────────────────────────────
if __name__ == "__main__":
    # Exemple minimal pour vérifier que le pipeline tourne
    sample = {
        "exemple.py": """\
def calculer(x, y):
<<<<<<< LOCAL
    return x + y
=======
    return x * y
>>>>>>> REMOTE
"""
    }
    results = run_pipeline(sample)
    print_final_report(results)
