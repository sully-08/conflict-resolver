"""
Module 6 : Aide à la résolution de conflits
Rôle : Générer des recommandations concrètes adaptées au type de conflit
"""


# Guides de résolution par type de conflit
RESOLUTION_GUIDES = {
    "INTRA_METHODE": {
        "titre": "Conflit intra-méthode",
        "enjeux": (
            "Les deux développeurs ont modifié la logique interne de la même fonction. "
            "Il est possible que les deux modifications soient compatibles et puissent coexister."
        ),
        "actions": [
            "Lire attentivement les deux versions pour comprendre l'intention de chaque modification.",
            "Vérifier si les changements sont indépendants (ex: ajout d'un log + modification d'une condition).",
            "Si compatibles : fusionner manuellement en intégrant les deux modifications.",
            "Si incompatibles : consulter l'auteur de l'autre branche avant de choisir.",
            "Lancer les tests unitaires après résolution pour valider le comportement."
        ]
    },
    "STRUCTUREL_RENOMMAGE": {
        "titre": "Conflit structurel – Renommage de fonction",
        "enjeux": (
            "Une fonction a été renommée dans une branche, mais l'ancienne référence "
            "est encore utilisée dans l'autre. Cela provoquera une erreur de compilation "
            "ou un crash à l'exécution."
        ),
        "actions": [
            "Identifier le nouveau nom de la fonction dans la version renommée.",
            "Rechercher dans tout le projet les appels à l'ancien nom (grep ou recherche IDE).",
            "Remplacer tous les appels obsolètes par le nouveau nom.",
            "Vérifier que la signature (paramètres) est identique entre les deux versions.",
            "Compiler le projet et corriger toute erreur résiduelle.",
            "Documenter le renommage dans le message de commit."
        ]
    },
    "SEMANTIQUE_SIGNATURE": {
        "titre": "Conflit sémantique – Changement de signature",
        "enjeux": (
            "La signature d'une fonction a été modifiée (nouveau paramètre ou paramètre supprimé). "
            "Git peut fusionner sans conflit textuel, mais le code résultant peut produire "
            "un bug silencieux ou une erreur à l'exécution."
        ),
        "actions": [
            "Comparer précisément les paramètres des deux versions de la fonction.",
            "Identifier tous les sites d'appel de cette fonction dans le projet.",
            "Mettre à jour chaque appel pour qu'il fournisse le nouveau paramètre.",
            "Si le paramètre est optionnel, définir une valeur par défaut pour assurer la rétrocompatibilité.",
            "Ajouter ou mettre à jour les tests de cette fonction.",
            "Vérifier l'impact sur les interfaces exposées (API, contrat de module)."
        ]
    },
    "MIXTE": {
        "titre": "Conflit mixte",
        "enjeux": (
            "Plusieurs types de différences ont été détectés. "
            "Une analyse manuelle approfondie est nécessaire."
        ),
        "actions": [
            "Analyser les différences structurelles et sémantiques identifiées.",
            "Traiter les renommages en premier (impact le plus large).",
            "Puis traiter les changements de signature.",
            "Enfin, résoudre les conflits de logique interne.",
            "Faire relire la fusion par un autre développeur avant de valider."
        ]
    }
}


def generate_resolution(comparison_report: dict, explanation: str) -> dict:
    """
    Génère un guide de résolution structuré adapté au type de conflit détecté.
    """
    conflict_type = comparison_report.get("conflict_type", "MIXTE")
    guide = RESOLUTION_GUIDES.get(conflict_type, RESOLUTION_GUIDES["MIXTE"])

    # Enrichissement avec les détails spécifiques du conflit
    specific_notes = _build_specific_notes(comparison_report)

    resolution = {
        "conflict_type": conflict_type,
        "titre": guide["titre"],
        "analyse_conflit": explanation,
        "enjeux": guide["enjeux"],
        "actions": guide["actions"],
        "notes_specifiques": specific_notes
    }

    _print_resolution(resolution)
    return resolution


def _build_specific_notes(report: dict) -> list:
    """Ajoute des notes spécifiques au conflit analysé."""
    notes = []
    if report.get("removed_functions"):
        notes.append(f" Fonction(s) à remplacer : {report['removed_functions']}")
    if report.get("added_functions"):
        notes.append(f" Nouvelle(s) fonction(s) dans B : {report['added_functions']}")
    for fn, ch in report.get("param_changes", {}).items():
        notes.append(
            f" '{fn}' : anciens paramètres {ch['version_a']} "
            f"→ nouveaux paramètres {ch['version_b']}"
        )
    if report.get("calls_at_risk"):
        risky = [c["name"] for c in report["calls_at_risk"]]
        notes.append(f" Appels à corriger immédiatement : {risky}")
    return notes


def _print_resolution(resolution: dict):
    print(f"\n[RÉSOLUTION] Guide : {resolution['titre']}")
    print(f"  Enjeux : {resolution['enjeux'][:80]}...")
    print(f"  Actions ({len(resolution['actions'])}) :")
    for i, action in enumerate(resolution["actions"], 1):
        print(f"    {i}. {action}")
    if resolution["notes_specifiques"]:
        print("  Notes spécifiques :")
        for note in resolution["notes_specifiques"]:
            print(f"    {note}")
