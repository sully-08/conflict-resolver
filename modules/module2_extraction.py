"""
Module 2 : Extraction des blocs en conflit
Rôle : Isoler les versions A et B à partir des marqueurs Git
"""

from module1_detection import MARKER_START, MARKER_SEP, MARKER_END


def extract_conflict_blocks(detection_report: dict) -> list:
    """
    À partir du rapport de détection, extrait les blocs de conflit
    structurés en Version A (locale) et Version B (distante).
    Retourne une liste de blocs.
    """
    lines = detection_report["raw_lines"]
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith(MARKER_START):
            block = {
                "block_index": len(blocks) + 1,
                "version_a": [],
                "version_b": [],
                "label_a": lines[i].strip().replace(MARKER_START, "").strip() or "LOCAL",
                "label_b": ""
            }
            i += 1
            # Lecture version A
            while i < len(lines) and not lines[i].strip().startswith(MARKER_SEP):
                block["version_a"].append(lines[i])
                i += 1
            i += 1  # passe le séparateur =======
            # Lecture version B
            while i < len(lines) and not lines[i].strip().startswith(MARKER_END):
                block["version_b"].append(lines[i])
                i += 1
            block["label_b"] = lines[i].strip().replace(MARKER_END, "").strip() or "REMOTE"
            blocks.append(block)

        i += 1

    print(f"[EXTRACTION] {len(blocks)} bloc(s) extrait(s) dans '{detection_report['filename']}'")
    for b in blocks:
        print(f"  Bloc {b['block_index']} — A: {len(b['version_a'])} ligne(s) | "
              f"B: {len(b['version_b'])} ligne(s)")
    return blocks


def get_code_versions(block: dict) -> tuple:
    """Retourne (code_A, code_B) sous forme de chaînes."""
    code_a = "\n".join(block["version_a"])
    code_b = "\n".join(block["version_b"])
    return code_a, code_b
