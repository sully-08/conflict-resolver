"""
Module 1 : Détection des conflits
Rôle : Identifier les fichiers en conflit et localiser les marqueurs Git
"""

MARKER_START = "<<<<<<<" 
MARKER_SEP   = "======="
MARKER_END   = ">>>>>>>"


def detect_conflicts_in_text(code: str, filename: str = "fichier") -> dict:
    """
    Analyse un texte et détecte la présence de marqueurs de conflit Git.
    Retourne un rapport de détection.
    """
    lines = code.splitlines()
    conflict_zones = []
    in_conflict = False
    start_line = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(MARKER_START):
            in_conflict = True
            start_line = i + 1  # numérotation humaine
        elif stripped.startswith(MARKER_END) and in_conflict:
            conflict_zones.append({
                "start_line": start_line,
                "end_line": i + 1
            })
            in_conflict = False

    has_conflict = len(conflict_zones) > 0

    return {
        "filename": filename,
        "has_conflict": has_conflict,
        "conflict_count": len(conflict_zones),
        "conflict_zones": conflict_zones,
        "raw_lines": lines
    }


def detect_conflicts(files: dict) -> list:
    """
    Entrée : dict { nom_fichier: contenu_texte }
    Sortie : liste des rapports de détection pour les fichiers en conflit
    """
    results = []
    for filename, content in files.items():
        report = detect_conflicts_in_text(content, filename)
        if report["has_conflict"]:
            results.append(report)
            print(f"[DÉTECTION] ✓ Conflit détecté dans '{filename}' "
                  f"({report['conflict_count']} zone(s))")
        else:
            print(f"[DÉTECTION] — Aucun conflit dans '{filename}'")
    return results
