"""
main.py — Système d'aide à la résolution des conflits de fusion Git
"""

import sys
import os
import glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules"))

from modules.module1_detection   import detect_conflicts
from modules.module2_extraction  import extract_conflict_blocks, get_code_versions
from modules.module3_ast         import analyze_versions
from modules.module4_comparaison import compare_asts
from modules.module5_explication import explain_conflict
from modules.module6_resolution  import generate_resolution


def run_pipeline(files: dict) -> list:
    all_results = []

    detected_files = detect_conflicts(files)
    if not detected_files:
        return []

    for file_report in detected_files:
        blocks = extract_conflict_blocks(file_report)
        for block in blocks:
            code_a, code_b = get_code_versions(block)
            ast_a, ast_b   = analyze_versions(code_a, code_b)
            comparison     = compare_asts(ast_a, ast_b)
            explanation    = explain_conflict(code_a, code_b, comparison)
            resolution     = generate_resolution(comparison, explanation)

            all_results.append({
                "filename":      file_report["filename"],
                "block_index":   block["block_index"],
                "conflict_type": comparison["conflict_type"],
                "explanation":   explanation,
                "resolution":    resolution
            })

    return all_results


def print_final_report(results: list):
    if not results:
        print(" Aucun conflit détecté dans ce dépôt.")
        return

    for r in results:
        res = r["resolution"]
        print("=" * 60)
        print(f"Fichier : {r['filename']}  |  Bloc #{r['block_index']}")
        print(f" Type de conflit : {r['conflict_type']}")
        print("=" * 60)

        print("\n── EXPLICATION DU CONFLIT ──")
        print(r["explanation"])

        print("\n── GUIDE DE RÉSOLUTION ──")
        print(f" {res['titre']}")
        print(f"\nEnjeux :\n{res['enjeux']}")
        print("\nActions à effectuer :")
        for i, action in enumerate(res["actions"], 1):
            print(f"  {i}. {action}")

        if res["notes_specifiques"]:
            print("\nNotes spécifiques :")
            for note in res["notes_specifiques"]:
                print(f"  {note}")
        print()


def scan_repo_for_conflicts() -> dict:
    """Mode GitHub Actions : scanne tous les fichiers .py du dépôt."""
    fichiers = {}
    for filepath in glob.glob("**/*.py", recursive=True):
        if any(skip in filepath for skip in ["modules/", "tests/", "test_"]):
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                contenu = f.read()
            if "<<<<<<<" in contenu:
                fichiers[filepath] = contenu
        except Exception:
            continue
    return fichiers


if __name__ == "__main__":
    github_mode = "--github-mode" in sys.argv

    if github_mode:
        fichiers = scan_repo_for_conflicts()
        if not fichiers:
            print(" Aucun fichier en conflit détecté dans le dépôt.")
            sys.exit(0)
    else:
        fichiers = {
            "exemple.py": """\
def calculer(x, y):
<<<<<<< LOCAL
    return x + y
=======
    return x * y
>>>>>>> REMOTE
"""
        }

    results = run_pipeline(fichiers)
    print_final_report(results)