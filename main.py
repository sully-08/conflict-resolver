"""
main.py
Système d'aide au diagnostic et à la résolution des conflits de fusion Git
"""

import sys
import os
import glob

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "modules"
    )
)

from modules.module1_detection import detect_conflicts
from modules.module2_extraction import (
    extract_conflict_blocks,
    get_code_versions
)
from modules.module3_ast import analyze_versions
from modules.module4_comparaison import compare_asts
from modules.module5_explication import generate_resolution_report


def run_pipeline(files: dict):

    reports = []

    detected_files = detect_conflicts(files)

    if not detected_files:
        return reports

    for file_report in detected_files:

        blocks = extract_conflict_blocks(file_report)

        for block in blocks:

            code_a, code_b = get_code_versions(block)

            ast_a, ast_b = analyze_versions(
                code_a,
                code_b
            )

            comparison = compare_asts(
                ast_a,
                ast_b
            )

            report = generate_resolution_report(
                code_a,
                code_b,
                comparison
            )

            reports.append({
                "filename": file_report["filename"],
                "block": block["block_index"],
                "report": report
            })

    return reports


def print_final_report(reports):

    if not reports:
        print("Aucun conflit détecté.")
        return

    for r in reports:

        print("=" * 80)
        print(f"Fichier : {r['filename']}")
        print(f"Bloc : {r['block']}")
        print("=" * 80)

        print(r["report"])
        print()


def scan_repo_for_conflicts():

    files = {}

    for filepath in glob.glob("**/*.py", recursive=True):

        if any(skip in filepath for skip in [
            "modules/",
            "tests/",
            "test_"
        ]):
            continue

        try:

            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            if "<<<<<<<" in content:
                files[filepath] = content

        except Exception:
            pass

    return files


if __name__ == "__main__":

    github_mode = "--github-mode" in sys.argv

    if github_mode:

        files = scan_repo_for_conflicts()

        if not files:
            print("Aucun conflit détecté.")
            sys.exit(0)

    else:
        files = scan_repo_for_conflicts()

    reports = run_pipeline(files)

    print_final_report(reports)